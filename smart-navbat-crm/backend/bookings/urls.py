from django.urls import path

from .views import (
    AvailabilityView,
    BookingCreateView,
    ServiceListView,
    TenantBotInfoView,
)

urlpatterns = [
    path("public/<slug:tenant_slug>/services/", ServiceListView.as_view(), name="public-services"),
    path(
        "public/<slug:tenant_slug>/availability/",
        AvailabilityView.as_view(),
        name="public-availability",
    ),
    path("public/<slug:tenant_slug>/book/", BookingCreateView.as_view(), name="public-book"),
    path(
        "internal/<slug:tenant_slug>/bot-info/",
        TenantBotInfoView.as_view(),
        name="internal-bot-info",
    ),
]
