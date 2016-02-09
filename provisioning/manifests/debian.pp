# This class will install the requirements to setup the
# useragent from source
class { '::pixelated::apt': } ->
class { '::pixelated::common': } ->
class { '::pixelated::source': }
