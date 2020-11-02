# FETCH AD USERS

### Create CSV with info about AD users

1. Get the userid info from AD:  
`users.txt`
2. Install python required packages:  
`pip install -r requirements.txt`
3. Run the `AD_Users.py` script:  
`python AD_Users.py -u AD_USERID -p AD_PASSWORD`
4. Check the `output` CSV file with details about AD users i.e. DISPLAYNAME, DEPARTMENT, USERID, MANAGERID.