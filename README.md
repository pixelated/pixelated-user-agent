Pixelated User Agent
====================

[![CircleCI](https://circleci.com/gh/pixelated/pixelated-user-agent.svg?style=svg)](https://circleci.com/gh/pixelated/pixelated-user-agent)
[![Coverage Status](https://coveralls.io/repos/pixelated/pixelated-user-agent/badge.svg?branch=master)](https://coveralls.io/r/pixelated/pixelated-user-agent?branch=master)
[![Stories in Doing](https://badge.waffle.io/pixelated/pixelated-user-agent.svg?label=doing&title=Doing)](http://waffle.io/pixelated/pixelated-user-agent)

The Pixelated User Agent is the email client of the Pixelated ecosystem. It is composed of two parts, a web interface written in JavaScript ([FlightJS](https://flightjs.github.io/) and [React](https://facebook.github.io/react/)) and a Python API that interacts with a [LEAP Provider](https://leap.se/), the email platform that Pixelated is built on.

Here's a [podcast](https://soundcloud.com/thoughtworks/pixelated-why-secure-communication-is-essential) that explains the project.

**Pixelated is still in early development state!**

![High level architecture User Agent](https://raw.githubusercontent.com/pixelated/website/master/assets/images/pixelated-user-agent.png)

## Installing Pixelated as a Service

To run your own instance of Pixelated, follow these instructions: https://github.com/pixelated/puppet-pixelated#manual-installation

## Installing Pixelated for Development

If you want to run and test it locally, then before you have to install the following dependencies:

* [Vagrant](https://www.vagrantup.com/downloads.html), a tool that automates the setup of a virtual machine with the development environment;
* A vagrant [compatible provider](https://www.vagrantup.com/docs/providers/), e.g. [Virtual Box](https://www.virtualbox.org/wiki/Downloads);
* If you don't want to use vagrant, check the [Developer-Setup-on-native-OS](https://github.com/pixelated/pixelated-user-agent/wiki/Developer-Setup-on-native-OS) page.

### Option 1: Run Pixelated User Agent against an existing LEAP provider

1. If you don't have access to an existing LEAP provider, you can create an account at [Bitmask mail demo provider](https://mail.bitmask.net/).

2. Clone the Pixelated User Agent repo and start the virtual machine (downloads 600MB, you may want get a coffee or tea in the meantime):

    ```
    $ git clone https://github.com/pixelated/pixelated-user-agent.git
    $ cd pixelated-user-agent
    $ vagrant up
    ```

3. Log into the VM:
    * You can access the guest OS shell via the command `vagrant ssh` run within the `pixelated-user-agent` folder in the host OS.
    * `/vagrant` in the guest OS is mapped to the `pixelated-user-agent` folder in the host OS. File changes on either side will reflect in the other.

    ```
    $ vagrant ssh
    $ cd /vagrant
    ```

4. Start the pixelated user agent:

    ```
    $ pixelated-user-agent --host 0.0.0.0 --multi-user --provider=mail.bitmask.net
    ```

    You also have other ways to start the user agent. Check the ["Single User Mode vs Multi User Mode"](https://github.com/pixelated/pixelated-user-agent/wiki/Single-User-mode-vs-Multi-User-mode) page.

5. Go to [localhost:3333](http://localhost:3333/) on your browser. You should see the login screen, where you can put your username and password created on step 1. Once you login, you'll see your inbox.

    First time email sync could be slow, please be patient. This could be the case if you have a lot of emails and it is the first time you setup the user agent on your machine.

### Option 2: Run Pixelated User Agent against a local LEAP provider

We suggest you to use the following instructions:

* Install Pixelated User Agent using [Developer-Setup-on-native-OS](https://github.com/pixelated/pixelated-user-agent/wiki/Developer-Setup-on-native-OS) page;
* Install a local LEAP provider using the [LEAP Platform installation with vagrant](https://leap.se/en/docs/platform/tutorials/vagrant#2-vagrant-with-static-vagrantfile) instructions.
* [Running user agent against a local LEAP provider](https://github.com/pixelated/pixelated-user-agent/wiki/Running-user-agent-against-a-local-LEAP-provider)

## Contributing

You are most welcome to contribute to the Pixelated User Agent code base. Please have a look at the [contributions guide](https://github.com/pixelated/pixelated-user-agent/blob/master/CONTRIBUTING.md).

If you want to contribute as a designer or XD, see the [issues labeled 'Needs Prototype'](https://github.com/pixelated/pixelated-user-agent/labels/Needs%20Prototype) for some ideas of where to start!

## Useful links

* [Starting Development](https://github.com/pixelated/pixelated-user-agent/wiki/Starting-Development)
* [Running tests](https://github.com/pixelated/pixelated-user-agent/wiki/Running-Tests)
* [User Agent with Debian packages](https://github.com/pixelated/pixelated-user-agent/wiki/Debian-package)
* [Translating Pixelated](https://github.com/pixelated/pixelated-user-agent/wiki/Translating-Pixelated)

And much more in our [wiki pages](https://github.com/pixelated/pixelated-user-agent/wiki)
