# install requirements for setting up the useragent from source
class pixelated::source {
  include phantomjs

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
    'xauth']:
      ensure => latest
  }

  # from jessie on, the 'virtualenv' cmd is provided
  # by a seperate package that is recommended by
  # 'python-virtualenv'
  package { 'python-virtualenv':
    ensure          => latest,
    install_options => [ '-o', 'APT::Install-Recommends=true'],
  }

  package {
    'chromium':
      ensure => '55.0.2883.75-1~deb8u1',
      before => Package['chromedriver']
  }

  package {
    'chromedriver':
      ensure => '55.0.2883.75-1~deb8u1'
  }


}
