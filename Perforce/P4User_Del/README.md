# Perforce User Deletion

## Description

- Deletes the inactive AD users from perforce database.

## Usage

`python3 P4UserDel.py` **or** `./P4UserDel.py`

## How to run the script and its result!

* Make sure the below operations are done using `p4admin` account only.
* Copy script to the Perforce hosted linux machine.
* Create a text file using cmd `touch InactiveUsers.txt` in the same location.
* Copy and paste the inactive AD users list in above text file that was received from version.control mailbox (generated every Friday).
* Change the script permission using cmd `chmod +x P4UserDel.py`.
* Run the script using the cmd mentioned in the `Usage` section.
* Displays summary of provided users and deleted users along with license count in perforce and creates the list of users which are deleted in the text file `user_deleted.txt`.

## What does it do?

- Checks if the user is available is perforce database, if yes..
- Checks the user auth method. if LDAP, continues.
- Skips the respective users if it belongs to any of the service account "service_users|serviceaccounts|serviceperforce|serviceperforceread"and/or if is a super user.
- Try deleting the user, if it fails, checks for the shelved files.
- If shelved files are found, it deletes the user workspace without deleting the shelved files and then try's deleting the user again.
- Even after the above operation the deletion failed, it checks if the user has any opened files, if yes then it deletes the opened files and deletes the user.
- If it fails, it skips the respective user and continues for the next user.

NOTE: It stores the deleted user in the output file to cross check later if needed. 
