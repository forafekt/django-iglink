"""
Created on 20/sep/2020

@author: Jonny Doyle
"""

import json
import logging
from socket import error as socket_error

import requests
from lxml import html
from requests.exceptions import ConnectionError, HTTPError

from rest.iglink.cache import cached_token

SCRIPT_JSON_PREFIX = 18
SCRIPT_JSON_DATA_INDEX = 21

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)


def instagram_scrap_profile(username):
    """
    Scrap an instagram profile page
    :param username:
    :return:
    """
    try:
        url = "https://www.instagram.com/{}/".format(username)
        page = requests.get(url)
        # Raise error for 404 cause by a bad profile name
        page.raise_for_status()
        return html.fromstring(page.content)
    except HTTPError:
        logging.exception('user profile "{}" not found'.format(username))
    except (ConnectionError, socket_error) as error:
        error.logging.exception("Error connecting to Instagram. \n"
                                "Check your username is correct & check your internet connection.")


def instagram_profile_js(username):
    """
    Retrieve the script tags from the parsed page.
    :param username:
    :return:
    """
    try:
        tree = instagram_scrap_profile(username)
        return tree.xpath('//script')
    except AttributeError:
        logging.exception("scripts not found")
        return None


def instagram_profile_json(username):
    """
    Get the JSON data string from the scripts.
    :param username:
    :return:
    """
    scripts = instagram_profile_js(username)
    source = None

    if scripts:
        for script in scripts:
            if script.text:
                if script.text[0:SCRIPT_JSON_PREFIX] == "window._sharedData":
                    source = script.text[SCRIPT_JSON_DATA_INDEX:-1]

    return source


@cached_token('ig-profile-cache.json')
def instagram_profile_obj(username):
    """
    Retrieve the JSON from the page and parse it to a python dict.
    :param username:
    :return:
    """
    json_data = instagram_profile_json(username)
    try:
        return json.loads(json_data) if json_data else None
    except (KeyError, TypeError):
        while KeyError == 'ProfilePage':
            pass
        logger.exception("Profile timeout")


@cached_token('ig-recent-media-cache.json')
def get_profile_media(profile, page=0):
    """
    Parse a generated media object
    :param profile:
    :param page:
    :return:
    """
    try:
        edges = profile['entry_data']['ProfilePage'][page]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        if KeyError or TypeError:
            return None
        else:
            return [edge['node'] for edge in edges]
    except (KeyError, TypeError):
        logger.exception("Either request limit reached or incorrect username. \n"
                         "Instagram data is now being served from last successful Json response. \n"
                         "Data will update once limit has been reset and will again cache last successful response.")
        return None
