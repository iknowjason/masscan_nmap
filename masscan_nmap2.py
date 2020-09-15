### Step 1:  Run masscan with a JSON output file
### Example:  sudo masscan 192.168.10.0/24 --rate 10000 -p1-65535 -oJ mscan.xml
### Note:  Make sure you take note of your output file for next step
### Important Note:  Tested on masscan 1.06 - There might be issues with older versions of masscan (i.e., 1.04) with JSON output

## Step 2:  Run this script that takes the output from Masscan JSON file and outputs a command you can use for nmap
### Example:  python3 masscan_nmap2.py mscan.xml 
### Note:  The script will create 'scans.txt' to be used by nmap; This file will allow you to run one nmap command per line, with each host and the ports listening that were enumerated by masscan

## Step 3:  Run the command below which will loop through 'scans.txt' and run an nmap scan.  An output file will be created for each host:
### Command: while IFS=' ' read -r host ports; do sudo nmap -n -vvv $host $ports -sV -sC -oN $host.txt;done < scans.txt

import sys
import json
hosts = {}
ports = "ports"

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

# Create host and port scan text file
text_file = open("scans.txt", 'w')

hcount = 0

for h in hosts:
    port_str = "-p"
    print("[+] Host: %s" % h)
    # Write the host
    text_file.write("%s" % h)
    hcount+=1
    for p in hosts[h]["ports"]:
        print("    [+] Port: %s" % p)
        blah = str(p)
        port_str += blah 
        port_str += str(",")
    tmp_str = port_str[:-1]
    text_file.write(" %s\n" % tmp_str)
print("[+] Created %d scan lines in text file: 'scans.txt'" % hcount)
text_file.close()
### This is the command to run next:
### while IFS=' ' read -r host ports; do echo "[+] Scanning $host"; sudo nmap -n -vvv $host $ports -sV -sC -oN $host.txt;done < scans.txt
print("[+] Run the following command below to perform an nmap scan of each host with enumerated ports")
print("Command:  while IFS=' ' read -r host ports; do sudo nmap -n -vvv $host $ports -sV -sC -oN $host.txt;done < scans.txt")
