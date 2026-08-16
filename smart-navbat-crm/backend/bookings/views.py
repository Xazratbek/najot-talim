from datetime import timedelta

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tenants.models import Tenant

from .models import Appointment, Client
from .permissions import IsInternalService
from .serializers import (
    AppointmentSerializer,
    AvailabilityQuerySerializer,
    BookingCreateSerializer,
    ServiceSerializer,
)
from .services import get_available_slots, notify_new_appointment


class TenantScopedAPIView(APIView):
    """Base for the public booking API: every endpoint hangs off a tenant slug.

    Deliberately AllowAny — this is the surface the public booking page and
    the Telegram bot call on behalf of end customers, who never log in.
    """

    permission_classes = [AllowAny]

    def get_tenant(self, tenant_slug):
        return get_object_or_404(Tenant, slug=tenant_slug, is_active=True)


class ServiceListView(TenantScopedAPIView):
    def get(self, request, tenant_slug):
        tenant = self.get_tenant(tenant_slug)
        services = tenant.services.filter(is_active=True)
        return Response(ServiceSerializer(services, many=True).data)


class AvailabilityView(TenantScopedAPIView):
    def get(self, request, tenant_slug):
        tenant = self.get_tenant(tenant_slug)
        query = AvailabilityQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        service = query.validated_data["service"]
        if service.tenant_id != tenant.id:
            return Response({"detail": "Xizmat topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        employee = query.validated_data.get("employee")
        if employee and employee.tenant_id != tenant.id:
            return Response({"detail": "Xodim topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        slots = get_available_slots(service, query.validated_data["date"], employee)
        return Response({"slots": [slot.isoformat() for slot in slots]})


class BookingCreateView(TenantScopedAPIView):
    def post(self, request, tenant_slug):
        tenant = self.get_tenant(tenant_slug)
        payload = BookingCreateSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        data = payload.validated_data

        service = data["service"]
        employee = data.get("employee")
        if service.tenant_id != tenant.id or (employee and employee.tenant_id != tenant.id):
            return Response(
                {"detail": "Xizmat yoki xodim ushbu biznesga tegishli emas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        client_data = data["client"]
        telegram_user_id = client_data.get("telegram_user_id")
        if telegram_user_id:
            client, _ = Client.objects.get_or_create(
                tenant=tenant,
                telegram_user_id=telegram_user_id,
                defaults={
                    "full_name": client_data["full_name"],
                    "phone": client_data.get("phone", ""),
                },
            )
        else:
            client = Client.objects.create(
                tenant=tenant,
                full_name=client_data["full_name"],
                phone=client_data.get("phone", ""),
            )

        start_time = data["start_time"]
        end_time = start_time + timedelta(minutes=service.duration_minutes)

        try:
            with transaction.atomic():
                appointment = Appointment.objects.create(
                    tenant=tenant,
                    service=service,
                    employee=employee,
                    client=client,
                    start_time=start_time,
                    end_time=end_time,
                    status=Appointment.Status.CONFIRMED,
                    notes=data.get("notes", ""),
                )
        except IntegrityError:
            return Response(
                {"detail": "Bu vaqt allaqachon band qilingan. Boshqa vaqtni tanlang."},
                status=status.HTTP_409_CONFLICT,
            )

        notify_new_appointment(appointment)
        return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)


class TenantBotInfoView(APIView):
    """Internal endpoint: lets bot_service resolve a tenant's bot token."""

    permission_classes = [IsInternalService]

    def get(self, request, tenant_slug):
        tenant = get_object_or_404(Tenant, slug=tenant_slug, is_active=True)
        return Response({"name": tenant.name, "bot_token": tenant.telegram_bot_token})
