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
    $virtualenv_path = "/home/vagrant/user-agent-venv"

    exec { 'install-pixelated':
      environment => 'USERNAME=vagrant',
      command     => "/vagrant/install-pixelated.sh -v \"${virtualenv_path}\"",
      cwd         => '/vagrant',
      user        => 'vagrant',
      timeout     => 0
    }

    exec { 'add_virtualenv_to_bashrc':
      command => "/bin/bash -c 'echo \"source ${virtualenv_path}/bin/activate ; cd /vagrant\" >> /home/vagrant/.bashrc'",
      unless  => "/bin/grep \"source ${virtualenv_path}\" /home/vagrant/.bashrc",
      user    => 'vagrant',
      require => Exec['install-pixelated']
    }
  }

  Stage['main'] -> Stage['install_pixelated']
}
