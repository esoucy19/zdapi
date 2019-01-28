import api


def test_get_organizations():
    r = api.get('organizations')
    assert r.status_code == 200
    assert api.org_id in r.text


def test_list_accounts():
    account = api.list_accounts(start=1, limit=1)[0]
    assert account['accountName']


def test_get_all_accounts():
    accounts = api.get_all_accounts()
    assert len(accounts) > 100
