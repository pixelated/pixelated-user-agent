Pixelated User Agent
====================

The Pixelated User Agent is the mail client of the Pixelated ecosystem, it is composed of two parts, a web interface written in javascript and an API written in python that glues that interface with the Pixelated or LEAP Provider.

>**The Pixelated User Agent is still in early development state!**

>Some things may not yet work the way you expect it to.
>Setting up the service is still rather troublesome and so far it only serves limited functionality.

## Getting started for development

First of all, you should have an account on a LEAP/Pixelated provider with email support.
  * You can use one of the demo accounts at [Try Pixelated](https://try.pixelated-project.org:8080/auth/login).
  * There are some other LEAP providers on the [Bitmask page](https://bitmask.net), but they don't support email currently.

Requirements:
  * vagrant
  * virtualbox

Clone the repository:

    git clone https://github.com/pixelated-project/pixelated-user-agent.git

From the root folder, set up the vagrant machine:

    vagrant up source

You can log into the machine using:

    vagrant ssh

then you can run with:

    pixelated-user-agent --host 0.0.0.0

and it's done!

## Getting started as an user

For people that just want to try the user agent, we have debian packages available in our [repository](http://packages.pixelated-project.org/debian/). To use it you have to add it to your sources list:

```shell

echo "deb http://packages.pixelated-project.org/debian wheezy-snapshots main" > /etc/apt/sources.list.d/pixelated.list
echo "deb http://packages.pixelated-project.org/debian wheezy-backports main" >> /etc/apt/sources.list.d/pixelated.list
echo "deb http://packages.pixelated-project.org/debian wheezy main" >> /etc/apt/sources.list.d/pixelated.list

apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

apt-get update

apt-get install pixelated-user-agent
```
