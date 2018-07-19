<?php

  require_once('db.php');
  require_once('gui.php');

  $db = new FileDB();
  $admin = isset($_GET["admin"]) && (hash("sha256", $_GET["admin"]) ==
    "a901a2fd04464ef1386f2b25b1720d5ec3b3b86b3e599a7700158a1de2409150");
  
  if(isset($_GET["ajax"])) {
    print_points($db, $admin);
    return;
  }
  
  if($admin && isset($_POST["team_admin"])) {
    $team = $_POST["team_admin"];
    $task = $_POST["task"];
    $val = 1 - $db->get_state()[$team][$task];
    $db->set_state($team, $task, $val);
  }

  $pwd_msg = "";
  if(isset($_POST["team_user"])) {
    $tasks = $db->get_tasks();
    $team = $_POST["team_user"];
    $task = $_POST["task"];
    $pwd = $_POST["pwd"];
    if($pwd == $tasks[$task][2]) {
      $db->set_state($team, $task, 1);
      $pwd_msg = "congratulations";
    }
    else $pwd_msg = "wrong password!";
    // TODO: wrong pwd counter?
  }
  
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Scoreboard</title>
    <script src="main.js?v=1"></script>
  </head>
  <body>
  
    <h1>Scoreboard</h1>
    <div id="table_out">
      <?php print_points($db, $admin); ?>
    </div>
    
    <?php
      if(!isset($_GET["overview"])) {
        echo "<h2>Enter Code</h2>";
        print_codeform($db);
      }
      if($pwd_msg != "") {
        echo "<div id=\"pwd_msg\">$pwd_msg</div>";
        echo "<script>setTimeout(remove_hint, 3000);</script>";
      }
    ?>
    
    <?php
      if(!$admin) echo "<script>setInterval(reload_table, 3000);</script>";
    ?>
    
  </body>
</html>
