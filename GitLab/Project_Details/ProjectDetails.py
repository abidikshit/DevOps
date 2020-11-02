#!/usr/bin/env python3

import os
import requests
from requests.exceptions import HTTPError


def remove():
    # To remove the text file after every script run
    if os.path.exists("../../../GLProjectDet/PRODProjects.csv"):
        os.remove("../../../GLProjectDet/PRODProjects.csv")
    else:
        pass


try:
    remove()
    # Give API token
    myToken = 'GiveAPIToken'
    head = {'Private-Token': myToken}

    for i in range(1, 106):
        url = "https://gitlab.com/api/v4/projects?per_page=100&page="+str(i)

        # Get request with token
        r = requests.get(url, headers=head)
        data = r.json()
        for project in range(len(data)):
            with open('../../../GLProjectDet/PRODProjects.csv', 'a') as fh:
                # print(data[project]['id'], data[project]['name'], data[project]['owner']['username'], file=fh)
                print(data[project]['id'], data[project]['name'], data[project]['creator_id'], file=fh)

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
