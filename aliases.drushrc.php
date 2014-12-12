<?php
// minimum viable drush aliases
// these are all just example values
$aliases['dev1'] = array(
    'uri' => 'test.web.server',
    'root' => '/var/www/drupal',
    'remote-host' => 'test.web.server',
    'remote-user' => 'username'
);
$aliases['live'] = array(
    'uri' => 'libraries.cca.edu',
    'root' => '/var/www/drupal',
    'remote-host' => 'libraries.cca.edu',
    'remote-user' => 'username'
);
$aliases['local'] = array(
    'uri' => 'localhost',
    'root' => '/Library/WebServer/Documents'
);
