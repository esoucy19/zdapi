# zoho-desk-api
Scripts for getting some useful information out of Zoho Desk's API

# Listing accounts
Unfortunately, it seems like we don't have a native way with the API of
searching for a specific account by name. Rather, we first have to go through
all accounts, find the one we're looking for, then write down its id, and then
we can start searching for it directly.

This is made even more egregious by the fact that we can only list 99 accounts
at a time. We will thus have to loop through multiple api calls to get through
all existing accounts to finally get to the one we require.

That said, since accound ids practically never change, we can cache our results
locally and use our local cache for id lookups. Make sure we have some policy in
place for refreshing the cache too. Maybe refresh the cache every day?
