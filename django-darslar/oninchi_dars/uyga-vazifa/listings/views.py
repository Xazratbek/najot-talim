from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import Listing, ListingImage
from django.db.models import F
from .forms import ListingForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from categories.models import Category
from django.views import View
from chat.models import ChatRoom, Message
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages

class ListingListView(ListView):
    model = Listing
    template_name = "listing/list.html"
    context_object_name = "listings"
    paginate_by = 30

    def get_queryset(self):
        queryset = (
            Listing.objects.filter(status="active")
            .select_related("user", "listing_category")
            .prefetch_related("images")
            .order_by("-created_at")
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(city__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["root_categories"] = Category.objects.filter(parent__isnull=True).prefetch_related("categories")[:10]
        context["featured_listings"] = list(context["listings"][:8])
        context["current_q"] = self.request.GET.get("q", "").strip()
        return context

class ListingDetailView(DetailView):
    model = Listing
    template_name = "listing/detail.html"
    context_object_name = "listing"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return Listing.objects.select_related("user", "listing_category").prefetch_related("images")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        Listing.objects.filter(uuid=obj.uuid).update(view_count=F("view_count") + 1)
        obj.refresh_from_db(fields=["view_count"])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_listings"] = (
            Listing.objects.filter(
                listing_category=self.object.listing_category,
                status="active",
            )
            .exclude(uuid=self.object.uuid)
            .select_related("user", "listing_category")
            .prefetch_related("images")[:8]
        )
        return context

class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    template_name = "listing/create.html"
    form_class = ListingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.view_count = 0
        response = super().form_valid(form)
        for index, image in enumerate(self.request.FILES.getlist("images")):
            ListingImage.objects.create(
                listing=self.object,
                image=image,
                is_main=index == 0,
            )
        return response

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    template_name = "listing/update.html"
    form_class = ListingForm
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def test_func(self):
        return self.get_object().user_id == self.request.user.id

    def form_valid(self, form):
        response = super().form_valid(form)
        uploaded_images = self.request.FILES.getlist("images")
        for index, image in enumerate(uploaded_images):
            ListingImage.objects.create(
                listing=self.object,
                image=image,
                is_main=not self.object.images.filter(is_main=True).exists() and index == 0,
            )
        return response

    def get_success_url(self):
        return reverse_lazy("listing:detail",kwargs={"uuid": self.object.uuid})

class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    template_name = "listing/delete.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def test_func(self):
        return self.get_object().user_id == self.request.user.id

    def get_success_url(self):
        return reverse_lazy("accounts:profile")

    def form_valid(self, form):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = "deleted"
        self.object.save(update_fields=["status"])
        return HttpResponseRedirect(success_url)


class AskSellerView(View):
    def post(self, request, uuid):
        text = request.POST.get("text","")
        if not text.strip():
            messages.warning(request, "Bo'sh xabar yozmang")
            return redirect(request.META.get('HTTP_REFERER', 'listing:list'))

        listing = Listing.objects.filter(uuid=uuid).select_related("user")
        if listing.user == request.user:
            messages.warning("O'zingizni xabaringizga xabar yozish mumkin emas.")
            return redirect(request.META.get('HTTP_REFERER', 'listing:list'))

        chat_room, created = ChatRoom.objects.get_or_create(chat_listing=listing[0],buyer=self.request.user,defaults={'seller': listing.user})

        if created:
            Message.objects.create(room=chat_room,sender=request.user,text=text)
        else:
            room = ChatRoom.objects.create(chat_listing=listing,buyer=request.user,seller=listing[0].user)
            Message.objects.create(room=room,sender=request.user,text=text)
            return redirect('chat:room_detail', room_id=chat_room.id)
