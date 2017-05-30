# install requirements for setting up the useragent from source
class pixelated::source {

  package { [
    'git',
    'nodejs',
    'python-dev',
    'libffi-dev',
    'libssl-dev',
    'g++',
    'libsqlite3-dev',
    'libsqlcipher-dev',
    'libfontconfig1',
    'build-essential',
    'ruby-compass',
    'xvfb',
    'xauth',
    'chromedriver',
    'phantomjs'
    ]:
      ensure => latest
  }

  package { ['sass', 'compass']:
    ensure => latest,
    provider => 'gem',
  }

  # from jessie on, the 'virtualenv' cmd is provided
  # by a seperate package that is recommended by
  # 'python-virtualenv'
  package { 'python-virtualenv':
    ensure          => latest,
    install_options => [ '-o', 'APT::Install-Recommends=true'],
  }

}
