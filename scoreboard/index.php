<?php

  require_once('db.php');

  $db = new FileDB();
  
  // TODO: create table and then test set_state etc.
  var_dump($db->get_state());
  $db->set_state(0,2,true);
  echo "asdf";
  var_dump($db->get_state());
  
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Scoreboard</title>
  </head>
  <body>
    <h1>Scoreboard</h1>
  </body>
</html>
