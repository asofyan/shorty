import requests

from config import SHORTY_API_URL, AUTH_HEADER

URL = SHORTY_API_URL

def shorten(url, custom='', tag=''):
    url = URL + '/v1/shorten'
    headers = { 'Authorization': AUTH_HEADER }
    params = { 'url', url }
    print('params', params)
    print('header', headers

    if custom:
        params['custom'] = custom

    if tag:
        params['tag'] = tag

    print('params', params)
    print('header', headers)

    return requests.post(URL,  headers=headers, params=params)

def shorten_profile(url, code):
    return shorten(url, custom=code, tag='profile')
