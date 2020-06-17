from rest_framework import serializers
from artists.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "bio",
            "role",
            "public_url",
            "public_twitter",
            "public_instagram",
        ]
