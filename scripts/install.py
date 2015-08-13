#!/usr/bin/env python

from scaleiopy import im
from scaleiopy import scaleioobject as sioobj
#from scaleio import installerfsm as instfsm
import time
import json
from pprint import pprint

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nodeUsername", metavar='USERNAME', required=True, help="Username for ScaleIO Node OS")
parser.add_argument("--nodePassword", metavar='PASSWORD',required=True, help="Password for ScaleIO Node OS")
parser.add_argument("--mdmPassword", metavar='PASSWORD', required=True, help="Password for ScaleIO MDM")
parser.add_argument("--liaPassword", metavar='PASSWORD', required=True, help="Password for ScaleIO LIA")
parser.add_argument("--gwUsername", metavar='USERNAME', required=True, help="Username for ScaleIO GW")
parser.add_argument("--gwPassword", metavar='PASSWORD', required=True, help="Password for ScaleIO GW")
parser.add_argument("--gwIPaddress", metavar='IP', required=True, help="IP address for ScaleIO GW")
parser.add_argument("--packagePath", metavar='IP', required=True, help="Path where ScaleIO Packages are located")
parser.add_argument("--mdm1IPaddress", metavar='IP', required=True, help="IP address for ScaleIO MDM1")
parser.add_argument("--mdm2IPaddress", metavar='IP', required=True, help="IP address for ScaleIO MDM2")
parser.add_argument("--tbIPaddress", metavar='IP', required=True, help="IP address for ScaleIO TB")
parser.add_argument("--nodeIPaddresses", metavar='IP', nargs='+', required=True, help="IP addresses for ScaleIO nodes")

args = parser.parse_args()

###########################
# Create a ScaleIO System #
###########################
#
# Prereq: 3 x CentOS 6.5 or RHEL 6.5
#
# Flow:
# Create Nodes
# Create basic info. mdmPass, liaPass and some others
# Construct MDM and TB and basic info
# Create list of SDS
# Create list of SDC


###################
# Construct nodes #
###################
nodeUsername = args.nodeUsername #'root' # Username for ScaleIO Node OS (these machines need to be pre installed)
nodePassword = args.nodePassword #'vagrant' # Password for ScaleIO Node OS
mdm1_node = sioobj.ScaleIO_Node_Object(None, None, [args.mdm1IPaddress], None, 'linux', nodePassword, nodeUsername)
mdm2_node = sioobj.ScaleIO_Node_Object(None, None, [args.mdm2IPaddress], None, 'linux', nodePassword, nodeUsername)
tb_node = sioobj.ScaleIO_Node_Object(None, None, [args.tbIPaddress], None, 'linux', nodePassword, nodeUsername)

##########################################
# Construct basic info for System_Object #
##########################################
mdmIPs = [mdm1_node.nodeIPs[0],mdm2_node.nodeIPs[0]]
sdcList = []
sdsList = []
mdmPassword = args.mdmPassword
liaPassword = args.liaPassword
licenseKey = None
installationId = None

########################################
# Create MDMs and TB for System_Object #
########################################
primaryMdm = sioobj.Mdm_Object(json.loads(mdm1_node.to_JSON()), None, None, mdm1_node.nodeIPs)
secondaryMdm = sioobj.Mdm_Object(json.loads(mdm2_node.to_JSON()), None, None, mdm2_node.nodeIPs)
tb = sioobj.Tb_Object(json.loads(tb_node.to_JSON()), None, tb_node.nodeIPs)

callHomeConfiguration = None # {'callHomeConfiguration':'None'}
remoteSyslogConfiguration = None # {'remoteSysogConfiguration':'None'}

################################################################
#Create SDS objects - To be added to SDS list in System_Object #
################################################################
# Adjust addDevice() to match local block device you have in your node
# Define SDS that belong to a FaultSet - Not tested!
#sds1 = sioobj.Sds_Object(json.loads(node1.to_JSON()), None, 'SDS_' + str(node1.nodeIPs[0]), 'default', 'faultset1', node1.nodeIPs, None, None, None, False, '7072')

for node_ip in args.nodeIPaddresses:
    sio_node = sioobj.ScaleIO_Node_Object(None, None, [node_ip], None, 'linux', nodePassword, nodeUsername)
    sds_obj = sioobj.Sds_Object(json.loads(sio_node.to_JSON()), None, 'SDS_' + str(sio_node.nodeIPs[0]), 'default', None, sio_node.nodeIPs, None, None, None, False, '7072')
    sds_obj.addDevice("/dev/loop0", None, None)
    sdsList.append(json.loads(sds_obj.to_JSON()))
    sdc_obj = sioobj.Sdc_Object(json.loads(sio_node.to_JSON()), None, None)
    sdcList.append(json.loads(sdc_obj.to_JSON()))

#############################################################
# Create SDC objects - To be added as list to System_Object #
#############################################################
# Decide which nodes in your cluster should become a SDC
"""
node=None,
nodeInfo=None,
splitterRpaIp=None
"""


######################################################
# Construct a complete ScaleIO cluster configuration #
######################################################
sioobj = sioobj.ScaleIO_System_Object(installationId,
                               mdmIPs,
                               mdmPassword,
                               liaPassword,
                               licenseKey,
                               json.loads(primaryMdm.to_JSON()),
                               json.loads(secondaryMdm.to_JSON()),
                               json.loads(tb.to_JSON()),
                               sdsList,
                               sdcList,
                               callHomeConfiguration,
                               remoteSyslogConfiguration
                               )

# Export sioobj to JSON (should upload clean in IM)


###########################################################################
# Push System_Object JSON - To be used by IM to install ScaleIO on nodes #
###########################################################################



#######################
# LOGIN TO SCALEIO IM #
#######################
imconn = im.Im("https://" + args.gwIPaddress,args.gwUsername,args.gwPassword,verify_ssl=False,debugLevel='INFO') # "Password1!") # HTTPS must be used as there seem to be an issue with 302 responses in Requests when using POST
imconn._login()

### UPLOAD RPM PACKAGES TO BE DEPLOYED BY IM ###
imconn.uploadPackages(args.packagePath) # Adjust to your needs. All RPMs for RHEL7 should exist in this dir except for GUI and Gateway

####################
# INSTALLER STAGES #
####################

# Initialize Installer
im_installer = im.InstallerFSM(imconn, True)

print "Create minimal cluster as Python objects"
imconn.push_cluster_configuration(sioobj.to_JSON())

print "Start Install process!!!"
im_installer.Execute() # Start install process

time.sleep(30) # Wait a few seconds before continuing
