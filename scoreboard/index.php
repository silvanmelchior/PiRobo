<?php

  require_once('db.php');

  $db = new FileDB();
  $admin = isset($_GET["admin"]) && (hash("sha256", $_GET["admin"]) ==
    "a901a2fd04464ef1386f2b25b1720d5ec3b3b86b3e599a7700158a1de2409150");
  
  if($admin && isset($_POST["team"])) {
    $team = $_POST["team"];
    $task = $_POST["task"];
    $val = 1 - $db->get_state()[$team][$task];
    $db->set_state($team, $task, $val);
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
    <table>
      <?php
        echo "<tr><th></th>";
        $tasks = $db->get_tasks();
        foreach($tasks as $task) {
          echo "<th>" . $task[0] . "</th>";
        }
        echo "<th>Total</th></tr>";
        
        $teams = $db->get_teams();
        $points = $db->get_state();
        for($i=0; $i<count($teams); $i++) {
          echo "<tr><td>" . $teams[$i][0] . "</td>";
          $total = 0;
          for($j=0; $j<count($points[$i]); $j++) {
            if($admin) {
              echo "<td><form action=\"index.php?admin=" . $_GET["admin"] . "\" method=\"post\">";
              echo "<input type=\"hidden\" name=\"team\" value=\"$i\">";
              echo "<input type=\"hidden\" name=\"task\" value=\"$j\">";
              echo "<input type=\"submit\" value=\"" . $points[$i][$j] . "\">";
              echo "</form></td>";
            }
            else {
              echo "<td>" . $points[$i][$j] . "</td>";
            }
            if($points[$i][$j]) $total += $tasks[$j][1];
          }
          echo "<td>$total</td>";
          echo "</tr>";
        }
      ?>
    </table>
  </body>
</html>
