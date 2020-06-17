from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Artist


class ArtistResource(resources.ModelResource):

    class Meta:
        model = Artist
        fields = (
            'name',
            'bio',
            'role',
            'public_url',
            'public_twitter',
            'public_instagram',
            'private_email',
            'private_phone',
            'creation_date',
            'creation_user__username',
            'modification_date',
            'modification_user__username',
        )



@admin.register(Artist)
class ArtistAdmin(ImportExportModelAdmin):
    resource_class = ArtistResource
