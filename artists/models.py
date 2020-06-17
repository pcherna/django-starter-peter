from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Artist(models.Model):

    ARTIST_TYPE_NONE = "None"
    ARTIST_TYPE_ARTIST = "Artist"
    ARTIST_TYPE_COMMISSIONED_ARTIST = "Commissioned"
    ARTIST_TYPE_WORKSHOP_PARTICIPANT = "Storyteller"
    ROLE_CHOICES = [
        (ARTIST_TYPE_NONE, "None"),
        (ARTIST_TYPE_ARTIST, "Artist"),
        (ARTIST_TYPE_COMMISSIONED_ARTIST, "Commissioned Artist"),
        (ARTIST_TYPE_WORKSHOP_PARTICIPANT, "Storyteller"),
    ]

    name = models.CharField("Artist Name", max_length=200)
    bio = models.TextField("Artist Bio", blank=True, max_length=5000)
    role = models.CharField(
        "Artist Type", choices=ROLE_CHOICES, default=ARTIST_TYPE_ARTIST, max_length=20
    )

    public_url = models.CharField("Artist Website", blank=True, max_length=500)
    public_twitter = models.CharField("Artist Twitter", blank=True, max_length=500)
    public_instagram = models.CharField("Artist Instagram", blank=True, max_length=500)

    private_email = models.CharField(
        "Contact Email (private)", blank=True, max_length=100
    )
    private_phone = models.CharField(
        "Contact Phone (private)", blank=True, max_length=100
    )

    # Tracking fields
    creation_date = models.DateTimeField(default=timezone.now)
    creation_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="artist_creation_user", null=True
    )
    modification_date = models.DateTimeField(default=timezone.now)
    modification_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="artist_modification_user",
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("artist-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = timezone.now()
        self.modification_date = timezone.now()
        return super(Artist, self).save(*args, **kwargs)
