Pixelated User Agent
====================

This contains the Pixelated User Agent, which is composed of a web UI written as a JavaScript single page app, and a service that provides a REST-ful interface that the UI can use for all User Agent actions. For now, all of these actions are mail-related but this might evolve later. The default service is written to talk to a Pixelated or LEAP provider.

>**The Pixelated User Agent is still in early development state!**

>Some things may not yet work the way you expect it to.
>Setting up the service is still rather troublesome and so far it only serves limited functionality.


# Running it
The User Agent has 2 components:
* The Web Ui, which is the the HTML, CSS and JS files served to the browser;
* The Service component, which is the web service that serves the Web UI to the browser, provides the REST API which the the Web Ui uses, and integrates with the LEAP or Pixelated provider.

## Quickstart

Dependencies are: node, npm, compass (ruby), virtualenv, git

* To install the dependencies on debian/ubuntu you need to run `sudo apt-get install nodejs npm ruby virtualenv git` and then `sudo gem install compass`

* Next step is cloning the repository with `git clone https://github.com/pixelated-project/pixelated-user-agent.git`

* Enter the folder `pixelated-user-agent`

* Run the setup `./install_pixelated.sh`

* After it finishes, you can activate the virtualenv with `source service/.virtualenv/bin/activate`

* The user agent will be available with the command `pixelated-user-agent`, running it you will be prompted for the credentials and the user agent will be started at localhost:3333

---

## Service

* Enter the `service` folder

* Create the virtualenv with `virtualenv .virtualenv` 

* Activate it with `source .virtualenv/bin/activate`

* Run the setup with `python setup.py develop --always-unzip`

* Then, to run use `pixelated-user-agent` on the command line

> You need an account in a Leap provider with support for email to test pixelated,
> if you don't have one yet, you can register with the following command
pixelated-user-agent --register your.provider.org desired_account

## Web Ui

* Enter the `web-ui` folder

* Run:
```
$ bundle install
$ npm install
$ bower install
```

If you don't have `bower` installed globally, change the third line to `$ ./node_modules/bower/bin/bower install`

The Web Ui needs to generate the templates and CSS to be served. For that, you need (from inside `./web-ui`) to run the command `./go build` at least once after downloading the code. From here on, you can run `./go watch` to auto-generate the resources as they are changed.


And that's it.

---

## Installing the debian package

The debian package is currently only available in our [repository](http://packages.pixelated-project.org/debian/). To use it you have to add it to your sources list:

```shell

echo "deb http://packages.pixelated-project.org/debian wheezy-snapshots main" >> /etc/apt/sources.list
echo "deb http://packages.pixelated-project.org/debian wheezy-backports main" >> /etc/apt/sources.list
echo "deb http://packages.pixelated-project.org/debian wheezy main" >> /etc/apt/sources.list

apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

apt-get update

apt-get install pixelated-user-agent
```

**Warning:** Currently there are some challenges with the dependencies. To make the user agent work see instructions used to build the docker image: [Dockerfile](provisioning/Dockerfile).

