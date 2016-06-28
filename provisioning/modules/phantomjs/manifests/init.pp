# install phantomjs for unit tests
# we ship our local copy of phantomjs
# because downloading phantomjs fails regularly
class phantomjs {
  file{'/usr/local/bin/phantomjs':
    source => 'puppet:///modules/phantomjs/phantomjs',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
}
