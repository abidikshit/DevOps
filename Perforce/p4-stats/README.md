# P4 Stats

### Create CSV with info about Perforce users

1. Get the Perforce users info (requires Perforce Superuser access):  
`p4 users > input/p4users.txt`
1. Install python required packages:  
`pip install -r requirements.txt`
1. Run the `parse_p4_users.py` script:  
`python parse_p4_users.py -u AD_USERID -p AD_PASSWORD`
1. Check the `output` folder for the CSVs with details about Perforce users.