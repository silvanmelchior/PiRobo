<?php

  $teams_file = "data/teams.txt";
  $tasks_file = "data/tasks.txt";
  if(!file_exists($teams_file) || !file_exists($tasks_file)) {
    echo "Scoreboard not initialized";
    die();
  }
  
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
