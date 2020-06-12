import logging

from rest_framework import generics, permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Artist
from .serializers import ArtistSerializer
from .forms import ArtistForm
from .admin import ArtistResource

logger = logging.getLogger(__name__)

# TODO:
# - default sort and filter need to be properties somehow, and derive ordering from that

class SortableListMixin(object):
    ordering = [Lower('name')]
    sort_by = 'name'
    _sort_tag = ''

    def __init__(self):
        super().__init__()
        self._sort_tag = self.model.__name__.lower() + '_sort'

    def get_ordering(self):
        # Use session variables to persist sort settings, override with query-args
        self.sort_by = self.request.GET.get('sort', self.request.session.get(self._sort_tag, 'name'))
        self.request.session[self._sort_tag] = self.sort_by
        if self.sort_by == '-name':
            result = [Lower('name').desc()]
        elif self.sort_by == 'name':
            result = [Lower('name')]
        else:
            result = self.sort_by
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sort'] = self.sort_by
        return context


class FilterableListMixin(object):
    filter_by = ''
    _filter_tag = ''

    def __init__(self):
        super().__init__()
        self._filter_tag = self.model.__name__.lower() + '_filter'

    def get_queryset(self):
        qs = super().get_queryset()
        # Use session variables to persist filter settings, override with query-args
        self.filter_by = self.request.GET.get('filter', self.request.session.get(self._filter_tag, ''))
        self.request.session[self._filter_tag] = self.filter_by
        if self.filter_by:
            qs = qs.filter(name__icontains=self.filter_by)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['unfiltered_count'] = Artist.objects.count
        context['filter'] = self.filter_by
        return context


class ArtistsListView(SortableListMixin, FilterableListMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Artist
    paginate_by = 20
    template_name = 'artists/artists_list.html'
    context_object_name = 'objects'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistsListView, self).get_context_data(*args, **kwargs)
        return context

    def test_func(self):
        return self.request.user.has_perm('artists.view_artist')


class ArtistDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Artist

    def test_func(self):
        return self.request.user.has_perm('artists.view_artist')


class ArtistCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Artist
    form_class = ArtistForm

    def form_valid(self, form):
        form.instance.creation_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm('artists.add_artist')


class ArtistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Artist
    form_class = ArtistForm

    # Add current user to form before validating
    def form_valid(self, form):
        form.instance.modification_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.has_perm('artists.change_artist')


class ArtistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Artist
    success_url = reverse_lazy('artists-list')

    def test_func(self):
        return self.request.user.has_perm('artists.delete_artist')

# By putting a Byte-Order-Mark at the head of the CSV file, it loads into Excel
# with proper Unicode support
BOM = '\ufeff'

def artist_export_view(request):
    dataset = ArtistResource().export()
    response = HttpResponse(BOM + dataset.csv,
                            content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="artists_export.csv"'
    return response


# API views


class ArtistsListAPI(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = 'Artists'
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ArtistDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = 'Artist Detail'
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
