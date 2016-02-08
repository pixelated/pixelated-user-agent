#!/bin/bash
#

hash vagrant 2>/dev/null || { echo >&2 "Vagrant is not installed.  Aborting."; exit 1; }
hash vboxmanage 2>/dev/null || hash virsh 2>/dev/null || { echo >&2 "Please install Virtualbox or Libvirt first and try again."; exit 1;}

vagrant_ssh (){
  vagrant ssh -c "export LANG=en_US.UTF-8; export LANGUAGE=en_US.UTF-8; export LC_ALL=en_US.UTF-8; cd $1; $2"
}

if [ -d ./pixelated-user-agent ]
then
  cd pixelated-user-agent
  /usr/bin/git pull --rebase
else
  /usr/bin/git clone https://github.com/pixelated/pixelated-user-agent.git
  cd pixelated-user-agent
fi

vagrant up
vagrant_ssh '/vagrant/service' './go setup'
vagrant ssh
