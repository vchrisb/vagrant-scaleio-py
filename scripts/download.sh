#!/bin/bash

yum -y install wget unzip
cd /vagrant
wget -N -nv ftp://ftp.emc.com/Downloads/ScaleIO/ScaleIO_Linux_SW_Download.zip
unzip -o ScaleIO_Linux_SW_Download.zip -d /vagrant/scaleio/
