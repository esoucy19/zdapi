"""
This module queries Zoho Desk's API to obtain lists of clients, tickets, etc.
"""
import requests
import os
import itertools

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
    pass
