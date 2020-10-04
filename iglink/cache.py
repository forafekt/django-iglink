import os
import json
import hashlib
import functools
from django import http
from django.core.cache import cache
from django.utils.encoding import force_bytes, iri_to_uri


def json_response_cache_page_decorator(seconds):
    """
    First attempt to cache json, if fails move to 'cache_token'
    """
    """Cache only when there's a healthy http.JsonResponse response."""

    def decorator(func):
        """
        Decorator wrapper
        :param: func:
        """

        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            """
            Cache response
            """
            cache_key = 'json_response_cache:{}:{}'.format(
                func.__name__,
                hashlib.md5(force_bytes(iri_to_uri(
                    request.build_absolute_uri()
                ))).hexdigest()
            )
            content = cache.get(cache_key)
            if content is not None:
                return http.HttpResponse(
                    content,
                    content_type='application/json'
                )
            response = func(request, *args, **kwargs)
            if (
                    isinstance(response, http.JsonResponse) and
                    response.status_code in (200, 304)
            ):
                cache.set(cache_key, response.content, seconds)
            return response

        return inner

    return decorator


def cached_token(jsonfile):
    """
    Cache only valid data if any exceptions from live requests.
    If live requests response is null, data will serve from cached JSON file
    and later update once a valid request is made.
    """
    def has_valid_token(data):
        """
        Check if a valid token.
        """
        if KeyError or TypeError:
            try:
                exit(0)
            except:
                exit(1)
        else:
            return 'token' in data

    def get_token_from_file():
        """
        Get the data to cache.
        """
        with open(os.path.join('cache', jsonfile), ) as f:
            data = json.load(f)
            if has_valid_token(data):
                if KeyError or TypeError:
                    try:
                        exit(0)
                    except:
                        exit(1)
                else:
                    return data.get('token')

    def save_token_to_file(token):
        """
        Save the cache data usable for API requests.
        """
        if token:
            with open(os.path.join('cache', jsonfile), 'w') as f:
                json.dump(token, f)

    def decorator(fn):
        """
        Decorate the view function as follows:
        @cached_token('ig-profile-cache.json')
        @cached_token('ig-recent-media-cache.json')
        """
        def wrapped(*args, **kwargs):
            """
            Wrap function.
            """
            if os.path.exists(jsonfile):
                token = get_token_from_file()
                if token:
                    return f'{token} (cached!!)'
            res = fn(*args, **kwargs)
            save_token_to_file(res)
            return res

        return wrapped

    return decorator
