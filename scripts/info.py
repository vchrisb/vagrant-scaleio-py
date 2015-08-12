#!/usr/bin/env python

from scaleiopy import scaleio
from pprint import pprint
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mdmUsername", metavar='USERNAME', required=True, help="Username for ScaleIO GW")
parser.add_argument("--mdmPassword", metavar='PASSWORD', required=True, help="Password for ScaleIO GW")
parser.add_argument("--gwIPaddress", metavar='IP', required=True, help="IP address for ScaleIO GW")
parser.add_argument("--mdm1IPaddress", metavar='IP', required=True, help="IP address for ScaleIO MDM1")
parser.add_argument("--mdm2IPaddress", metavar='IP', required=True, help="IP address for ScaleIO MDM2")

args = parser.parse_args()

sio = scaleio.ScaleIO("https://" + args.gwIPaddress + "/api",args.mdmUsername, args.mdmPassword, False, "ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST

print "{}{}".format("--- Current ScaleIO API version is: ", sio.get_api_version())
print "\n\n--- ScaleIO System ---"
pprint(sio.system)
print "\n\n--- ScaleIO SDC ---"
pprint(sio.sdc)
print "\n\n--- ScaleIO SDS ---"
pprint(sio.sds)
print  "\n\n--- ScaleiO Volumes ---"
pprint(sio.volumes)
print "\n\n--- ScaleIO Protection Domains ---"
pprint(sio.protection_domains)
print "\n\n--- ScaleIO Fault Sets ---"
pprint(sio.fault_sets)
print "\n\n--- ScaleIO IP addresses ---"
print ("Gateway: " + args.gwIPaddress)
print ("MDM1: " + args.mdm1IPaddress)
print ("MDM2: " + args.mdm2IPaddress)
