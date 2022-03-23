"""
First version of the Zotero Library Updates Mailer
"""

import smtplib, ssl
import requests

# TODO: get details defined in config.yaml

# TODO: make API call and read results

# TODO: prepare email text
import yaml


def get_config():
    with open("config.yaml", "r") as stream:
        config = yaml.safe_load(stream)
    return config


def get_mail_config():
    return get_config()["email_configuration"]


def get_api_config():
    return get_config()["API_configuration"]


def call_api():
    api_key = get_api_config()["API_key"]
    user_id = get_api_config()["user_id"]
    is_group = get_api_config()["is_group"]
    if is_group:
        group_id = get_group_id(user_id, api_key)
        prefix = "/groups/" + group_id
    else:
        prefix = "/users/" + user_id

    with requests.Session() as s:
        s.headers = {'Authorization': "Bearer " + api_key}

        request_string = "https://api.zotero.org" + prefix + "/searches/"
        searches = s.get(request_string)

        for item in searches.json():
            if item['data']['name'] == get_api_config()["saved_search_name"]:
                search_key = item['data']['key']

        request_string = "https://api.zotero.org" + prefix + "/searches?searchKey=" + search_key + "/items?format=bib"
        search = s.get(request_string)
        print(search)

def get_group_id(user_id, api_key):
    with requests.Session() as s:
        s.headers = {'Authorization': "Bearer " + api_key}
        group_id = s.get("https://api.zotero.org" + "/users/" + user_id + "/groups?id").json()[0]['id']
        return str(group_id)

call_api()


