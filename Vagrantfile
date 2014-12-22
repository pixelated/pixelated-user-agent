# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "fbernitt/debian-testing-amd64"
  config.vm.network :forwarded_port, guest: 3333, host: 3333
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end

  config.vm.provision "puppet" do |puppet|
    puppet.manifests_path = "provisioning"
    puppet.manifest_file = "provision.pp"
  end
end
