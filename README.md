Pixelated User Agent
====================

[![CircleCI](https://circleci.com/gh/pixelated/pixelated-user-agent.svg?style=svg)](https://circleci.com/gh/pixelated/pixelated-user-agent)
[![Coverage Status](https://coveralls.io/repos/pixelated/pixelated-user-agent/badge.svg?branch=master)](https://coveralls.io/r/pixelated/pixelated-user-agent?branch=master)
[![Stories in Doing](https://badge.waffle.io/pixelated/pixelated-user-agent.svg?label=doing&title=Doing)](http://waffle.io/pixelated/pixelated-user-agent)

The Pixelated User Agent is the email client of the Pixelated ecosystem. It is composed of two parts, a web interface written in JavaScript ([FlightJS](https://flightjs.github.io/) and [React](https://facebook.github.io/react/)) and a Python API that interacts with a [LEAP Provider](https://leap.se/), the email platform that Pixelated is built on.

Here's a [podcast](https://soundcloud.com/thoughtworks/pixelated-why-secure-communication-is-essential) that explains the project.

**Pixelated is still in early development state!**

![High level architecture User Agent](https://raw.githubusercontent.com/pixelated/website/master/assets/images/pixelated-user-agent.png)

## Getting started

You are most welcome to contribute to the pixelated user agent code base. Please have a look at the [contributions how to](https://github.com/pixelated/pixelated-user-agent/blob/master/CONTRIBUTING.md).

## Installing Pixelated

To run your own instance of Pixelated, follow these instructions: https://github.com/pixelated/puppet-pixelated#manual-installation

## Development

If you want to run and test it locally, then before you have to install the following dependencies:

* [Vagrant](https://www.vagrantup.com/downloads.html), Vagrant is a tool that automates the setup of a virtual machine with the development environment
* A vagrant [compatible provider](https://www.vagrantup.com/docs/providers/), e.g. [Virtual Box](https://www.virtualbox.org/wiki/Downloads).

### Option 1: Run Pixelated User Agent against an existing LEAP provider

1) If you don't have access to an existing LEAP provider, you can create an account at [Bitmask mail demo provider](https://mail.bitmask.net/).

2) Clone the Pixelated User Agent repo and start the virtual machine (downloads 600MB, you may want get a coffee or tea in the meantime):

```
$ git clone https://github.com/pixelated/pixelated-user-agent.git
$ cd pixelated-user-agent
$ vagrant up
```

3) Log into the VM:
* You can access the guest OS shell via the command `vagrant ssh` run within the `pixelated-user-agent/` folder in the host OS.
* /vagrant/ in the guest OS is mapped to the pixelated-user-agent/ folder in the host OS. File changes on either side will reflect in the other.

```
$ vagrant ssh
$ cd /vagrant
```

4) Start the pixelated user agent:

```
$ pixelated-user-agent --host 0.0.0.0 --multi-user --provider=mail.bitmask.net
```

5) Go to [localhost:3333](http://localhost:3333/) on your browser. You should see the login screen, where you can put your username and password created on step 1. Once you login, you'll see your inbox.

First time email sync could be slow, please be patient. This could be the case if you have a lot of emails and it is the first time you setup the user agent on your machine.

#### How to get start with development?

See the [Starting Development page](https://github.com/pixelated/pixelated-user-agent/wiki/Starting-Development)

### Option 2: Pixelated User Agent + Leap Platform

You can install the Pixelated User Agent and the Leap Platform at once, just by running the following command on your console (this may take a while, please be patient):

```bash
 curl https://raw.githubusercontent.com/pixelated/puppet-pixelated/master/vagrant_platform.sh | sh
```

 Once installed, you can create accounts by visiting the LEAP Webapp at [localhost:4443/signup](https://localhost:4443/signup) and see Pixelated in action at [localhost:8080](https://localhost:8080/).

 NOTE: Be aware that you will not be able to send mails outside, but you can test sending mails internally from one user to another.

 ## Developer Setup On Native OS

 Please ensure that you have an email user from your preferred leap provider (Step 3).
 Details for developer installations [on OSX](#on-osx) and [Debian distributions](#on-debian-distributions) are explained below.


 ### On OSX

 First, you will need to install the [GPG tools](https://gpgtools.org/) for Mac.
 Then, run the following sequence of commands:
 ```bash
 $ curl https://raw.githubusercontent.com/pixelated/pixelated-user-agent/master/osx_setup.sh | sh
 $ cd pixelated-user-agent && source ~/.virtualenv/user-agent-venv/bin/activate
 ```

 Please note that you will have to activate the virtualenv anytime you work on a different terminal. This is done by simply running `$ source ~/.virtualenv/user-agent-venv/bin/activate` first.

 Running the user agent and the various tests are the same as in the vagrant setup in step 4) and 6) above.

 ### On Debian distributions

 This is the setup for developers. Please run the following commands:

 ```bash
 $ curl https://raw.githubusercontent.com/pixelated/pixelated-user-agent/master/debian_setup.sh | bash
 $ cd pixelated-user-agent && source ~/.virtualenv/user-agent-venv/bin/activate
 ```

 Please note that you will have to activate the virtualenv anytime you work on a different terminal. This is done by simply running `$ source ~/.virtualenv/user-agent-venv/bin/activate` first.

 Running the user agent and the various tests are the same as in the vagrant setup in step 4) and 6) above.

 ## Debian package

 For people that just want to try the user agent, we have debian packages available in our [repository](http://packages.pixelated-project.org/debian/). To use it, you have to add it to your sources list:

 ```shell

 echo "deb [arch=amd64] http://packages.pixelated-project.org/debian jessie-snapshots main" > /etc/apt/sources.list.d/pixelated.list

 apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

 apt-get update

 apt-get install pixelated-user-agent
 ```

 for multi-user mode, change the last line above to
 ```shell
 apt-get install pixelated-server
 ```

## Running tests

[Here](https://github.com/pixelated/pixelated-user-agent/wiki/Running-Tests) you will find informations about how to run Pixelated tests.

# Further Notes

## Multi User Mode

To run the pixelated user agent multi user mode, please run the following:
```bash
 vagrant@jessie:/vagrant$ pixelated-user-agent --host 0.0.0.0 --multi-user --provider=dev.pixelated-project.org
```

You will need to change `dev.pixelated-project.org` to the hostname of the leap provider that you will be using.
Once that is done, you can use by browsing to [http://localhost:3333](http://localhost:3333), where you will be prompted for your email username and password.

## Config file with credentials

Create a config file with `ini` format in the root directory, see the example:

*credentials.ini*
```
[pixelated]
HOST=0.0.0.0
PORT=8080
leap_server_name=<your_provider>
leap_username=<your_username>
leap_password=<your_password>
```
Host and port is optional.

To use it, start the user agent like this:
`$ pixelated-user-agent --host 0.0.0.0 --config credentials.ini`



## How to translate the user interface

See: [Translating Pixelated](https://github.com/pixelated/pixelated-user-agent/wiki/Translating-Pixelated)

## More informations

Read the [wiki pages](https://github.com/pixelated/pixelated-user-agent/wiki)
