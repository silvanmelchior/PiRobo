<?php

  $ip = "255.255.255.255";
  $port = 56000+100;
  $str = "PiRobo discover";

  $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP); 
  socket_set_option($sock, SOL_SOCKET, SO_BROADCAST, 1);
  socket_set_option($sock, SOL_SOCKET, SO_RCVTIMEO, array("sec"=>5, "usec"=>0));
  socket_sendto($sock, $str, strlen($str), 0, $ip, $port);
  
  $answer = array();
  while(true) {
    $ret = @socket_recvfrom($sock, $buf, 20, 0, $ip, $port);
    if($ret === false) break;
    if(substr($buf, 0, 2) == "v1") {
      $split = explode(" ", $buf);
      $item = array("ip" => $ip, "sw_version" => $split[1], "hw_id" => $split[2]);
      array_push($answer, $item);
    }
  }
  
  echo json_encode($answer);

  socket_close($sock);

?>
