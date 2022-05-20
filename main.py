"""
First version of the Zotero Library Updates Mailer
"""
import datetime
import smtplib, ssl
import requests
import json
from datetime import *

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
        request_string = "https://api.zotero.org" + prefix + "/items/sort=dateAdded/direction=desc"

        search = s.get(request_string)
        print(search)
        sorted_json = search.json()
        with open('json_data.json', 'w') as outfile:
            outfile.write(json.dumps(sorted_json))

        get_recent_entries_as_string(search.json(), get_api_config()["period_in_days"])


def get_group_id(user_id, api_key):
    with requests.Session() as s:
        s.headers = {'Authorization': "Bearer " + api_key}
        group_id = s.get("https://api.zotero.org" + "/users/" + user_id + "/groups?id").json()[0]['id']
        return str(group_id)


def get_search_key(userprefix, api_key):
    with requests.Session() as s:
        s.headers = {'Authorization': "Bearer " + api_key}

        request_string = "https://api.zotero.org" + userprefix + "/searches/"

        for item in s.get(request_string).json():
            if item['data']['name'] == get_api_config()["saved_search_name"]:
                search_key = item['data']['key']


def sort_json_by_date_modified(json_string):
    return sorted(json_string, key=lambda x: datetime.strptime(x['data']['dateModified'][0:10], '%Y-%m-%d'))


def get_recent_entries_as_string(items_json, period_in_days):
    counter_true = 0
    counter_false = 0

    for item in items_json:
        if datetime.today() - datetime.strptime(item['data']['dateModified'][0:10], '%Y-%m-%d') <= timedelta(days=period_in_days):
            counter_true += 1
            print(counter_true)
            print(counter_false)
            print(datetime.strptime(item['data']['dateAdded'][0:10], '%Y-%m-%d'))
        else:
            counter_false += 1
            print(datetime.strptime(item['data']['dateAdded'][0:10], '%Y-%m-%d'))


    print("------")
    print("Included: " + str(counter_true))
    print("Excluded: " + str(counter_false))


def get_library_version(user_id, api_key):
    with requests.Session() as s:
        s.headers = {'Authorization': "Bearer " + api_key}
        version = s.get("https://api.zotero.org" + "/users/" + get_group_id(user_id, api_key) + "/items?format=versions").json()
        print(str(version))

#call_api()
get_library_version("8267074", "AwmIsxfG9L39daG3z8tSVcfr")