![](/images/jFrog.JPG)

# Artifactory upgrade script

## Description

Python script for upgrading AF to the any specific latest versions.

## Usage
`pip3 install questionary`

`python3 AFupg.py` **or** `./AFupg.py`

`Note: Install the` ***questionary*** `module before running the script as mentioned above.`

## What does it do?

* Displays the current AF installed version.
* Checks for latest version availability, if YES then proceeds with upgrade process, else exit.
* Checks AF service state (Active/Inactive).
* If service is already in stopped state, continues further **or** if service is in active mode, stops the service before proceeding.
* Clears version lock for current package.
* Upgrades the AF package.
* Once the upgrade is completed successfully, puts version lock to upgraded package.
* Starts the AF service.
* Displays the current running Af package along with the version.
