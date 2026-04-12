from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.views import View
from .models import ChatRoom, Message
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q

class ChatPlaceholderView(TemplateView):
    template_name = "placeholders/chat.html"

class ChatDetailView(View):
    def get(self, request, pk):
        room = get_object_or_404(ChatRoom,pk=pk)
        if request.user != room.buyer and request.user != room.seller:
            return HttpResponseForbidden("Bu chat xonasiga kirishga ruxsat yo'q.")

        Message.objects.filter(room=room, is_read=False).exclude(sender=request.user).update(is_read=True)
        all_messages = Message.objects.filter(room=room).order_by('created_at').select_related('sender')

        other_user = room.seller if request.user == room.buyer else room.buyer
        context = {
            "room": room,
            "messages": all_messages,
            "other_user": other_user
         }
        return render(request, "chat/detail.html", context)

class SendMessageView(View):
    def post(self, request,pk):
        room = get_object_or_404(ChatRoom, pk=pk)
        text = request.POST.get("text","")

        if text.strip():
            Message.objects.create(room=room,sender=request.user,text=text)
            return redirect('chat:room_detail', pk=pk)

class ChatListView(View):
    def get(self, request):
        chats = ChatRoom.objects.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)).order_by("-updated_at").select_related("buyer","seller","chat_listing")
        return render(request,"chat/list.html",context={"chat_rooms": chats})