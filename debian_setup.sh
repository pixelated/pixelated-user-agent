#!/bin/bash
#

function clone_repo {
    if [ -d ./pixelated-user-agent ]
    then
      cd pixelated-user-agent
      /usr/bin/git pull --rebase
      rm -rf web-ui/node_modules
    else
      /usr/bin/git clone https://github.com/pixelated/pixelated-user-agent.git
      cd pixelated-user-agent
    fi
}

sudo apt-get install -y puppet git </dev/null
clone_repo
sudo puppet apply --modulepath='provisioning/modules' provisioning/manifests/debian.pp
./install-pixelated.sh -v ~/.virtualenv/user-agent-venv
