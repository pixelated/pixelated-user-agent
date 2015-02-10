# installs npm from source
class pixelated::source::npm {

  exec { 'install_npm':
    command => '/usr/bin/curl -s -L https://npmjs.org/install.sh | /bin/sh',
    unless  => '/usr/bin/test -e /usr/bin/npm',
    require => Package['nodejs-legacy'];
  }
}
