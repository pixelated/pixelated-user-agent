class pixelated::source {
  include phantomjs

  package { [
    'git',
    'nodejs-legacy',
    'npm',
    'python-dev',
    'python-virtualenv',
    'libffi-dev',
    'g++',
    'ruby-dev',
    'libsqlite3-dev',
    'libfontconfig1']:
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
    $virtualenv_path = '/home/vagrant/user-agent-venv'

    exec { 'install-pixelated':
      environment => 'USERNAME=vagrant',
      command     => "/vagrant/install-pixelated.sh -v \"${virtualenv_path}\" -n /home/vagrant/boxed_node_modules",
      cwd         => '/vagrant',
      user        => 'vagrant',
      timeout     => 0
    }
  }

  Stage['main'] -> Stage['install_pixelated']
}
