import requests

URL = 'https://jatayu.azurewebsites.net'

def get_referral_by_code(code):
    url = URL + '/referralcode/bycode/' + code
    res = requests.get(url)
    return res