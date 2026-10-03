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
        sys.exit(1)
    try:
        jdata = json.loads(release.text)
        version_name = jdata["tag_name"]
    except:
        print_log(2, "Unable to determine the latest Pi node version from Github: " + traceback.format_exc())
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
        sys.exit(1)
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
        sys.exit(1)
    print_log(0, "Extracting electron archive...")
    try:
        subprocess.run(["7za", "x", INSTALL_DIRECTORY + "/tmp/*.zip", "-o" +  INSTALL_DIRECTORY])
        subprocess.run(["rm", INSTALL_DIRECTORY + "/tmp/*.zip"])
        subprocess.run(["mv", INSTALL_DIRECTORY + "/electron", INSTALL_DIRECTORY + "/PiNetwork"])
    except:
        print_log(2, "Extraction subprocess failed. Is p7zip installed?")
        sys.exit(1)
    print_log(0, "Extracting Pi node binary...")
    try:
        subprocess.run(["7za", "x", INSTALL_DIRECTORY + "/tmp/*.exe", "-o" + INSTALL_DIRECTORY + "/tmp"])
        subprocess.run(["rm", "-r", INSTALL_DIRECTORY + "/resources"])
        subprocess.run(["mv", INSTALL_DIRECTORY + "/tmp/resources", INSTALL_DIRECTORY])
        subprocess.run(["rm", "-r", INSTALL_DIRECTORY + "/tmp"])
    except:
        print_log(2, "Extraction subprocess failed. Is p7zip installed?")
        sys.exit(1)
    print_log(0, "All done! Launch '" + INSTALL_DIRECTORY + "/PiNetwork --no-sandbox' with root privileges.")

install_pi_app()
            
    
