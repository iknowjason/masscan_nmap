### Step 1:  Edit your masscan command in the variable line below, correctly specifying your hosts and ports.  You don't need to change the '-oJ mscan.xml' line as this is required.
masscan_command = "sudo masscan 192.168.7.0/24 --rate 20000 -p1-3000 -oG mscan.xml"
#Example masscan_command = "sudo masscan 192.168.7.0/24 --rate 20000 -p1-65535 -oG mscan.xml"
#Example masscan_command = "sudo masscan 192.168.7.0/24 -p1-65535 -oG mscan.xml"
### Note:  Make sure your output file name is 'mscan.txt'

### Step 2:  Run this script
### python3 masscan_nmap4.py

import os
import json
hosts = {}
ports = "ports"

### Run the masscan command
print("[+] Running the masscan enumeration:  %s" % masscan_command)
os.system(masscan_command)

with open('mscan.xml') as json_file:

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
cmds_list = []

for h in hosts:
    port_str = "-p"
    print("[+] Host: %s" % h)
    # Write the host
    text_file.write("%s" % h)
    hcount+=1
    tstring = h
    tstring += str(':-p')
    for p in hosts[h]["ports"]:
        blah = str(p)
        print("    [+] Port: %s" % blah)
        port_str += blah 
        port_str += str(",")
        tstring += blah 
        tstring += str(",")
    tmp_str = port_str[:-1]
    text_file.write(" %s\n" % tmp_str)

    tstring = tstring[:-1]
    cmds_list.append(tstring)
print("[+] Created %d scan lines in text file: 'scans.txt'" % hcount)
## save this file just for inspection
text_file.close()

### Loop through and run nmap command, running each scan against a single host with precise ports, and saving the file with IP address (i.e., <IP>.txt)
# Declare the nmap base command
nmap_base = "sudo nmap -n -vvv -sV -sC "
for cmd in cmds_list:
   #print("cmd: %s" % cmd)
   tmp1 = cmd.split(':')
   host = tmp1[0]
   ports = tmp1[1]
   #print("ports: %s" % ports)
   full_nmap_cmd = nmap_base + host + " " + ports + " " + "-oN " + host + ".txt"
   print("[+] Running nmap command: %s" % full_nmap_cmd)
   os.system(full_nmap_cmd)
