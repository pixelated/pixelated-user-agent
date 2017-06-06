# install chromedriver for functional tests
# we ship our local copy of chromedriver
# because latest versions are getting recurring errors on
# test/functional/features/login.feature#Then I should see the fancy interstitial

class chromedriver (
  $release       = '1.0_beta1',
  $chromedriver  = 'chromedriver_2.27_linux64.zip',
  $google_chrome = 'google-chrome-stable_54.0.2840.100-1_amd64.deb',
) {

  exec { 'fetch_chromedriver':
    command => "/usr/bin/wget https://github.com/pixelated/pixelated-user-agent/releases/download/${release}/${chromedriver}",
    cwd     => '/var/tmp',
    creates => "/var/tmp/${chromedriver}",
  }

  exec { 'fetch_google_chrome':
    command => "/usr/bin/wget https://github.com/pixelated/pixelated-user-agent/releases/download/${release}/${google_chrome}",
    cwd     => '/var/tmp',
    creates => "/var/tmp/${google_chrome}",
  }

  exec { 'unpack_chromedriver':
    command => "/usr/bin/unzip ${chromedriver} -d /usr/local/bin/",
    cwd     => '/var/tmp/',
    creates => '/usr/local/bin/chromedriver',
    require => [ Exec['fetch_chromedriver'] ],
  }

  exec { 'install_google_chrome':
    command => "/usr/bin/dpkg -i ${google_chrome} || /usr/bin/apt-get -y -f install",
    cwd     => '/var/tmp/',
    unless  => '/usr/bin/dpkg -l google-chrome-stable > /dev/null 2>&1',
    require => [ Exec['fetch_google_chrome'], Exec['apt_get_update'] ],
  }

}
