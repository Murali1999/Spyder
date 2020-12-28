#!/usr/bin/env python3

import argparse
import socket
from subprocess import call
import sys
import os
import re
from termcolor import colored
from colored import fg, bg, attr

#ascii banner for the CLI tool
ret=os.system('figlet -f slant Spyder')
print('\n \033[1m\033[3m' + '    Created by Nrchy and Co.' +  '\033[0m \n')

if sys.version_info[0] < 3:
    print("Python3 is needed to run Spyder, Try \"python3 project.py\" instead\n")
    sys.exit(2)

#examples for reference
example = "\nEXAMPLES: \n"
example += "----------------------------------------------------------------------------------------------------------------------------> \n" 
example += "spyder -s linkedin.com -d                    # Perform DNS lookup and find SPF records if any, on the target \n"
example += "spyder -s facebook.com -bg                   # Banner grabbing, WAF detection, crawl for subdomains on the target \n"
example += "spyder -s ncdc.gov.in -e                     # Use Google dorking and OSINT to gather publicly emails related to the domain \n"
example += "spyder -s facebook.com -bg -cs               # Run a scan for banner grabbing and a CMS scan \n"
example += "spyder -s linkedin.com -xs                   # Run an XSS vulnerability scan on the target \n"
example += "spyder -s barc.gov.in -b                     # Run a directory bruteforcing attack on the target \n"
example += "spyder -s linkedin.com -pscan                # Run a fast port scanner on the target \n"
example += "You can even add https:// or http:// to the target site \n"
example += "----------------------------------------------------------------------------------------------------------------------------> \n"

#description about the CLI tool
parser = argparse.ArgumentParser(description='Passive & Active Reconnaissance and OSINT-based Tool', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter)

#provide run time arguments (required and optional) for the tool to run

#mutually exclusive group title
group1 = parser.add_argument_group('Passive Reconnaissance Options')
#target site name (required flag)
group1.add_argument('-s', help='The target site or domain on which recon has to be performed', required=True)
#perform dns resolutions and waf detection
group1.add_argument('-d', help='Perform DNS lookup and find SPF records if available on the target', action='store_true')
#banner grabbing on target (optional flag)
group1.add_argument('-bg', help='Perform banner grabbing, WAF detection, and find subdomains if any on the target', action='store_true')
#scan for cms on target (optional flag)
group1.add_argument('-cs', help='Run a CMS scan on the website', action='store_true')
#google dork for emails (optional flag)
group1.add_argument('-e', help='Use google dorking to gather any publicly available email ids related to the domain', action='store_true')
#full dns agressive scan for all dns records
group1.add_argument('-fd', help='A full DNS scan for all DNS records available on the target', action='store_true')
#check for load balancers
group1.add_argument('-lb', help='Check if the target site has load balancers', action='store_true')

#mutually exclusive group title
group2 = parser.add_argument_group('Active/Aggressive Reconnaissance Options')
#directory brutefocing
group2.add_argument('-b', help='Brute force directory listings on the target', action='store_true')
#vulnerability scanning
group2.add_argument('-vscan',help='Initiate vulnerability scanning on the target', action='store_true')
#extensive google dorking
group2.add_argument('-lf', help='Find any links on the target that could be potential endpoints for attack', action='store_true')
#xss vulnerability scanning on the target
group2.add_argument('-xs', help='Start an XSS vulnerability scan on the target', action='store_true')
#run a fast port scanner on the target
group2.add_argument('-pscan',help='Run a fast port scanner on the target', action='store_true')
#ssl vulnerability analyser
group2.add_argument('-ssl',help='Run a scanner to find SSL related vulnerabilities',action='store_true')

args = parser.parse_args()
site = ''
site = args.s
httpssite='https://'+site
httpsite='http://'+site
ip=0
ip=socket.gethostbyname(site)

#print the arguments that you provided during run time
#separate if statements for active and passive scanning options

if (args.d == False and args.bg == False and args.cs == False and args.e == False and args.fd == False and args.lb == False and args.b == False and args.vscan == False and args.xs == False and args.lf == False and args.pscan == False and args.ssl == False):
	print(colored('%sJust the name of the site is not enough, you will have to provide other options for reconnaissance!', 'red') % (attr('bold')))
	print('Try these:')
	print(parser.epilog)
