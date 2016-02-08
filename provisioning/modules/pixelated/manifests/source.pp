# install useragent from source
class pixelated::source {
  include phantomjs

  package { [
    'git',
    'nodejs',
    'nodejs-legacy',
    'npm',
    'python-dev',
    'virtualenv',
    'libffi-dev',
    'libssl-dev',
    'g++',
    'libsqlite3-dev',
    'libfontconfig1',
    'build-essential',
    'ruby-compass']:
    ensure => latest
  }

  stage { 'install_pixelated': }

  class { 'pixelated::source::install_useragent' :
    stage => install_pixelated
  }

  Stage['main'] -> Stage['install_pixelated']
}
