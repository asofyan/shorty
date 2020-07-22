import requests

from config import SHORTY_API_URL, AUTH_HEADER

URL = SHORTY_API_URL

def shorten(target_url, custom='', tag=''):
    endpoint = URL + '/v1/shorten'
    headers = { 'Authorization': AUTH_HEADER }
    params = { 'url': target_url }

    if custom:
        params['custom'] = custom

    if tag:
        params['tag'] = tag

    return requests.post(endpoint,  headers=headers, params=params)

def shorten_profile(url, code):
    return shorten(url, custom=code, tag='profile')
