from ldap3 import Server, Connection, ALL
import os
import argparse
import json
import pandas as pd
import csv

"""
Get info about Perforce users
"""

# Argparse
parser = argparse.ArgumentParser(description='Get members of AD groups.')
parser.add_argument('--password', '-p', required=True, help='Global passord')
parser.add_argument('--user', '-u', required=True, help='Password for global user')
args = parser.parse_args()
ad_user = args.user
ad_password = args.password
#################################
ldapserver = 'ldap://'
ad_group_query = 'OU=,OU=,OU=,OU=SE,DC=global,DC=,DC=,DC='
basedn = 'DC=global,DC=,DC=,DC='
server = Server(ldapserver, get_info=ALL)
conn = Connection(server, ad_user, ad_password, auto_bind=True)
p4_users_raw = 'input/p4users.txt'
p4_users_details = 'output/p4_users_details.csv'
p4_users_per_dep = 'output/p4_users_per_dep.csv'

def parse_p4_users_file(userfile):
    """Parse the Perforce users file created by the 'p4users > p4users.txt' command

    Args:
        userfile (file): p4users file

    Returns:
        [list]: List with just userids
    """
    print(' # Parsing p4users file')
    p4_userids = []
    with open(p4_users_raw, newline = '') as p4_users:
            users_raw = csv.reader(p4_users, delimiter=' ')
            for user in users_raw:
                p4_userids.append(str(user).split()[0][1:].split(sep=',')[0].strip("'"))
    return p4_userids


def remove_none_ad_users(build_owner_list):
    """Takes a list of user ids and checks if they are found in AD

    Args:
        build_owner_list (list): List of users

    Returns:
        list: List of active AD users
    """
    print(' # Removing none AD users from users list')
    userlist = [x.lower() for x in build_owner_list]
    active = []
    for user in userlist:
        ldapsearchpath = f"(sAMAccountName={user})"
        conn.search(basedn, ldapsearchpath, attributes=['sAMAccountName'])
        for entry in conn.entries:
            active.append(str(entry.sAMAccountName).lower())
    inactive_users = set(userlist) - set(active)
    if len(inactive_users) == 0:
        print('All users active in AD')
    else:
        print('----------------------')
        print(f'Users not found in AD: {list(inactive_users)}')
        print(f'Number of none AD users: {len(list(inactive_users))}')
        print('----------------------')

    return list(active)


def users_details_to_csv(userlist):
    print(' # Creating perforce users details CSV')
    employees = []
    userlist = [x.lower() for x in userlist]
    for user in userlist:
        ldapsearchpath = f"(sAMAccountName={user})"
        conn.search(basedn, ldapsearchpath, attributes=['cn','displayName', 'department', 'sAMAccountName', 'manager'])
        for entry in conn.entries:
            employees.append({"displayname" : str(entry.displayName),"department" : str(entry.department).lower(),"userid" : str(entry.sAMAccountName).lower(),"manager" : str(entry.manager)[3:9].lower()})
    df = pd.DataFrame(employees)
    df.to_csv(p4_users_details, index=False)


def users_per_dep():
    """
    Create csv report with users per department
    """
    print(' # Creating perforce users per department CSV')
    df = pd.read_csv(p4_users_details)
    sortby_dep = df.groupby('department')['userid'].count().sort_values(ascending=False)
    sortby_dep.to_csv(p4_users_per_dep, header=['count'])



# Parse Perforce users list
p4_user_ids = parse_p4_users_file('p4users.txt')
# Removed inactive users from the list
active_users = remove_none_ad_users(p4_user_ids)
# Creating csv with some additional info
users_details_to_csv(active_users)
# Creating csv with users per dep
users_per_dep()

print(' ##### Check the "output" dir for csv files #####')