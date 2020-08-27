from termcolor import colored
import os
import subprocess
import json
import cgi

#Ensure that the user has the required requests dependency
try:
    #attempt to import requests
    import requests
except Exception as e:
    print(colored("ERROR!", 'yellow'))
    print(colored(e, 'red'))
    print("Error, Module 'requests' is required, connect device to the internet and run 'pip3 install requests', attempting to automatically retrieve...")
    #if importing requsts fails, try to install it via pip over command line
    try:
        os.system("pip3 install requests")
        print(colored("install succesful, rereun program to launch", 'green'))
    except Exception as e:
        #if pip fails, user likely isn;t connected to the internet, or doesn't have pip, or is just beyond help
        print(colored("ERROR!", 'yellow'))
        print(colored(e, 'red'))
        print("pip install failed, are you connected to the internet?, try running this script with root/admin privelages")

#global variables
req = None
sessionID = None
user = "fcta"
passwd = "Mandrake488!"
machines = []

#cool banner because why not
banner = ("____   _________      _____         .__        __         .__        \n"
          "\   \ /   /     \    /     \ _____  |__| _____/  |______  |__| ____  \n"
          " \   Y   /  \ /  \  /  \ /  \\__  \ |  |/    \   __\__  \ |  |/    \ \n"
          "  \     /    Y    \/    Y    \/ __ \|  |   |  \  |  / __ \|  |   |  \\\n"
          "   \___/\____|__  /\____|__  (____  /__|___|  /__| (____  /__|___|  /\n"
          "                \/         \/     \/        \/          \/        \/  \n"
          "V 0.1 Alpha\n"
          "By:\n"
          "+-+-+-+ +-+-+-+-+-+-+-+\n"
          "|S|l|t| |R|o|d|g|e|r|s|\n"
          "+-+-+-+ +-+-+-+-+-+-+-+\n"
          "This software is UNCLASS//FOUO\n")

print(colored(banner, 'yellow'))
print(colored('#################################################################################', 'green'))

#Sets up the connection to the vmrest.exe API


def SessionInit():
    '''Sets up the connection to the vmrest.exe API'''
    global req
    #attempt to connect to vmrest on it's default port (assumes local host, at the time of writing there is no reason to do this remotely, hence the use of plaintext passwords and lack of SSL)
    try:
        req = requests.get("http://127.0.0.1:8697/api/vms",
                           auth=(user, passwd))
        GetVMs(req)
    except Exception as e:
        print(colored("ERROR!", 'yellow'))
        print(colored(e, 'red'))
        print(colored("connection to VMWare REST API Failed, attempting to resolve... launching 'C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrest.exe...", 'yellow'))
        try:
            proc = subprocess.Popen(
                'C:\\Program Files (x86)\\VMware\\VMware Workstation\\vmrest.exe')
        except Exception as e:
            print(colored("ERROR!", 'yellow'))
            print(colored(e, 'red'))
            print(colored("Execution of vmrest.exe failed, terminating. Is VMware up to date? and is the path to vmrest.exe in this scipt correct? do the credentials match those in the script? (if not, run vmrest.exe -C and update credentials)", 'red'))
        try:
            req = requests.get("http://127.0.0.1:8697/api/vms",
                               auth=(user, passwd))
            GetVMs(req)
        except Exception as e:
            print(colored("ERROR!", 'yellow'))
            print(colored(e, 'red'))
            print("an error occurred, terminating")

#Assuming the connection to the rest API was successful, this function updates/maintains the list of VMs on the host


def GetVMs(r):
    '''Assuming the connection to the rest API was successful, this function updates/maintains the list of VMs on the host'''
    global machines
    #if successful, (ie, code 200), update the current list of VM's
    if r:
        print(colored('************************************CONNECTION TO VMWARE API... SUCCESSFUL!!!************************************', 'green'))
        data = r.json()
        for vms in data:
            machines.append(vms)
        ActiveSession()

    #if unsuccessful, print error message
    else:
        print(colored('************************************CONNECTION TO VMWARE API... FAILED!!!************************************', 'red'))
        print(b"from server: " + r.content)
        print("probably a bad request")

#This function is intended for managing the active session and issueing commands to VM's, this is the programs core loop
def ActiveSession():
    '''This function is intended for managing the active session and issueing commands to VM's, this is the programs core loop'''
    global machines
    global req
    count = 0
    while True:
        print("Select VM(s) from the list below:\n")
        for i, vms in enumerate(machines):
            count += 1
            print(str(i+1) + ". " + vms["path"])
        print(str(count) + ". All")
        response = int(input("choose a number: "), 10)


if __name__ == "__main__":
    SessionInit()
