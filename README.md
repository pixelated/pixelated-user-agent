Pixelated User Agent
====================

[![Build Status](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master/build_image)](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master) [
![Coverage Status](https://coveralls.io/repos/pixelated-project/pixelated-user-agent/badge.svg?branch=master)](https://coveralls.io/r/pixelated-project/pixelated-user-agent?branch=master)

The Pixelated User Agent is the mail client of the Pixelated ecosystem. It is composed of two parts, a web interface written in JavaScript ([FlightJS](https://flightjs.github.io/)) and a Python API that interacts with a LEAP Provider, the e-mail platform that Pixelated is built on.

**Pixelated is still in early development state!**

![High level architecture User Agent](https://pixelated-project.org/assets/images/pixelated-user-agent.png)



## Getting started

### Registering with a LEAP provider
  * You can create a developer account at our [Dev Provider](https://dev.pixelated-project.org/).
  * If you want to run your own LEAP provider, see [pixelated-platform](https://github.com/pixelated-project/pixelated-platform).

### Requirements

  * [virtualbox](https://www.virtualbox.org/wiki/Downloads) - Virtualbox is a virtual machine provider platform. It will be used by Vagrant to create a virtual machine ready to run the Pixelated User Agent.
  * [vagrant](https://www.vagrantup.com/downloads.html) - Vagrant is a tool that automates the setup of a virtual machine with the development environment in your computer. Inside the virtual machine's filesystem, this repository will be automatically mounted in the `/vagrant` folder.

### Instructions

Clone the repository:

    git clone https://github.com/pixelated-project/pixelated-user-agent.git
    cd pixelated-user-agent

From the project root folder, set up the vagrant machine:

    vagrant up

After this is done, you can log into the machine and view project root folder with:

    vagrant ssh
    cd /vagrant

Then run the setup:
 
    cd /vagrant/service
    ./go setup
 
From here on you can run the tests for the UI by going to the **web-ui** folder or for the REST API by going to the **service** folder:

    cd /vagrant/web-ui
    ./go test

    cd /vagrant/service
    ./go test
    
To run the user agent:

```
$ pixelated-user-agent --host 0.0.0.0 -lc /vagrant/service/pixelated/certificates/dev.pixelated-project.org.ca.crt
> 2015-01-23 11:18:07+0100 [-] Log opened.
> 2015-01-23 11:18:07+0100 [-] Which provider do you want to connect to:
dev.pixelated-project.org
> 2015-01-23 11:18:52+0100 [-] What's your username registered on the provider:
username
> Type your password:
*******************
```

As soon as the user agent starts you will be asked for username, password and the [provider you registered with](https://github.com/pixelated-project/pixelated-user-agent/blob/master/README.md#registering-with-a-provider). 

Now you can see it running on [http://localhost:3333](http://localhost:3333)

## Debian package

For people that just want to try the user agent, we have debian packages available in our [repository](http://packages.pixelated-project.org/debian/). To use it you have to add it to your sources list:

```shell

echo "deb http://packages.pixelated-project.org/debian wheezy-snapshots main" > /etc/apt/sources.list.d/pixelated.list
echo "deb http://packages.pixelated-project.org/debian wheezy-backports main" >> /etc/apt/sources.list.d/pixelated.list
echo "deb http://packages.pixelated-project.org/debian wheezy main" >> /etc/apt/sources.list.d/pixelated.list

apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

apt-get update

apt-get install pixelated-user-agent
```
