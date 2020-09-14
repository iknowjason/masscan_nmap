### Step 1:  Run masscan with a greppable text output file
### Example:  sudo masscan 192.168.10.0/24 -p1-65535 -oG mscan.txt
### Note:  Make sure your output file name is 'mscan.txt'

## Step 2:  Run this script that takes the output from Masscan (file:  mscan.txt) and outputs a command you can use for nmap
### Example:  python3 script1.py
### Note:  The script will create 'scans.txt' to be used by nmap; This file will allow you to run one nmap command per line, with each host and the ports listening that were enumerated by masscan

## Step 3:  Run the command below which will loop through 'scans.txt' and run an nmap scan.  An output file will be created for each host:
### Command: while IFS=' ' read -r host ports; do sudo nmap -n -vvv $host $ports -sV -sC -oN $host.txt;done < scans.txt

hosts = {}
ports = "ports"

with open('mscan.txt') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('Host:'):

            ### split the line to parse it
            x = line.split(" ")
            ip_addr = x[1]

            ### Parse the port only if TCP and open
            if "open" in x[3] and "tcp" in x[3]:
                port_str = x[3].split('/')
                port = port_str[0]

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
                    #print("Port %s already exists" % port)
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
        port_str += p
        port_str += str(",")
    tmp_str = port_str[:-1]
    text_file.write(" %s\n" % tmp_str)
print("[+] Created %d scan lines in text file: 'scans.txt'" % hcount)
text_file.close()
### This is the command to run next:
### while IFS=' ' read -r host ports; do echo "[+] Scanning $host"; sudo nmap -n -vvv $host $ports -sV -sC -oN $host.txt;done < scans.txt
print("[+] Run the following command below to perform an nmap scan of each host with enumerated ports")
print("Command:  while IFS=' ' read -r host ports; do sudo nmap -n -vvv $host $ports -sV -sC -oN $host.txt;done < scans.txt")
