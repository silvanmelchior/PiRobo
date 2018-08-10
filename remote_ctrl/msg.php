<?php

  $ip = "255.255.255.255";
  $port = 56000+100;

  $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP); 
  socket_set_option($sock, SOL_SOCKET, SO_BROADCAST, 1);
  socket_sendto($sock, $_GET["msg"], strlen($_GET["msg"]), 0, $ip, $port);

  socket_close($sock);

?>
