sudo apt-get update
sudo apt-get install -y git nodejs-legacy npm python-setuptools python-dev libffi-dev g++ rng-tools
sudo easy_install pip
sudo pip install virtualenv
sudo gem install bundler

sudo echo "HRNGDEVICE=/dev/urandom" >> /etc/default/rng-tools

sudo /etc/init.d/rng-tools start

cd /vagrant

USERNAME=vagrant ./install-pixelated.sh
