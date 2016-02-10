Pixelated User Agent
====================

[![Build Status](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master/build_image)](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master) [
![Coverage Status](https://coveralls.io/repos/pixelated/pixelated-user-agent/badge.svg?branch=master)](https://coveralls.io/r/pixelated/pixelated-user-agent?branch=master)

The Pixelated User Agent is the mail client of the Pixelated ecosystem. It is composed of two parts, a web interface written in JavaScript ([FlightJS](https://flightjs.github.io/)) and a Python API that interacts with a LEAP Provider, the e-mail platform that Pixelated is built on.

**Pixelated is still in early development state!**

![High level architecture User Agent](https://pixelated-project.org/assets/images/pixelated-user-agent.png)

## Getting started

You are most welcome to contribute to the pixelated user agent code base. Please have a look at the [contributions how to](https://github.com/pixelated/pixelated-user-agent/blob/master/CONTRIBUTING.md).

1) Listen to [this podcast](https://soundcloud.com/thoughtworks/pixelated-why-secure-communication-is-essential).

2) Install [Vagrant](https://www.vagrantup.com/downloads.html) and a vagrant [compatible provider](https://www.vagrantup.com/docs/providers/), e.g. [Virtual Box](https://www.virtualbox.org/wiki/Downloads). Vagrant is a tool that automates the setup of a virtual machine with the development environment in your computer. Inside the virtual machine's filesystem, this repository will be automatically mounted in the `/vagrant` folder.

3) Clone the repo and start the virtual machine (downloads 600MB):

```
$ git clone https://github.com/pixelated-project/pixelated-user-agent.git
$ cd pixelated-user-agent 
$ vagrant up
```

4) Set up your python virtualenv

```
$ pip install virtualenv setuptools
$ cd ~
$ virtualenv pixelated
$ virtualenv -p [PATH/TO/YOUR/PYTHON/EXECUTABLE] pixelated
$ source ~/.virtualenv/pixelated/bin/activate
```

5) There's a bug in a LEAP library that can't handle symlinks to your local GPG installation. To fix it, add the path to your GPG binary to your $PATH so that it is found before the symlink in `/usr/local/bin` (or similar)

6) Log into the VM: 

```
$ vagrant ssh
```

7) Setup the project (downloads a few hundred more megabytes): 

```
$ cd /vagrant/service
$ ./go setup
```

8) Register with a LEAP provider. You can create a developer account at our [Dev Provider](https://dev.pixelated-project.org/). Please contact us at team@pixelated-project.org for an invite code.

9) Run the user agent:

```
$ pixelated-user-agent --host 0.0.0.0

Which provider do you want to connect to: 
dev.pixelated-project.org

What’s your username registered on the provider: 
username (the one you created in previous step)

Type your password: 
******** (the one you created in previous step)
```

10) Connect to the provider using your credentials. If the user agent starts up successfully, you will not see any other output.

11) Go to [localhost:3333](http://localhost:3333/). You should see a loading screen for a few seconds, then your inbox. If it sticks on the loading screen, check your terminal for errors, then [get help](https://pixelated-project.org/faq/#contact-the-project).

12) If you like console output, you can also run the tests to see if everything went according to plan.

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

13) You're all set! We've prepared [a couple of issues labeled "Beginner"](https://github.com/pixelated/pixelated-user-agent/issues?utf8=%E2%9C%93&q=is%3Aopen+is%3Aissue+label%3ABeginners+) that are a good place to dive into the project. Happy Hacking!

# Further Notes

## Multi User Mode

To run the pixelated user agent multi user mode, please run the following:
```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ pixelated-user-agent --host 0.0.0.0 --multi-user --provider=dev.pixelated-project.org
```

You will need to change `dev.pixelated-project.org` to the hostname of the leap provider that you will be using.
Once that is done, you can use by browsing to [http://localhost:3333](http://localhost:3333), where you will be prompted for your email username and password.

## Continuous Integration
All commits to the pixelated user agent code trigger all tests to be run in [snap-ci](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master).

## Misc
* You can access the guest OS shell via the command `vagrant ssh` run within the `pixelated-user-agent/` folder in the host OS.
* `/vagrant/` in the guest OS is mapped to the `pixelated-user-agent/` folder in the host OS. File changes on either side will reflect in the other.
* First time email sync could be slow, please be patient. This could be the case if you have a lot of emails already and it is the first time you setup the user agent on your machine.
* CTRL + \ will stop the server.
* For all backend changes, you will need to stop and [restart the server](#running-the-user-agent).
* For most frontend changes, you will just need to reload the browser. Some changes (in particular, those involving css or handlebars) you will need to run:
```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd web-ui
 (user-agent-venv)vagrant@jessie:/vagrant/web-ui$ ./go build
```

## Developer Setup On Native OS
Please ensure that you have an email user from your preferred leap provider ([How to](#registering-with-a-leap-provider)).
Details for developer installations [on OSX](#on-osx) and [Debian distributions](#on-debian-distributions) are explained below.
In case of any issues, please ping us on IRC ([#pixelated on irc.freenode.net](irc://irc.freenode.net/pixelated)), we will be available to help you from there.

### On OSX
First, you will need to install the [GPG tools](https://gpgtools.org/) for Mac.
Then, run the following sequence of commands:
```bash
$ curl https://raw.githubusercontent.com/pixelated/pixelated-user-agent/master/osx_setup.sh | sh
$ cd pixelated-user-agent && source ~/.virtualenv/user-agent-venv/bin/activate
```

Please note that you will have to activate the virtualenv anytime you work on a different terminal. This is done by simply running `$ source ~/.virtualenv/user-agent-venv/bin/activate` first.

Running the user agent ([How to](#running-the-user-agent)), and the various tests ([How to](#running-tests)) are the same as in the vagrant setup above.

### On Debian distributions
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
