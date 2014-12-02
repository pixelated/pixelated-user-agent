# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network :forwarded_port, guest: 3333, host: 3333
  config.vm.provision :shell, path: "provisioning/provision.sh"
  config.vm.provider "virtualbox" do |v|
      v.memory = 1024
  end
end
