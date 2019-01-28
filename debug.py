#!/usr/bin/env python

import api
import os


token = os.environ.get('ZOHO_DESK_API_TOKEN')
org_id = os.environ.get('ZOHO_DESK_API_ORG_ID')


if __name__ == '__main__':

    accounts = api.get_all_accounts(token=token, org_id=org_id)

    print(accounts)
