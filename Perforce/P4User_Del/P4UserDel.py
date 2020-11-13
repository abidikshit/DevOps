#!/p4/common/python/bin/python3
"""
AUTHOR: Abhilash Dikshit
DESCRIPTION: Perforce user deletion of inactive AD users
"""

import os
import subprocess

f_input = "InactiveUsers.txt"
f_output = "user_del.txt"
f_mid = "client.txt"
f_last = "opened.txt"


def del_operation():
    with open(f_input, 'r') as inactive_users:
        for userid in inactive_users:
            user = userid.strip()

            def p4user():
                print("-"*80)
                print("User id:", user)
                check_users = subprocess.Popen('p4 users | grep -w '+user, shell=True, stdout=subprocess.PIPE)
                status_check_user = check_users.communicate()[0]
                if status_check_user:
                    print("\n'"+user+"' exist in perforce database, checking authorisation method...")
                    auth_method()
                else:
                    print("\n'"+user+"' doesn't exist in perforce database.")

            def auth_method():
                check_auth = "p4 user -o " + user + " | tail -12 |grep -i ldap"
                auth = os.system(check_auth)
                if auth != 0:
                    print("\n'"+user+"' auth method is: 'PERFORCE', excluding...")
                else:
                    service_account()

            def service_account():
                check_service_account = "p4 groups -u "+user+"| egrep 'service_users|serviceaccounts|serviceperforce|serviceperforceread'"
                service_account_status = os.system(check_service_account)
                if service_account_status == 0:
                    print("\n'"+user+"' belongs to service account, excluding...")
                else:
                    print("\n'"+user+"' does not belongs to service account, checking for normal/super user...")
                    superuser()

            def superuser():
                check_superuser = "p4 protects -u " + user + " | grep 'super user'"
                check_superuser_status = os.system(check_superuser)
                if check_superuser_status == 0:
                    print("\n'"+user+"' is a Super user, excluding...")
                else:
                    print("\n'"+user+"' is a Normal user, continuing for deletion process...\n")
                    user_del()

            def user_del():
                check_deletion = "p4 user -df " + user
                os.system(check_deletion)
                check_user_del = subprocess.Popen('p4 users | grep -w ' + user, shell=True, stdout=subprocess.PIPE)
                user_status = check_user_del.communicate()[0]
                if user_status:
                    print("\n'" + user + "' deletion unsuccessful. Checking for shelved files...")
                    # print("\nTrying other methods...")
                    shelve_file()
                else:
                    # user deleted successfully
                    with open(f_output, "a") as fh:
                        print(user, file=fh)

            def shelve_file():
                check_shelve = subprocess.Popen('p4 changes -s pending -u '+user, shell=True, stdout=subprocess.PIPE)
                shelve = check_shelve.communicate()[0]
                if shelve:
                    print("\n'"+user+"' has shelved files, listing client workspace for deletion...")
                    workspace_del()
                else:
                    print("\n'"+user+"' has no shelved files, checking for opened files...")
                    check_open_files()

            def workspace_del():
                check_clients = "p4 changes -s pending -u "+user+" |awk {'print $6'}|cut -d '@' -f2 | awk '!x[$0]++'>"+f_mid
                os.system(check_clients)
                with open(f_mid, 'r') as fh:
                    for client in fh:
                        del_workspace = "p4 client -df -Fs "+client
                        os.system(del_workspace)

                remove_files()

                check_deletion = "p4 user -df " + user
                os.system(check_deletion)
                check_user_del = subprocess.Popen('p4 users | grep -w ' + user, shell=True, stdout=subprocess.PIPE)
                user_status = check_user_del.communicate()[0]
                if user_status:
                    check_open_files()
                else:
                    # user deleted successfully
                    with open(f_output, "a") as fh:
                        print(user, file=fh)

            def check_open_files():
                opened_file = subprocess.Popen('p4 -z maxScanRows=2000000 opened -u '+user, shell=True,
                                               stdout=subprocess.PIPE)
                status_opened = opened_file.communicate()[0]
                if status_opened:
                    print("\nDeleting opened files")
                    open_del = subprocess.Popen("p4 -z maxScanRows=2000000 opened -u" + user + "|cut -d '@' -f2 |awk {'print $1'}| awk '!x[$0]++' >"+ f_last, shell=True, stdout=subprocess.PIPE)
                    status_open_del = open_del.communicate()[0]
                    with open(f_last, 'r') as fh:
                        for i in fh:
                            del_open = subprocess.Popen("p4 client -df -Fs "+i, shell=True, stdout=subprocess.PIPE)
                            sts_del_open = del_open.communicate()[0]
                    user_del()
                else:
                    print("\nSkipping deletion of user"+user)
                    pass

            p4user()


def total_users():
    print("")
    print("*" * 60)
    print("summary".upper().center(60))
    print("*" * 60)
    count_input_user = subprocess.Popen("wc -l "+f_input+" |awk {'print $1'}", shell=True, stdout=subprocess.PIPE)
    status_count_input_user = count_input_user.communicate()[0]
    print("\nNo. of users provided: " + str(status_count_input_user.decode('utf-8').strip()))
    count_del_user = subprocess.Popen("wc -l "+f_output+"| awk {'print $1'}", shell=True, stdout=subprocess.PIPE)
    status_count_del_user = count_del_user.communicate()[0]
    print("\nNo. of users deleted: " + str(status_count_del_user.decode('utf-8').strip()))

    print("*" * 60)
    print("*" * 60)
    print("license count after user deletion".upper().center(60))
    print("*" * 60)
    license_count = "p4 license -u | sed -n '2,3p;4q' | awk {'print $2,$3'}"
    os.system(license_count)
    print("*" * 60)


def remove_files():
    if os.path.exists(f_mid):
        os.remove(f_mid)
    if os.path.exists(f_last):
        os.remove(f_last)
    else:
        pass


if os.path.exists(f_output):
    os.remove(f_output)
else:
    pass
del_operation()
total_users()
remove_files()
