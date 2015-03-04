Pixelated User Agent
====================

The Pixelated User Agent is the mail client of the Pixelated ecosystem, it is composed of two parts, a web interface written in javascript and an API written in python that glues that interface with the Pixelated or LEAP Provider.

>**The Pixelated User Agent is still in early development state!**

>Some things may not yet work the way you expect it to.
>Setting up the service is still rather troublesome and so far it only serves limited functionality.

![High level architecture User Agent](https://pixelated-project.org/drawings/architecture-user-agent.svg)

## Getting started for development

### Registering with a provider
First of all, you should have an account on a LEAP/Pixelated provider with email support.
  * You can create a developer account at our [Dev Provider](https://dev.pixelated-project.org/).
  * There are some other LEAP providers on the [Bitmask page](https://bitmask.net), but they don't support email currently.

### Instructions
Requirements:
  * vagrant
  * virtualbox

Clone the repository:

    git clone https://github.com/pixelated-project/pixelated-user-agent.git

From the root folder, set up the vagrant machine:

    vagrant up source

You can log into the machine and view project root folder with:

    vagrant ssh
From here on you can run the tests for the UI by going to the **web-ui** folder or for the API by going to the **service** folder and running:

    cd /vagrant/web-ui
    ./go test
    
    cd /vagrant/service
    ./go test
You can also run the mail client with:

    pixelated-user-agent --host 0.0.0.0

As soon as the agent start you will be asked for username, password and the [provider you registered with](https://github.com/pixelated-project/pixelated-user-agent/blob/master/README.md#registering-with-a-provider). 

Then point your browser to [http://localhost:3333](http://localhost:3333) to see it running.

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
