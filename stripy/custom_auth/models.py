import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from stripy.settings import DEFAULT_AVATAR_IMAGE, MEDIA_URL


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    photo = models.ImageField(blank=False, default=DEFAULT_AVATAR_IMAGE, upload_to=f"avas")

    def __str__(self):
        return f"{self.user.username} avatar"

    def url(self):
        return os.path.join(MEDIA_URL, str(self.photo))

    def get_photo(self):
        # used in the admin site model as a "thumbnail"
        # TODO: create thumbnail
        html = '<img src="{}" width="150" height="150" />'
        return mark_safe(html.format(self.url()))