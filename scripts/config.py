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

sio.create_volume('testvol001', 81920, sio.get_pd_by_name('default'), sio.get_storage_pool_by_name('default'),enableMapAllSdcs=True)
