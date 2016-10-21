#!/bin/bash

sudo apt-get -y install debian-archive-keyring
sudo bash -c 'echo "deb http://deb.debian.org/debian jessie main" > /etc/apt/sources.list.d/jessie.list'
sudo bash -c 'echo "deb http://deb.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/jessie.list'
sudo bash -c "echo -e 'Package: *\nPin: release o=Debian\nPin-Priority: -10\n' > /etc/apt/preferences.d/debian2"
sudo apt-get update
sudo  apt-get install --yes -t jessie python-dev  virtualenv
sudo  DEBIAN_FRONTEND=noninteractive apt-get install --yes -t jessie openssl libssl-dev libsqlite3-dev
sudo apt-get install --yes -t jessie-backports libsqlcipher-dev
sudo bash -c 'echo "deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu trusty main" > /etc/apt/sources.list.d/ubuntu-toolchain.list'
sudo apt-get update
sudo apt-get --yes --force-yes install gcc-4.9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60
sudo rm -rf /usr/bin/x86_64-linux-gnu-gcc && sudo ln -s /usr/bin/gcc-4.9 /usr/bin/x86_64-linux-gnu-gcc

if [ -n "$VAGRANT" ] ; then
    sudo apt-get install --yes git
    git clone https://github.com/pixelated/pixelated-user-agent && cd pixelated-user-agent
fi

rm -rf venv && virtualenv venv && source venv/bin/activate && pip install --upgrade pip setuptools

