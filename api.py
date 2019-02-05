"""
This module queries Zoho Desk's API to obtain lists of clients, tickets, etc.
"""
import requests
import os
import itertools
import json
import datetime

api_root = 'https://desk.zoho.com/api/v1/'
token = os.environ.get('ZOHO_DESK_API_TOKEN')
org_id = os.environ.get('ZOHO_DESK_API_ORG_ID')


def get(endpoint, *args, **kwargs):
    url = api_root + endpoint
    auth = 'Zoho-authtoken ' + token

    if kwargs.get('headers') is None:
        kwargs['headers'] = dict()
    kwargs['headers']['orgId'] = org_id
    kwargs['headers']['Authorization'] = auth

    response = requests.get(url, *args, **kwargs)
    if (response.raise_for_status() is None):
        return response


def list_accounts(start, limit):
    endpoint = 'accounts'
    params = {'from': start,
              'limit': limit}
    response = get(endpoint, params=params)

    accounts = response.json()['data']
    return accounts


def get_all_accounts():
    def accounts_generator():
        for start in itertools.count(0, 99):
            limit = 99
            accounts = list_accounts(start, limit)
            yield accounts

    def accounts_len_99(accounts):
        return len(accounts) == 99

    accounts = sum(itertools.takewhile(accounts_len_99,
                                       accounts_generator()), [])
    return accounts


def cache_accounts():
    data = get_all_accounts()
    filename = 'accounts.json'
    cache_data(data, filename)


# Accounts cache section; put in a separate file?
cwd = os.getcwd()
temp_dir = cwd + '/temp/'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


def cache_data(data, filename):
    if not cache_is_fresh(filename):
        file_path = temp_dir + filename
        with open(file_path, 'w') as f:
            json.dump(data, f)


def cache_is_fresh(filename):
    file_path = temp_dir + filename
    yesterday = datetime.date.today() - datetime.timedelta(1)
    if os.path.isfile(file_path):
        last_mod_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        if last_mod_date < yesterday:
            return False
        return True
    else:
        return False
