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

args = parser.parse_args()

sio = scaleio.ScaleIO("https://" + args.gwIPaddress + "/api",args.mdmUsername, args.mdmPassword, False, "ERROR") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST

print "\n\n--- ScaleIO System ---"
pprint(sio.system)
print "\n\n--- ScaleIO Gateway addresses ---"
print ("https://" + args.gwIPaddress)
