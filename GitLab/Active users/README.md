# GitLab Active Users

## Description

Provides the list of all the active users in GitLab.

## Usage

`python3 ActiveUsers.py`

## How to run the script?

- Provide your Private API token in `myToken` variable in the script.
- Run the script as per `Usage` section and two output file will be generated.

NOTE: Change to PROD url in the URL variable to get the active users list for PROD environment.

## What does it do?

- Checks for the active users in GitLab and gets the users list using API call along with all other required details.
- Script generates two output files, one file contains RAW data which is unsorted and might have duplicate entries, the other file contains the filtered data that needs to be considered for further needs.