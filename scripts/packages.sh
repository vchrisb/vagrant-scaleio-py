#!/bin/bash

case "$(uname -r)" in
  *el6*)
    sysctl -p kernel.shmmax=209715200
    yum install numactl libaio -y
    ;;
  *el7*)
    yum install numactl libaio -y
    ;;
esac

truncate -s 100GB /home/vagrant/scaleio1
losetup /dev/loop0 /home/vagrant/scaleio1

if [[ -n $1 ]]; then
  echo "Last line of file specified as non-opt/last argument:"
  tail -1 $1
fi
