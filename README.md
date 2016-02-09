Pixelated User Agent
====================

[![Build Status](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master/build_image)](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master) [
![Coverage Status](https://coveralls.io/repos/pixelated/pixelated-user-agent/badge.svg?branch=master)](https://coveralls.io/r/pixelated/pixelated-user-agent?branch=master)

The Pixelated User Agent is the mail client of the Pixelated ecosystem. It is composed of two parts, a web interface written in JavaScript ([FlightJS](https://flightjs.github.io/)) and a Python API that interacts with a LEAP Provider, the e-mail platform that Pixelated is built on.

**Pixelated is still in early development state!**

![High level architecture User Agent](https://pixelated-project.org/assets/images/pixelated-user-agent.png)



## Getting started

### Registering with a LEAP provider
  * You can create a developer account at our [Dev Provider](https://dev.pixelated-project.org/). Please contact us at team@pixelated-project.org for an invite code.
  * If you want to run your own LEAP provider, see [Pixelated Platform installation](https://github.com/pixelated/puppet-pixelated).

## Installation Instructions
We provide a [setup with vagrant](#developer-setup-with-vagrant), which we will go in details below. There is a section on [native OSX](#on-osx) and [native Debian distributions](#on-debian-distributions) as well.
For server setup, see [debian package](#debian-package) below.


### Developer Setup With Vagrant
Please ensure that you have an email user from your preferred leap provider ([How to](#registering-with-a-leap-provider)).

##### Requirements
  * [vagrant](https://www.vagrantup.com/downloads.html) - Vagrant is a tool that automates the setup of a virtual machine with the development environment in your computer. Inside the virtual machine's filesystem, this repository will be automatically mounted in the `/vagrant` folder.
  * You will also need a vagrant [compatible provider](https://www.vagrantup.com/docs/providers/) e.g. [virtualbox](https://www.virtualbox.org/wiki/Downloads)

##### Set up
To setup the pixelated user agent inside a vagrant machine, please run the following sequence of commands in a terminal:

```bash
 $ git clone https://github.com/pixelated/pixelated-user-agent.git
 $ cd pixelated-user-agent
 $ vagrant up
 $ vagrant ssh
```

This could take a while depending on your internet connection.
Once it is complete, you should be within the terminal of the vagrant box.

##### Running the user agent
To run the pixelated user agent single user mode, please run the following:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ pixelated-user-agent --host 0.0.0.0
```
You will then need to input your provider hostname, email username and password. Please follow the prompt.
Once that is done, you can use by browsing to [http://localhost:3333](http://localhost:3333)

To run the pixelated user agent multi user mode, please run the following:
```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ pixelated-user-agent --host 0.0.0.0 --multi-user --provider=dev.pixelated-project.org
```
You will need to change dev.pixelated-project.org to the hostname of the leap provider that you will be using.
Once that is done, you can use by browsing to [http://localhost:3333](http://localhost:3333), where you will be prompted for your email username and password.

##### Running tests
To run the backend tests:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd service
 (user-agent-venv)vagrant@jessie:/vagrant/service$ ./go test
```

To run the frontend tests:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd web-ui
 (user-agent-venv)vagrant@jessie:/vagrant/web-ui$ ./go test
```

To run the functional tests:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd service
 (user-agent-venv)vagrant@jessie:/vagrant/service$ ./go functional
```

##### Continuous Integration
All commits to the pixelated user agent code trigger all tests to be run in [snap-ci](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master).

##### Note
* You can access the guest OS shell via the command `vagrant ssh` run within the `pixelated-user-agent/` folder in the host OS.
* `/vagrant/` in the guest OS is mapped to the `pixelated-user-agent/` folder in the host OS. File changes on either side will reflect in the other.
* First time email sync could be slow, please be patient. This could be the case if you have a lot of emails already and it is the first time you setup the user agent on your machine.
* CTRL + \ will stop the server.
* For all backend changes, you will need to stop and [restart the server](#running-the-user-agent).
* For most frontend changes, you will just need to reload the browser. Some changes (in particular, those involving css or handlebars) you will need run:
```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd web-ui
 (user-agent-venv)vagrant@jessie:/vagrant/web-ui$ ./go build
```

### Developer Setup On Native OS
Please ensure that you have an email user from your preferred leap provider ([How to](#registering-with-a-leap-provider)).
Details for developer installations [on OSX](#on-osx) and [Debian distributions](#on-debian-distributions) are explained below.
In case of any issues, please ping us on IRC ([#pixelated on irc.freenode.net](irc://irc.freenode.net/pixelated)), we will be available to help you from there.

#### On OSX
First, you will need to install the [GPG tools](https://gpgtools.org/) for Mac.
Then, run the following sequence of commands:
```bash
$ curl https://raw.githubusercontent.com/pixelated/pixelated-user-agent/master/osx_setup.sh | sh
$ cd pixelated-user-agent && source ~/.virtualenv/user-agent-venv/bin/activate
```

Please note that you will have to activate the virtualenv anytime you work on a different terminal. This is done by simply running `$ source ~/.virtualenv/user-agent-venv/bin/activate` first.

Running the user agent ([How to](#running-the-user-agent)), and the various tests ([How to](#running-tests)) are the same as in the vagrant setup above.

#### On Debian distributions
This is the setup for developers. Please run the following commands:

```bash
$ curl https://raw.githubusercontent.com/pixelated/pixelated-user-agent/master/debian_setup.sh | bash
$ cd pixelated-user-agent && source ~/.virtualenv/user-agent-venv/bin/activate
```

Please note that you will have to activate the virtualenv anytime you work on a different terminal. This is done by simply running `$ source ~/.virtualenv/user-agent-venv/bin/activate` first.

Running the user agent ([How to](#running-the-user-agent)), and the various tests ([How to](#running-tests)) are the same as in the vagrant setup above.

## Debian package

For people that just want to try the user agent, we have debian packages available in our [repository](http://packages.pixelated-project.org/debian/). To use it, you have to add it to your sources list:

```shell

echo "deb http://packages.pixelated-project.org/debian jessie-snapshots main" > /etc/apt/sources.list.d/pixelated.list

apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

apt-get update

apt-get install pixelated-user-agent
```
