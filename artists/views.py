import logging

from rest_framework import generics, permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Artist
from .serializers import ArtistSerializer
from .forms import ArtistForm
from .admin import ArtistResource

from django_starter_peter.mixins.sortfilter import (
    SortableListMixin,
    FilterableListMixin,
)

logger = logging.getLogger(__name__)


class ArtistsListView(
    SortableListMixin,
    FilterableListMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView,
):
    model = Artist
    paginate_by = 20
    template_name = "artists/artists_list.html"
    context_object_name = "objects"

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistsListView, self).get_context_data(*args, **kwargs)
        return context

    def test_func(self):
        return self.request.user.has_perm("artists.view_artist")


class ArtistDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Artist

    def test_func(self):
        return self.request.user.has_perm("artists.view_artist")


class ArtistCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Artist
    form_class = ArtistForm

    def form_valid(self, form):
        form.instance.creation_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm("artists.add_artist")


class ArtistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Artist
    form_class = ArtistForm

    # Add current user to form before validating
    def form_valid(self, form):
        form.instance.modification_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm("artists.change_artist")


class ArtistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Artist
    success_url = reverse_lazy("artists-list")

    def test_func(self):
        return self.request.user.has_perm("artists.delete_artist")


# By putting a Byte-Order-Mark at the head of the CSV file, it loads into Excel
# with proper Unicode support
BOM = "\ufeff"


def artist_export_view(request):
    dataset = ArtistResource().export()
    response = HttpResponse(BOM + dataset.csv, content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="artists_export.csv"'
    return response


# API views


class ArtistsListAPI(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = "Artists"
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ArtistDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = "Artist Detail"
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
