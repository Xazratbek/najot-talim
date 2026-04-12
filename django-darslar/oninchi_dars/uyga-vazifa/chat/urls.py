from django.urls import path
from .views import ChatPlaceholderView, ChatDetailView, SendMessageView, ChatListView

app_name = "chat"

urlpatterns = [
    path("", ChatListView.as_view(), name="list"),
    path('message/send/<int:pk>/', SendMessageView.as_view(), name='send_message'),
    path("<int:pk>/", ChatDetailView.as_view(), name="room_detail"),
]
