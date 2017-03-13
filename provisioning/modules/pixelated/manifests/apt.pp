# add the pixelated sources needed to install everything
class pixelated::apt {

  package { [
    'apt-transport-https',
    'lsb-release']:
    ensure => installed
  }

  # pixelated repo
  file { '/etc/apt/sources.list.d/pixelated.list':
    source  => 'puppet:///modules/pixelated/apt/pixelated.list',
    owner   => 'root',
    require => Exec['add_pixelated_key'],
    notify  => Exec['apt_get_update'],
  }

  exec{'add_pixelated_key':
    command => '/usr/bin/apt-key adv --keyserver pool.sks-keyservers.net --recv-keys F4C220FCD74F4DF45DD78FC0287A1542472DC0E3',
    unless  => '/usr/bin/apt-key finger 2>&1 | grep -q "F4C2 20FC D74F 4DF4 5DD7  8FC0 287A 1542 472D C0E3"',
    notify  => Exec['apt_get_update'],
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
