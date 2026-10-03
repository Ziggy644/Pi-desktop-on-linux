import json
import subprocess
import requests
from colorama import Fore
import datetime
import sys
import traceback
import os

def print_log(t,m):
    if t == 0:
    	print(Fore.WHITE + "[" + Fore.BLUE + str(datetime.datetime.now()) + Fore.WHITE + "][" + Fore.GREEN + "INFO" + Fore.WHITE + "] " + m)
    elif t == 1:
        print(Fore.WHITE + "[" + Fore.BLUE + str(datetime.datetime.now()) + Fore.WHITE + "][" + Fore.YELLOW + "WARNING" + Fore.WHITE + "] " + m)
    elif t == 2:
        print(Fore.WHITE + "[" + Fore.BLUE + str(datetime.datetime.now()) + Fore.WHITE + "][" + Fore.RED + "ERROR" + Fore.WHITE + "] " + m)

def find_pi_version(vs):
    result = ""
    for v in vs:
        if v["browser_download_url"][-3:] == "exe":
            result = v["browser_download_url"]
            break
    return result

def find_electron_version(vs):
    result = ""
    for v in vs:
        if v["browser_download_url"].find("linux-x64.zip") > -1 and v["browser_download_url"].find("electron-") > -1:
            result = v["browser_download_url"]
            break
    return result

def install_pi_app():
    INSTALL_DIRECTORY = "./Pi"
    if os.path.exists(INSTALL_DIRECTORY) == False:
        print_log(1, "Working directory doesn't exist. Creating...")
        subprocess.run(["mkdir", INSTALL_DIRECTORY])
    if os.path.exists(INSTALL_DIRECTORY + "/tmp") == False:
        print_log(1, "Download directory doesn't exist. Creating...")
        subprocess.run(["mkdir", INSTALL_DIRECTORY + "/tmp"])
    print_log(0, "Fetching Pi node release metadata...")
    try:
        release = requests.get("https://api.github.com/repos/pi-node/pi-node/releases/latest")
    except:
        print_log(2, "Unable to fetch Pi node release metadata from Github: " + traceback.format_exc())
        raise SystemExit(1)
    try:
        jdata = json.loads(release.text)
        version_name = jdata["tag_name"]
        if os.path.exists(INSTALL_DIRECTORY + "/current_version.txt") == True:
            current_version_file = open(INSTALL_DIRECTORY + "/current_version.txt", "r")
            current_version = current_version_file.read()
            current_version_file.close()
            if current_version.strip() == version_name:
                print_log(0, "Your Pi node version is up-to-date.")
                raise SystemExit(0)
            else:
                print_log(0, "Your Pi node needs to be updated.")
                current_version_file = open(INSTALL_DIRECTORY + "/current_version.txt", "w")
                current_version_file.write(version_name)
                current_version_file.close()
        else:
            print_log(0, "Your Pi node needs to be updated.")
            current_version_file = open(INSTALL_DIRECTORY + "/current_version.txt", "w")
            current_version_file.write(version_name)
            current_version_file.close()
    except Exception as e:
        exception_type = type(e).__name__
        if exception_type == "SystemExit":
            raise SystemExit(0)
        else:
            print_log(2, "Unable to determine the latest Pi node version from Github.")
            raise SystemExit(1)
    try:
        download_url = find_pi_version(jdata["assets"])
        if download_url == "":
            raise ValueError("No windows version in this release.")
        else:
            print_log(0, "Downloading latest Pi node release...")
            subprocess.run(["wget", "-P", INSTALL_DIRECTORY + "/tmp", download_url])
    except:
        print_log(2, "Unable to download Pi node release file.")
    try:
        release = requests.get("https://api.github.com/repos/electron/electron/releases/latest")
    except:
        print_log(2, "Unable to fetch electron release metadata from Github")
        raise SystemExit(1)
    try:
        jdata = json.loads(release.text)
        download_url = find_electron_version(jdata["assets"])
        if download_url == "":
            raise ValueError("Latest electron release not found")
        else:
            print_log(0, "Downloading latest electron release...")
            subprocess.run(["wget", "-P", INSTALL_DIRECTORY + "/tmp", download_url])
    except:
        print_log(2, "Unable to download electron release file.")
        raise SystemExit(1)
    print_log(0, "Extracting electron archive...")
    try:
        subprocess.run(["7za", "x", INSTALL_DIRECTORY + "/tmp/*.zip", "-o" +  INSTALL_DIRECTORY])
        subprocess.run(["rm", INSTALL_DIRECTORY + "/tmp/*.zip"])
        subprocess.run(["mv", INSTALL_DIRECTORY + "/electron", INSTALL_DIRECTORY + "/PiNetwork"])
    except:
        print_log(2, "Extraction subprocess failed. Is p7zip installed?")
        raise SystemExit(1)
    print_log(0, "Extracting Pi node binary...")
    try:
        subprocess.run(["7za", "x", INSTALL_DIRECTORY + "/tmp/*.exe", "-o" + INSTALL_DIRECTORY + "/tmp"])
        subprocess.run(["rm", "-r", INSTALL_DIRECTORY + "/resources"])
        subprocess.run(["mv", INSTALL_DIRECTORY + "/tmp/resources", INSTALL_DIRECTORY])
        subprocess.run(["rm", "-r", INSTALL_DIRECTORY + "/tmp"])
    except:
        print_log(2, "Extraction subprocess failed. Is p7zip installed?")
        raise SystemExit(1)
    print_log(0, "All done! Launch '" + INSTALL_DIRECTORY + "/PiNetwork --no-sandbox' with root privileges.")

install_pi_app()
            
    
