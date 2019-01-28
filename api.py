"""
This module queries Zoho Desk's API obtain lists of clients, tickets, etc.
"""
import requests
import itertools

api_root = 'https://desk.zoho.com/api/v1/'


def get(endpoint, token, org_id='', headers={}):
    """
    This is our main HTTP get function.

    Takes the following parameters:

    endpoint: String, the API endpoint to use, i.e. 'accounts?from=0&limit=99'
    token: String, the auth token to provide
    org_id: String, id of the organization to query. Usually required except
            when querying for organizations.
    headers: Dict, additionnal headers to provide if needed

    Returns an HTTP response object

    example:
    response = api.get(endpoint='accounts?from=0&limit=99',
                       token=token,
                       org_id=org_id)
    """
    url = ''.join([api_root, endpoint])
    auth = ''.join(['Zoho-authtoken ', token])

    request_headers = dict(headers, Authorization=auth, orgID=org_id)

    response = requests.get(url, headers=request_headers)
    if (response.raise_for_status() is None):
        return response


def get_accounts(token, org_id, start, limit):
    """
    Returns a list of dict objects containing all accounts for a given org_id
    and range, starting at 'start' and ending at 'limit'.
    """
    endpoint = ''.join(['accounts?from=', str(start),
                        '&limit=', str(limit)])

    response = get(endpoint=endpoint,
                   token=token,
                   org_id=org_id)

    accounts = response.json()['data']
    return accounts


def get_all_accounts(token, org_id):
    """
    Returns a list of dict objects containing all accounts for a given org_id.
    """

    def accounts_generator(token, org_id):
        for start in itertools.count(0, 99):
            limit = 99
            accounts = get_accounts(token, org_id, start, limit)
            yield accounts

    def accounts_len_99(accounts):
        """
        Gets a list of accounts and returns of tuple containing the list of
        accounts and its length.
        """
        return len(accounts) == 99

    accounts = sum(itertools.takewhile(accounts_len_99,
                                       accounts_generator(token, org_id)), [])
    return accounts


