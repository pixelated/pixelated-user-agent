class pixelated::source {

  package { [
    'git',
    'nodejs-legacy',
    'npm',
    'python-dev',
    'python-virtualenv',
    'libffi-dev',
    'g++',
    'ruby-dev',
    'libsqlite3-dev' ]:
    ensure => latest
  }

  package { 'compass':
    ensure   => installed,
    provider => 'gem'
  }

  stage { 'install_pixelated': }

  class { 'install_pixelated' :
    stage => install_pixelated
  }

  class install_pixelated {
    exec { 'install-pixelated':
      environment => 'USERNAME=vagrant',
      command     => '/bin/bash /vagrant/install-pixelated.sh',
      cwd         => '/vagrant',
      user        => 'vagrant',
      timeout     => 0
    }
  }

  Stage['main'] -> Stage['install_pixelated']
}
