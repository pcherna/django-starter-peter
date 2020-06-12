from artists import views
from django.urls import path

urlpatterns = [
    path('', views.ArtistsListAPI.as_view()),
    path('<int:pk>/', views.ArtistDetailAPI.as_view()),
]
