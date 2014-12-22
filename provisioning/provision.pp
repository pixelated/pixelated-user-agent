stage { 'preinstall':
  before => Stage['main']
}

class apt_get_update {
  exec { '/usr/bin/apt-get -y update': }
}
  
class { 'apt_get_update':
  stage => preinstall
}

package { [
  'git',
  'nodejs-legacy',
  'npm',
  'python-dev',
  'python-virtualenv',
  'libffi-dev',
  'g++',
  'rng-tools',
  'ruby-dev']:
  ensure => latest
}

package { 'compass':
  ensure => latest,
  provider=> 'gem'
}

file { '/etc/default/rng-tools':
  ensure => present,
  content => "HRNGDEVICE=/dev/urandom",
  require   => Package["rng-tools"]
}

service { 'rng-tools':
  ensure => running,
  provider => init,
  require   => File['/etc/default/rng-tools']
}

stage { 'install_pixelated': }

class { 'install_pixelated' :
  stage => install_pixelated
}

class install_pixelated {
  exec { 'install-pixelated':
    command => '/bin/bash /vagrant/install-pixelated.sh',
    cwd => '/vagrant',
    user => 'vagrant'
  }
}

Stage['main'] -> Stage['install_pixelated']
