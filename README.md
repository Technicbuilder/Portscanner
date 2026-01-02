# Portscanner

A basic TCP port scanner (simple imitation of what Nmap does)

---------------------------------------------------------------------------------------
Features:

-> Uses standard socket connections to determine status of port
-> Attempts to grab the banner from the service running on a port and displays it
-> If the service lookup fails, it will use socket.getservbyport
-> Makes use of mutithreading if user requests to scan > 500 ports
---------------------------------------------------------------------------------------
Upcoming features to implement:

-> Going to add UDP port scanning
-> Going to make results accessible from a json file
---------------------------------------------------------------------------------------
How to use:

scan (domain name/Ip address) -p (starting port)-(ending port)

example: scan google.com -p 1-1000
----------------------------------------------------------------------------------------
Other:

For ethical/Cybersecurity uses only
Anyone can use this I dont mind
I dont mind using AI to fix mistakes etc but I dont condone its use if you are going to
make it generate the whole thing for you - you should know what you made
-----------------------------------------------------------------------------------------


