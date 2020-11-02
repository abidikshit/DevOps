"""
AUTHOR: Abhilash Dikshit
PUBLISHER: Abhilash Dikshit
VERSION: 1.0
DESCRIPTION: FIND AD USERS PROPERTIES
"""

from ldap3 import Server, Connection, ALL
import argparse
import pandas as pd

# Get info about AD users
# Argparse
parser = argparse.ArgumentParser(description='Get members of Scania AD groups.')
parser.add_argument('--password', '-p', required=True, help='Global Scania passord')
parser.add_argument('--user', '-u', required=True, help='Password for global Scania user')
args = parser.parse_args()
ad_user = args.user
ad_password = args.password
#################################
ldapserver = 'ldap://ldapse01.scania.com:389'
ad_group_query = 'OU=Groups,OU=InfoMate,OU=Sodertalje,OU=SE,DC=global,DC=scd,DC=scania,DC=com'
basedn = 'DC=global,DC=scd,DC=scania,DC=com'
server = Server(ldapserver, get_info=ALL)
conn = Connection(server, ad_user, ad_password, auto_bind=True)
AD_users_raw = 'users.txt'
AD_users_details = 'user_details.csv'


def parse_AD_users_file(userfile):
    """Parse the AD users provided in the input file 'users.txt'
    Args:
        userfile (file): users file
    Returns:
        [list]: List with just userids"""
    print('* Parsing users input file...'.upper())
    AD_userids = []
    with open(AD_users_raw, newline='') as AD_users:
        for user in AD_users:
            AD_userids.append(str(user).strip().split(sep=',')[0].strip("'"))
    return AD_userids


def remove_none_ad_users(build_owner_list):
    """Takes a list of user ids and checks if they are found in AD
    Args:
        build_owner_list (list): List of users
    Returns:
        list: List of active AD users"""
    print('* Removing none AD users from users list...'.upper())
    userlist = [x.lower() for x in build_owner_list]
    active = []
    for user in userlist:
        ldapsearchpath = f"(sAMAccountName={user})"
        conn.search(basedn, ldapsearchpath, attributes=['sAMAccountName'])
        for entry in conn.entries:
            active.append(str(entry.sAMAccountName).lower())
    inactive_users = set(userlist) - set(active)
    if len(inactive_users) == 0:
        print('\nAll users active in AD'.upper())
    else:
        print('-'*30)
        print(f'\nUsers not found in AD: {list(inactive_users)}'.upper())
        print(f'\nNumber of none AD users: {len(list(inactive_users))}'.upper())
        print('-'*30)

    return list(active)


def users_details_to_csv(userlist):
    print('* Creating AD users details to CSV file...'.upper())
    employees = []
    userlist = [x.lower() for x in userlist]
    for user in userlist:
        ldapsearchpath = f"(sAMAccountName={user})"
        conn.search(basedn, ldapsearchpath, attributes=['cn', 'displayName', 'department', 'sAMAccountName', 'manager'])
        for entry in conn.entries:
            employees.append({"DISPLAYNAME": str(entry.displayName), "DEPARTMENT": str(entry.department).lower(),
                              "USERID": str(entry.sAMAccountName).lower(), "MANAGERID": str(entry.manager)[3:9].lower()})
    df = pd.DataFrame(employees)
    df.to_csv(AD_users_details, index=False)


# Parse AD users list
AD_user_ids = parse_AD_users_file(AD_users_raw)
# Removed inactive users from the list
active_users = remove_none_ad_users(AD_user_ids)
# Creating csv with some additional info
users_details_to_csv(active_users)

print('* CHECK THE "'+AD_users_details+'" FILE')
