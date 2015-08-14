vagrant-scaleio-py
---------------

# Description

Vagrantfile to create a EMC ScaleIO lab setup leveraging `scaleio-py`from @swevm.

# Usage

This Vagrant setup will automatically deploy a configurable number of CentOS 7 nodes, download the ScaleIO software and install a full ScaleIO cluster.

To use this, you'll need to complete a few steps:

1. `git clone https://github.com/vchrisb/vagrant-scaleio-py.git`
2. Edit nodes parameter to adjust for number of ScaleIO nodes to be deployed
3. Run `vagrant up` (if you have more than one Vagrant Provider on your machine run `vagrant up --provider virtualbox` instead)

Note, the cluster will come up with the default unlimited license for dev and test use.

# Troubleshooting

If anything goes wrong during the deployment, run `vagrant destroy -f` to remove all the VMs and then `vagrant up` again to restart the deployment.
