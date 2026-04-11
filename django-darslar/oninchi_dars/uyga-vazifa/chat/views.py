from django.views.generic import TemplateView


class ChatPlaceholderView(TemplateView):
    template_name = "placeholders/chat.html"
