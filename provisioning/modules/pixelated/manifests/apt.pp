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

  file { '/tmp/0x287A1542472DC0E3_packages@pixelated-project.org.asc':
    source => 'puppet:///modules/pixelated/0x287A1542472DC0E3_packages@pixelated-project.org.asc',
    notify => Exec['add_pixelated_key']
  }

  exec{'add_pixelated_key':
    command     => '/usr/bin/apt-key add /tmp/0x287A1542472DC0E3_packages@pixelated-project.org.asc',
    refreshonly => true,
    require     => File['/tmp/0x287A1542472DC0E3_packages@pixelated-project.org.asc'],
    notify      => Exec['apt_get_update'],
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
    notify => Exec['apt_get_update']
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
