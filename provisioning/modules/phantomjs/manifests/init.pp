class phantomjs {
  exec{'download_phantomjs':
    command => '/usr/bin/wget -O /var/local/phantomjs-1.9.8.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2',
    creates => '/var/local/phantomjs-1.9.8.tar.bz2',
    notify  => Exec['unpack_phantomjs'],
  }
  exec{'unpack_phantomjs':
    command     => '/bin/tar xvfj phantomjs-1.9.8.tar.bz2',
    cwd         => '/var/local/',
    refreshonly => true,
    notify      => Exec['install_phantomjs'],
  }
  exec{'install_phantomjs':
    command     => '/usr/bin/install /var/local/phantomjs-1.9.8-linux-x86_64/bin/phantomjs /usr/bin/phantomjs',
    refreshonly => true,
  }
}
