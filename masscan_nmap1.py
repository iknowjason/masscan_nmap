## Overview:  These steps will help you automate masscan and nmap together.  Run masscan to enumerate all live hosts and listening ports.
### Then use nmap to run a more targeted service and NSE basic scripts scan.  This will ran against all hosts with all enumerated ports.
### So there might be extra port scans that run against hosts that don't have those listening ports.

### Step 1:  Run masscan with a greppable text output file
### Example:  sudo masscan 192.168.10.0/24 -p1-65535 -oG mscan.txt
### Note:  Make sure your output file name is 'mscan.txt'

## Step 2:  Run this script that takes the output from Masscan (file:  mscan.txt) and outputs a command you can use for nmap
### Example:  python3 script1.py
### Note:  The script will create 'hosts.txt' to be used by nmap; It will also create a port list for you to pass command line

### Step 3: Run the nmap command.  When you run this script it will output the below with a custom command for the host list and ports.  Just copy and paste.
### Example: [+] Run this nmap command: <COPY AND PASTE THIS COMMAND>

host_list = []
port_list = []
port_list_str = "-p"
hcount = 0

with open('mscan.txt') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('Host:'):

            ### split the line to parse it
            x = line.split(" ")

            ### Add hosts to list
            if(x[1] in host_list):
                pass
            else:
                host_list.append(x[1])
                hcount+=1

            ### Add ports to list
            ### Only add port if it's TCP and open
            if "open" in x[3] and "tcp" in x[3]:
                port_str = x[3].split('/')
                port = port_str[0]
                if port in port_list:
                    pass
                else:
                    port_list.append(port)

## Create a port list string
for i in port_list:
    port_list_str += i
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
