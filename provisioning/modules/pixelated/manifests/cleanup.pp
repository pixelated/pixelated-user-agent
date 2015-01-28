# make the vagrant images smaller
class pixelated::cleanup {
  exec{'dd_zero':
    command => '/bin/dd if=/dev/zero of=/tmp/dd_zero;rm /tmp/dd_zero'
  }
}
