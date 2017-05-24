# add the pixelated sources needed to install everything
class pixelated::apt {
  package { [
    'apt-transport-https',
    'lsb-release']:
      ensure => installed
  }

  # nodejs latest repo
  file { '/etc/apt/sources.list.d/noderesource.list':
    content =>
      'deb https://deb.nodesource.com/node_7.x jessie main
      deb-src https://deb.nodesource.com/node_7.x jessie main',
    owner   => 'root'
  }
  exec{'add_nodesource_key':
    command => '/usr/bin/curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -',
    unless  => '/usr/bin/apt-key finger 2>&1 | grep -q "9FD3 B784 BC1C 6FC3 1A8A  0A1C 1655 A0AB 6857 6280"',
    notify  => Exec['apt_get_update']
  }
  file { '/etc/apt/preferences.d/nodejs':
    content =>
      'Package: nodejs
      Pin: release o=Node Source
      Pin-Priority: 999',
    owner   => 'root'
  }

  exec { 'apt_get_update':
    command     => '/usr/bin/apt-get -y update',
    refreshonly => true,
    require => [
      Package['apt-transport-https', 'lsb-release'],
      File['/etc/apt/sources.list.d/noderesource.list'],
      File['/etc/apt/preferences.d/nodejs']
    ]
  }

}
