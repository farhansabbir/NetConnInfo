#!/usr/local/python277/bin/python
import subprocess, os, sys, time
if len(sys.argv) < 3:
	print("Usage: " + str(sys.argv[0]) + " <seconds_to_pause> <loop_times>")
	exit(1)
LOOPCOUNT=int(sys.argv[2])
SLEEPSEC = int(sys.argv[1])
if SLEEPSEC < 1 or SLEEPSEC > 20:
	print("Sleep time is too low or too high")
	exit(1)
PORTS=list()
for line in os.popen('netstat -an').readlines():
	sp = line.split()
 	if 'LISTEN' in sp[-1]:
  		PORTS.append("" + sp[3].split(':')[-1])


IPS=([line.split()[1].split('/')[0] for line in os.popen('/sbin/ip a').readlines() if "inet" in line])
MYLISTEN = list()
for IP in IPS:
 	for PORT in PORTS:
  		MYLISTEN.append(IP + ":" + PORT)

DATA = dict()

for i in range(LOOPCOUNT):
	p = subprocess.Popen(("netstat","-an"),stdout=subprocess.PIPE)
	ALLCONNS = [row.rstrip().split() for row in iter(p.stdout.readline,b'') if "tcp" in row.rstrip().split()[0] or "udp" in row.rstrip().split()[0]]
	for conn in ALLCONNS:
 		if 'LISTEN' not in conn[-1]:
  			if conn[3].split("ffff:")[-1] in MYLISTEN:
   				try:
    					INDEX = "IN," + conn[0] + "," + conn[4].split("ffff:")[-1].split(":")[-2] + "," + conn[3].split("ffff:")[-1]
    					DATA[INDEX] = int(DATA[INDEX]) + 1
   				except KeyError:
    					DATA[INDEX] = 1
  			else:
   				try:
    					INDEX = "OUT," + conn[0] + "," + conn[3].split(":")[0] + "," + conn[4]
    					DATA[INDEX] = int(DATA[INDEX]) + 1
   				except KeyError:
    					DATA[INDEX] = 1
	time.sleep(SLEEPSEC)

import platform
print("My hostname: " + platform.node())
print("My IP addresses: " + str(IPS))
for key in sorted(DATA):
 	print(key + "," + str(int(DATA[key])))
