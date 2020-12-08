### Overview:  These steps will help you automate masscan and nmap together.  This script will do the following:
# 1.  Automatically run masscan to enumerate all live hosts and listening ports, with output to an XML file 
# 2.  Parse output XML file into live hosts (hosts.txt) and a normalized port string with all discovered ports 
#     Note:  there might be extra port scans that run against hosts that don't have those listening ports (since the port list string is normalized across all live hosts.  If you want exact ports for each host, look at scripts 3 and 4)
# 3.  Automatically run nmap command with parsed hosts and ports from masscan
# 4.  Output nmap scan with -oA nmap_scan 
# Important Note:  Tested on masscan 1.06 - Older versions (1.04, 1.05) will not work with JSON decoder 

# Author:  Jason Ostrom

# Dependencies:
# 1.  masscan 1.06
# 2.  nmap
# 3.  python3

# Step 1: Edit the masscan base command variable (MASSCAN_CMD) in the line below to include your scope for target IP addresses and ports 
# Optional:  Tune the rate (--rate).  Below 10,000 is used.  100 is the default, which is quite slow 
MASSCAN_CMD = "sudo masscan 192.168.1.0/24 --rate 10000 -p1-1000 -oJ mscan.xml" 
# Note:  Make sure you don't change the xml file output section (-oJ mscan.xml) as this is vital for the script to work 

# Step 2: Edit the nmap base command variable (NMAP_CMD) in the line below to include your preferred nmap options
# Note:  Don't touch HOSTS  and PORTS in the variable below ~ This is dynamically populated
# The script dynamically creates a normalized port list string, so you don't have to worry about the port list and IP addresses
NMAP_CMD = "sudo nmap -n -vvv -Pn -sV -sC HOSTS PORTS -oA nmap_scan"

# Step 3:  Run this script
# Example:  python3 masscan_nmap2.py
###

### import os
import os

### import sys
import sys

### import json
import json

## hosts dictionary
hosts = {}

## port string
ports = "ports"

## host list
host_list = []

## port list
port_list = []

## initial port string
port_list_str = "-p"

## a counter for number of discovered hosts
hcount = 0

### Run the masscan command
print("[+] Running the masscan enumeration:  %s" % MASSCAN_CMD)
os.system(MASSCAN_CMD)

### get filesize of 'mscan.xml'
filesize = os.path.getsize("mscan.xml")

### if the filesize is 0, exit (no data discovered) 
if filesize == 0:
    print ("[-] mscan.xml file is 0 bytes ~ (No discovered data)")
    print ("    [-] Going to exit")
    sys.exit()

### open the mscan.xml file created from masscan
with open("mscan.xml") as json_file:

    ### load json
    loaded_json = json.load(json_file)

    ### loop through json
    for x in loaded_json:

        ### Parse the port only if open (if you want TCP ports only - specify here)
        if x["ports"][0]["status"] == "open":

            ### add the port to this data structure
            port = x["ports"][0]["port"]

            ip_addr = x["ip"]
            ### Add the IP address to dictionary if it doesn't already exist
            try:
                hosts[ip_addr]
            except KeyError:
                hosts[ip_addr] = {}

            ### Add the port list to dictionary if it doesn't already exist
            try:
                hosts[ip_addr][ports]
            except KeyError:
                hosts[ip_addr][ports] = []

            ## append the port to the list
            if port in hosts[ip_addr][ports]:
                pass
            else:
                hosts[ip_addr][ports].append(port)
                print("[+] Appending port: %s" % port)
                port_list.append(port)

### loop through and append the host to the hosts list 
for h in hosts:
    print("[+] Appending host: %s" % h)
    host_list.append(h)
    hcount+=1

## remove duplicate ports in list for combined ports
port_list = list(dict.fromkeys(port_list))

## Create a port list string
for i in port_list: 
    print("[+] Listing port in string: %s" % i)
    portstring = str(i) 
    port_list_str += portstring 
    port_list_str += str(",")

### modify the port list string to remove last ',' character
tmp_str = port_list_str[:-1]

# Output copy and paste port string
print ("[+] Port list string: %s" % tmp_str)

# Create hosts.txt file
text_file = open("hosts.txt", 'w')
for host in host_list:
    text_file.write("%s\n" % host)
text_file.close()
### finished creating hosts.txt file

## print informational
print ("[+] Wrote %d hosts to file: hosts.txt" % hcount)

### Build the new nmap command string, replacing HOST
nmap_tmp_str = NMAP_CMD.replace("HOSTS", "-iL hosts.txt")

### Build the new nmap command string, replacing PORTS 
nmap_final_cmd = nmap_tmp_str.replace("PORTS", tmp_str)

### Print final command before running it
print ("[+] Runing this nmap command:  %s" % nmap_final_cmd)

### Run final command
os.system(nmap_final_cmd)
