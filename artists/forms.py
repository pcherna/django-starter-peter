from django import forms

from .models import Artist


class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'name', 'role', 'curator', 'bio',
            'public_url', 'public_twitter', 'public_instagram',
            'private_email', 'private_phone'
        ]
