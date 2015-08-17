
# scaleio admin password
password="Scaleio123"

# add your domain here
domain = 'scaleio.local'

# add your IPs here
network = "192.168.100."
firstip = 10

box = "chef/centos-7.0"

# at least 4 nodes
nodes = 6

Vagrant.configure("2") do |config|
  # try to enable caching to speed up package installation for second run
  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  # the last node to provision will be the gateway and get the "firstip"
  gwIPaddress = "#{network}#{firstip}"
  # node-1 to node-3 are used for MDM and TB
  mdm1IPaddress = "#{network}#{firstip + 1}"
  mdm2IPaddress = "#{network}#{firstip + 2}"
  tbIPaddress = "#{network}#{firstip + 3}"

  nodeIPaddresses = ""
  (1..nodes).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.box = box
      node.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 1024]
      end
      # update box
      #node.vm.provision "update", type: "shell", path: "scripts/update.sh"

      if i != nodes
        node.vm.host_name = "node-#{i}"
        node.vm.network "private_network", ip: "#{network}#{firstip + i}"
        node.vm.provision "packages", type: "shell", path: "scripts/packages.sh"
        nodeIPaddresses += "#{network}#{firstip + i} "
      else

        node.vm.host_name = "gateway"
        node.vm.network "private_network", ip: "#{gwIPaddress}"

        node.vm.provision "download", type: "shell", path: "scripts/download.sh"
        node.vm.provision "shell" do |s|
          s.path = "scripts/gateway.sh"
          s.args   = "-p #{password}"
        end
        node.vm.provision "shell" do |s|
          s.path = "scripts/install.py"
          s.args   = "--nodeUsername root --nodePassword vagrant --mdmPassword #{password} --liaPassword #{password} --gwUsername admin --gwPassword #{password} --gwIPaddress #{gwIPaddress} --packagePath /vagrant/scaleio/ScaleIO_1.32_RHEL7_Download/ --mdm1IPaddress #{mdm1IPaddress} --mdm2IPaddress #{mdm2IPaddress} --tbIPaddress #{tbIPaddress} --nodeIPaddresses #{nodeIPaddresses}"
        end
        node.vm.provision "shell" do |s|
          s.path = "scripts/config.py"
          s.args   = "--gwIPaddress #{gwIPaddress} --mdmUsername admin --mdmPassword #{password}"
        end
        node.vm.provision "shell" do |s|
          s.path = "scripts/info.py"
          s.args   = "--gwIPaddress #{gwIPaddress} --mdmUsername admin --mdmPassword #{password}"
        end
      end

    end
  end
end
