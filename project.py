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
print('\n \033[1m\033[3m\033[5m' + '    Created by Nrchy and Co.' +  '\033[0m \n')

if sys.version_info[0] < 3:
    print("\nPython3 is needed to run Spyder, Try \"python3 project.py\" instead\n")
    sys.exit(2)

#examples for reference
example = "\nEXAMPLES: \n"
example += "-----------------------------------------------------------------------------------------------------------------------> \n" 
example += "spyder -s linkedin.com -d                    # Perform DNS resolution, WAF detection on the target \n"
example += "spyder -s facebook.com -bg                   # Banner grabbing on target \n"
example += "spyder -s ncdc.gov.in -e                     # Gather emails related to the domain \n"
example += "spyder -s facebook.com -e -bg -cs            # Run a simple recon scan, banner grabbing, email gathering, and CMS scan \n"
example += "-----------------------------------------------------------------------------------------------------------------------> \n"

#description about the CLI tool
parser = argparse.ArgumentParser(description='Passive Reconnaissance and OSINT-based Tool', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter)

#provide run time arguments (required and optional) for the tool to run

#mutually exclusive group title
group = parser.add_argument_group('Reconnaissance Options')
#target site name (required flag)
group.add_argument('-s', help='The target site or domain on which recon has to be performed', required=True)
#perform dns resolutions and waf detection
group.add_argument('-d', help='Performs normal scans like DNS resolution, WAF detection', action='store_true')
#banner grabbing on target (optional flag)
group.add_argument('-bg', help='Perform banner grabbing on the target', action='store_true')
#scan for cms on target (optional flag)
group.add_argument('-cs', help='Run a CMS scan on the website', action='store_true')
#google dork for emails (optional flag)
group.add_argument('-e', help='Use google dorking to gather any publicly available email ids related to the domain', action='store_true')

args = parser.parse_args()
site = ''
site = args.s
#ip=0
#ip=socket.gethostbyname(site)

#print the arguments that you provided during run time

if (args.d == False and args.bg == False and args.cs == False and args.e == False):
	print(colored('%sJust the name of the site is not enough, you will have to provide other options for reconnaissance!', 'red') % (attr('bold')))
	print('Try these:')
	print(parser.epilog)
else:
	#print the arguments that you provided during run time
	print('\n%s%sYour target site name: {}'.format(site) % (fg('blue'),attr('bold')))

if (args.d == True):
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
	print(colored('%s - PERFORM BASIC DNS RESOLUTIONS ON THE TARGET','green') % (attr('bold')))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#get ip address of the target
	ret=os.system('nslookup {}'.format(site))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#get spf, dmarc records
	ret=os.system('dig {} txt | grep "ANSWER SECTION" -A20'.format(site))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.bg == True): 
	print(colored('%s - PERFORM BANNER GRABBING, WAF DETECTION, CRAWL FOR SUBDOMAINS ON THE TARGET','green') % (attr('bold')))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
	
	#banner grabbing
	ret=os.system('curl -s -I {} '.format(site))
	ret=os.system('whatweb {}'.format(site))

	#WAF detection
	print('\n')
	ret=os.system('wafw00f -a -r {} | grep Checking -A20'.format(site))

	#find subdomains
	print('\n')
	ret=os.system('dmitry -s {} | grep Host -A20'.format(site))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.cs == True): 
	print(colored('%s - PERFORM A CMS SCAN ON THE TARGET','green') % (attr('bold')))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#run a cms scan on the website
	ret=os.system('python3 /root/Desktop/major1/CMSeeK/cmseek.py --url {} | grep [i] -A30'.format(site))
	#ret=os.system('cat /root/Desktop/major1/CMSeeK/cmseek.py')
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

if (args.e == True): 
	print(colored('%s - PERFORM EMAIL GATHERING USING GOOGLE DORKING','green') % (attr('bold')))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))

	#use google dorking to find any email ids that are publicly available
	ret=os.system('theharvester -d {} -l 50 -b google | grep found -A20'.format(site))
	print(colored('%s---------------------------------------------------------------------------------------------------------------------------------------------','yellow') % (attr('bold')))
