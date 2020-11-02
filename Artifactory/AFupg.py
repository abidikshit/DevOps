#!/usr/bin/python3

"""
AUTHOR: Abhilash Dikshit
PUBLISHER: Abhilash Dikshit
VERSION: 1.0
DESCRIPTION: Upgrading jfrog artifactory to latest version
"""

import os
import subprocess
import questionary

file1 = "ver.txt"
file2 = "upg.txt"


def artifactory_package():
    os.system("rpm -qa | grep -i artifactory")


def version_lock_clear():
    print("\nclearing version lock...".upper())
    sts_ver_lock = subprocess.call("yum versionlock clear jfrog-artifactory-pro-* && yum versionlock list", shell=True,
                                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if sts_ver_lock == 0:
        print("\nVersion lock cleared.".upper())
    else:
        print("\nFailed to clear version lock".upper())


def version_lock_package():
    print("\nversion lock status... ".upper())
    os.system("yum versionlock jfrog-artifactory-pro-*")


def serv_start():
    print("\nstarting af service...".upper())
    os.system("systemctl start artifactory && sudo systemctl status artifactory")


def serv_stop():
    os.system("systemctl stop artifactory && systemctl status artifactory")


def serv_check():
    serv_check_status = os.system("systemctl is-active --quiet artifactory")
    if serv_check_status == 0:
        print("\nStopping af service..".upper())
        serv_stop()
        version_lock_clear()
        choose_input()
        version_lock_package()
        serv_start()
        print("\nAf package after upgrading...".upper())
        artifactory_package()
        print("*" * 100)
        print("*", " " * 38, "AF UPGRADE COMPLETED", " " * 38, "*")
        print("*" * 100)

    else:
        print("\nAf service is already in stopped state, continuing with upgrade steps...".upper())
        version_lock_clear()
        choose_input()
        version_lock_package()
        serv_start()
        print("\nAf package after upgrading...".upper())
        artifactory_package()
        print("*" * 100)
        print("*", " " * 38, "AF UPGRADE COMPLETED", " " * 38, "*")
        print("*" * 100)


def package_check():
    # Gets af installed version
    crnt_pkg = subprocess.call("yum --showduplicates list jfrog-artifactory-pro.x* |grep -A1 -i 'Installed'|sed '1d'|"
                               "awk {'print $2'} >"+file1, shell=True, stderr=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL)
    ver_pkg = open(file1).read().strip()
    print("\nINSTALLED VERSION: ", ver_pkg)

    # Gets upgraded version packages
    latest_pkg = subprocess.call("yum --showduplicates list jfrog-artifactory-pro.x*|sed -n '/Available/,$p'|sed '1d'|"
                                 "sed -n '/"+ver_pkg+"/,$p'|sed '1d'", shell=True, stderr=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL)

    if latest_pkg == 0:
        print("\nLatest packages available? Yes".upper())
        pkg = subprocess.call("yum --showduplicates list jfrog-artifactory-pro.x* |sed -n '/Available/,$p'|sed '1d'|"
                              "sed -n '/"+ver_pkg+"/,$p'|sed '1d'|awk {'print $2'} >"+file2, shell=True,
                              stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        serv_check()
    else:
        exit("\nLatest packages available? No".upper())


def choose_input():
    with open(file2, 'r') as f:
        versions = [line.strip() for line in f]
    af_version = questionary.select("\nSELECT VERSION TO BE UPGRADED TO: ", choices=versions).ask()
    # print(f'\nVERSION SELECTED: {af_version}')
    print("\nstarting upgrade process for artifactory...".upper())
    begin_upg = "yum install -y jfrog-artifactory-pro-" + af_version + ".x86_64"
    os.system(begin_upg)


def remove_files():
    if os.path.exists(file1):
        os.remove(file1)
        if os.path.exists(file2):
            os.remove(file2)
        else:
            pass
    else:
        pass


print("*" * 100)
print("*", " " * 38, "AF VERSION UPGRADE", " " * 38, "*")
print("*" * 100)
package_check()
remove_files()
