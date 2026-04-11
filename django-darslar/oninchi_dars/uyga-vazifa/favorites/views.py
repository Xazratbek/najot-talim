from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Favorite
from listings.models import Listing

class ToggleFavoriteView(View):
    def post(self, request, uuid):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'login_required'}, status=403)

        listing = get_object_or_404(Listing, uuid=uuid)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            favorite_listing=listing
        )

        if not created:
            favorite.delete()
            status = 'removed'
        else:
            status = 'added'

        return JsonResponse({
            'status': status,
            'favorite_count': Favorite.objects.filter(favorite_listing=listing).count()
        })
