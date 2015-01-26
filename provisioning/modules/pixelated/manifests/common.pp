# applied to both vagrant boxed
class pixelated::common {
  package{'haveged':
    ensure => installed,
  }
}
