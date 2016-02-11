# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "LEAP/jessie"

  config.vm.define "source", primary: true do |source|
    source.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "provisioning/manifests"
      puppet.module_path    = "provisioning/modules"
      puppet.manifest_file  = "source.pp"
    end
  end

  config.vm.define "deb", autostart: false do |deb|
    deb.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "provisioning/manifests"
      puppet.module_path    = "provisioning/modules"
      puppet.manifest_file  = "deb.pp"
    end
  end

  config.vm.provider "libvirt" do |v, override|
    v.memory = 1024
    override.vm.network :forwarded_port, guest: 3333, guest_ip: '127.0.0.1', host: 3333
  end

  config.vm.provider "virtualbox" do |v, override|
    v.memory = 1024
    override.vm.network :forwarded_port, guest: 3333, host: 3333 # do NOT add host_ip in this line. It is not necessary
  end
end
