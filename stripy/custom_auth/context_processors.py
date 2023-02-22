from django.http import HttpRequest

from stripy.settings import DEFAULT_AVATAR_URL
from custom_auth.models import Avatar


def get_avatar_url(req: HttpRequest):
    user = req.user
    url = DEFAULT_AVATAR_URL
    if req.user.is_authenticated:
        try:
            url = Avatar.objects.get(user=user).url()
        except Avatar.DoesNotExist:
            default_avatar = Avatar(user=user)
            default_avatar.save()
            url = default_avatar.url()
    return {'avatar_url': url}


def get_avatar_username(req: HttpRequest):
    user = req.user
    username = 'Anonymous'
    if req.user.is_authenticated:
        username = user.username
    return {'avatar_username': username}
