#
class pixelated::hackday_dev_env {
  file { '/home/vagrant/.activate_custom_node_modules.sh':
    owner  => 'vagrant',
    mode   => '0600',
    source => 'puppet:///modules/pixelated/activate_custom_node_modules.sh',
  }
  exec { 'add_custom_node_modules_to_bashrc':
    command => "/bin/bash -c 'echo \"source /home/vagrant/.activate_custom_node_modules.sh\" >> /home/vagrant/.bashrc'",
    unless  => "/bin/grep \"source /home/vagrant/.activate_custom_node_modules.sh\" /home/vagrant/.bashrc",
    user    => 'vagrant',
    require => File['/home/vagrant/.activate_custom_node_modules.sh']
  }
}
