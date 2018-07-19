<?php

  function print_points($db, $admin) {
    echo "<table><tr><th></th>";
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
          echo "<input type=\"hidden\" name=\"team_admin\" value=\"$i\">";
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
    echo "</table>";
  }
  
  function print_codeform($db) {
    ?>
    <form action="index.php" method="post">
      <table>
        <tr>
          <td>Team:</td>
          <td>
            <select name="team_user">
              <?php
                $teams = $db->get_teams();
                for($i=0; $i<count($teams); $i++) {
                  echo "<option value=\"$i\">" . $teams[$i][0] . "</option>";
                }
              ?>
            </select>
          </td>
        </tr>
        <tr>
          <td>Taks:</td>
          <td>
            <select name="task">
              <?php
                $tasks = $db->get_tasks();
                for($i=0; $i<count($tasks); $i++) {
                  echo "<option value=\"$i\">" . $tasks[$i][0] . "</option>";
                }
              ?>
            </select>
          </td>
        </tr>
        <tr>
          <td>Password: </td>
          <td><input type="text" name="pwd"></td>
        </tr>
        <tr>
          <td></td>
          <td><input type="submit" value="Submit"></td>
        </tr>
      </table>
    </form>
    <?php
  }
  
?>
