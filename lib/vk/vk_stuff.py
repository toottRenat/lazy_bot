# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from urllib.parse import parse_qs
import webbrowser
import pickle
from datetime import datetime, timedelta
import vk
import time

# id of vk.com application
# APP_ID = 6043173
APP_ID =6054131
# file, where auth data is saved
AUTH_FILE = '.auth_data'
# chars to exclude from filename
FORBIDDEN_CHARS = '/\\\?%*:|"<>!'


def get_saved_auth_params():
    access_token = None
    user_id = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            token = pickle.load(pkl_file)
            expires = pickle.load(pkl_file)
            uid = pickle.load(pkl_file)
        if datetime.now() < expires:
            access_token = token
            user_id = uid
    except IOError:
        pass
    return access_token, user_id


def save_auth_params(access_token, expires_in, user_id):
    expires = datetime.now() + timedelta(seconds=int(expires_in))
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)
        pickle.dump(expires, output)
        pickle.dump(user_id, output)


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=wall,messages&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token".format(app_id=APP_ID))
    webbrowser.open_new_tab(auth_url)
    redirected_url = "https://oauth.vk.com/blank.html#access_token=9c1b7343ed95358f82abb1e8a087951fb8a4ad77" \
                     "604ad2406c230167701122ba74c9314e0fa93af644a49&expires_in=86400&user_id=3920099"
    #redirected_url = input("Paste here url you were redirected:\n")
    aup = parse_qs(redirected_url)
    aup['access_token'] = aup.pop(
        '#access_token')
    save_auth_params(aup['access_token'][0], aup['expires_in'][0],
                     aup['user_id'][0])
    return aup['access_token'][0], aup['user_id'][0]


def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)


def send_message(api, user_id, message, **kwargs):
    data_dict = {
        'user_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.messages.send(**data_dict)


def main():
    access_token, _ = get_saved_auth_params()
    if not access_token or not _:
        access_token, _ = get_auth_params()
    api = get_api(access_token)
    # "https://oauth.vk.com/blank.html#access_token=5d48a5b8ac84717405354d5549b2b0cb845e03eafe19fe4666f3583121c32a2b7656bf38eb8dc1557615d&expires_in=86400&user_id=3920099"
    #users = [95249893]
    users = [3920099]
    user_text = "."
    for user_id in users:
        print("User ", user_id)
        res = send_message(api, user_id=user_id, message=user_text)
        time.sleep(1)
        print(res)

main()
