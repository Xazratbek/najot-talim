from django.views.generic import TemplateView


class ReviewsPlaceholderView(TemplateView):
    template_name = "placeholders/reviews.html"
