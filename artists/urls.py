from django.urls import path

from .views import (
    ArtistsListView,
    ArtistDetailView,
    ArtistCreateView,
    ArtistUpdateView,
    ArtistDeleteView,
    artist_export_view,
)

urlpatterns = [
    path("", ArtistsListView.as_view(), name="artists-list"),
    path("<int:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("new/", ArtistCreateView.as_view(), name="artist-create"),
    path("<int:pk>/update/", ArtistUpdateView.as_view(), name="artist-update"),
    path("<int:pk>/delete/", ArtistDeleteView.as_view(), name="artist-delete"),
    path("export/", artist_export_view, name="artists-export"),
]