else:
	#print the arguments that you provided during run time
	print('%s%sYour target site name: {} \n'.format(site) % (fg('blue'),attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

#passive recon options

if (args.d == True):
	print(colored('%s - PERFORM BASIC DNS LOOKUP, FIND SPF/DMARC RECORDS ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#do a DNS lookup on the target
	ret=os.system('nslookup {}'.format(site))

	#get spf, dmarc records
	ret=os.system('dig +noall +answer +multiline txt {}'.format(site))
	print()
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.bg == True): 
	print(colored('%s - PERFORM BANNER GRABBING, WAF DETECTION, CRAWL FOR SUBDOMAINS ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
	
	#banner grabbing
	ret=os.system('curl -s -I {} '.format(site))
	ret=os.system('whatweb {}'.format(site))

	#WAF detection
	print('\n')
	ret=os.system('wafw00f -a -r {} | grep Checking -A20'.format(site))

	#find subdomains
	print('\n')
	ret=os.system('dmitry -s {} | grep Host -A20'.format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
	print()
	ret=os.system('python3 /root/Desktop/major1/Sublist3r/sublist3r.py -d {} | grep Enumerating -A100'.format(site))
	print()
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.cs == True): 
	print(colored('%s - PERFORM A CMS SCAN ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#run a cms scan on the website
	ret=os.system('python3 /root/Desktop/major1/cms-detector.py -s {}'.format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.e == True): 
	print(colored('%s - PERFORM EMAIL GATHERING USING GOOGLE DORKING AND OSINT','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#use google dorking to find any email ids that are publicly available
	ret=os.system('theharvester -d {} -l 50 -b google | grep found -A20'.format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
	print()
	ret=os.system('python3 /root/Desktop/major1/infoga/infoga.py -d {} -s all'.format(site))
	print()
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
	
if (args.fd == True):
	print(colored('%s - FULL DNS SCAN FOR ALL DNS RECORDS AVAILABLE ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#dig to find all dns records on the target
	ret=os.system('dig @8.8.8.8 +nocmd {} any +multiline +noall +answer'. format(site))
	print()
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.lb == True):
	print(colored('%s - CHECK FOR LOAD BALANCERS ON THE TARGET SITE','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#check for load balancers (software or hardware) on the target
	ret=os.system('lbd {} | grep Checking -A10'. format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

#active recon options

if (args.b == True):
	print(colored('%s - RUN A DIRECTORY BRUTEFORCING ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#bruteforce the directory listing of the target
	ret=os.system('gobuster dir -e -u {} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 60'. format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.vscan == True):
	print(colored('%s - RUN AN AGGRESSIVE SCAN ON THE TARGET TO FIND ANY ATTACK SURFACES AND OTHER VULNERABILITIES','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#run a vulnerability scan on the target using striker
	ret=os.system('python3 /root/Desktop/major1/Striker/striker.py {}'. format(site))
	
	#run a golismero scan on the target
	ret=os.system('golismero scan {}'.format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.lf == True):
	print(colored('%s - FIND LINKS WHICH COULD BE POTENTIAL ENDPOINTS FOR ATTACKS','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#find for links from the code written for the implementation of the site, to find any endpoints for attacks
	ret=os.system('python /root/Desktop/major1/LinkFinder/linkfinder.py -i {} -o cli'. format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.xs == True):
	print(colored('%s - RUN AN XSS VULNERABILITY SCANNING ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#run an explicit vulnerability scan for XSS on the target
	ret=os.system('python /root/Desktop/major1/XssPy/XssPy.py -u {} | grep Doing -A30'. format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.pscan == True):
	print(colored('%s - RUN A FAST PORT SCANNER ON THE TARGET','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#run a fast port scanner on thet target
	ret=os.system('nmap -sC -sV -Pn -O -T4 {} -vv'. format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.ssl == True):
	print(colored('%s - RUN A SCAN TO FIND SSL RELATED VULNERABILITIES','green') % (attr('bold')))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#run an ssl vulnerability analyser
	ret=os.system('sslyze --regular {}'. format(site))
	print(colored('%s--------------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
