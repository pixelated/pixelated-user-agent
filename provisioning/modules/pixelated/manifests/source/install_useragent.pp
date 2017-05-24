# install useragent in a virtualenv
# and make sure venv is activated on login
class pixelated::source::install_useragent {

  $virtualenv_path = '/home/vagrant/.venvs/pixua'

  exec { 'install-pixelated':
    # use of "user" parameter doesn't set env variables right,
    # see https://projects.puppetlabs.com/issues/23053
    # therefore we need to explicitily set them here
    environment => [ 'USERNAME=vagrant', 'HOME=/home/vagrant' ],
    command     => '/usr/bin/make install',
    cwd         => '/vagrant',
    user        => 'vagrant',
    # to debug use this
    logoutput   => true,
    timeout     => 0
  }

  file { '/home/vagrant/.bashrc':
    owner  => 'vagrant',
    mode   => '0644',
    source => 'puppet:///modules/pixelated/.bashrc',
  }

}
