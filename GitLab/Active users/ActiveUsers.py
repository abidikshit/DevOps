import os
import requests
from requests.exceptions import HTTPError


try:
    # To remove the text file after every script run
    if os.path.exists("RawUsers.txt"):
        os.remove("RawUsers.txt")
        if os.path.exists("ActiveUsers.txt"):
            os.remove("ActiveUsers.txt")
    else:
        pass
    for i in range(1,4):
        url = "https://gitlab.com/api/v4/users?active=true&&per_page=100&page="+i

        # Give API token
        myToken = 'Provide API token here'
        head = {'Private-Token': myToken}

        # Get request with token
        r = requests.get(url, headers=head)
        data = r.json()
        # Storing raw output to a txt file
        for user in range(len(data)):
            with open('RawUsers.txt', 'a') as fh:
                print("{}".format(data[user]["username"]), file=fh)

        # Sorting alphabetically & removing duplicates from input file and storing in output file
        names = set()
        with open('RawUsers.txt') as f:
            for line in f:
                if line.strip():
                    names.add(line.strip())
        with open('ActiveUsers.txt', 'a') as fh:
            print('\n'.join(sorted(names)), file=fh)


except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
