export LC_ALL=en_US.UTF-8

sudo apt-get update
sudo apt-get install -y git nodejs-legacy npm python-setuptools python-dev libffi-dev g++ rng-tools ruby-dev
sudo easy_install pip
sudo pip install virtualenv
sudo gem install compass

sudo echo "HRNGDEVICE=/dev/urandom" >> /etc/default/rng-tools

sudo /etc/init.d/rng-tools start

cd /vagrant

USERNAME=vagrant ./install-pixelated.sh
