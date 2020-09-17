## Overview:  These steps will help you automate masscan and nmap together.  Run masscan to enumerate all live hosts and listening ports.
### Then use nmap to run a more targeted service and NSE basic scripts scan.  This will ran against all hosts with all enumerated ports.
### So there might be extra port scans that run against hosts that don't have those listening ports.
### Important Note:  Tested on masscan 1.06 - There might be issues with older versions of masscan (i.e., 1.04) with JSON output

### Step 1:  Run masscan with a JSON output file
### Example:  sudo masscan 192.168.10.0/24 -p1-65535 -oJ mscan.xml
### Note:  Make sure you take note of your output file for next step

## Step 2:  Run this script that takes the output from Masscan JSON output file and outputs a command you can use for nmap
### Example:  python3 masscan_nmap1.py mscan.xml
### Note:  The script will create 'hosts.txt' to be used by nmap; It will also create a port list for you to pass command line

### Step 3: Run the nmap command.  When you run this script it will output the below with a custom command for the host list and ports.  Just copy and paste.
### Example: [+] Run this nmap command: <COPY AND PASTE THIS COMMAND>

import sys
import json
hosts = {}
ports = "ports"
host_list = []
port_list = []
port_list_str = "-p"
hcount = 0


with open('%s' % str(sys.argv[1])) as json_file:
    loaded_json = json.load(json_file)
    for x in loaded_json:
        ### Parse the port only if open (if you want TCP ports only - specify here)
        if x["ports"][0]["status"] == "open":
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

tmp_str = port_list_str[:-1]
# Output copy and paste port string
print ("[+] Port list string: %s" % tmp_str)

# Create hosts.txt file
text_file = open("hosts.txt", 'w')
for host in host_list:
    text_file.write("%s\n" % host)
text_file.close()
print ("[+] Wrote %d hosts to file: hosts.txt" % hcount)
print ("[+] Run this nmap command:  sudo nmap -n -vvv -Pn -sV -sC -iL hosts.txt %s -oA nmap_scan" % tmp_str)
