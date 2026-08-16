from rest_framework import serializers

from tenants.models import Employee, Service

from .models import Appointment, Client


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "duration_minutes", "price", "description"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position"]


class AvailabilityQuerySerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.filter(is_active=True))
    date = serializers.DateField()
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(is_active=True), required=False, allow_null=True
    )


class ClientInputSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    telegram_user_id = serializers.CharField(max_length=50, required=False, allow_blank=True)


class BookingCreateSerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.filter(is_active=True))
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.filter(is_active=True), required=False, allow_null=True
    )
    start_time = serializers.DateTimeField()
    client = ClientInputSerializer()
    notes = serializers.CharField(required=False, allow_blank=True)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "service",
            "employee",
            "client",
            "start_time",
            "end_time",
            "status",
            "notes",
        ]
        read_only_fields = fields
