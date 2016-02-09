# This class will install the requirements and the useragent
# from source. It's the default provision script called by
# 'vagrant up'

class { '::pixelated::apt': } ->
class { '::pixelated::common': } ->
class { '::pixelated::source': } ->
class { '::pixelated::source::install_useragent':}

