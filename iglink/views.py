import json
from django.http import HttpResponse
from .cache import json_response_cache_page_decorator
from .models import InstagramAPISettings
from .scraper import instagram_profile_obj, get_profile_media
from django.conf import settings as base_settings
import os
import json


class Settings:
    """
    Retrieve last given username from model.
    """
    field_name = 'ig_username'
    obj = InstagramAPISettings()
    field_value = getattr(obj, field_name)


@json_response_cache_page_decorator(60)
def profile_data_json(request):
    """
    Retrieve JSON data of user profile.
    If request limit or errors, serve from cache.
    :param request:
    """
    settings = Settings()

    profile = instagram_profile_obj(username=settings.field_value)

    response_data = {'profile': profile}

    if KeyError or TypeError:
        backup_path = os.path.join(os.path.abspath('cache'), "ig-profile-cache.json")
        return HttpResponse(open(backup_path, 'r'), content_type='application/json; charset=utf8')
    else:
        return HttpResponse(json.dumps(response_data['profile']), content_type="application/json")


@json_response_cache_page_decorator(60)
def recent_media_json(request):
    """
    Retrieve JSON data of recent media from user profile.
    If request limit or errors, serve from cache.
    :param: request:
    """
    settings = Settings()

    profile = instagram_profile_obj(username=settings.field_value)
    recent_media = get_profile_media(profile=profile)

    response_data = {'recent_media': recent_media}

    if KeyError or TypeError:
        backup_path = os.path.join(os.path.abspath('cache'), "ig-recent-media-cache.json")
        return HttpResponse(open(backup_path, 'r'), content_type='application/json; charset=utf8')
    else:
        return HttpResponse(json.dumps(response_data['recent_media']), content_type="application/json")
