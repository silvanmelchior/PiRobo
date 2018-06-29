<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/fontawesome-all.min.css">
    <title>PiRobo Power Page</title>
  </head>
  <body>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="index.php">PiRobo</a>      
    </nav>

    <div class="container-fluid mt-2">
      <div class="row">
        <div class="col-md-12">
          <?php if($_POST["action"]=="reboot") { ?>
            <h1>The system is going to reboot</h1>
            <p><br></p>
            <p>Once completed you can <a href="/">go back</a> to the start page.</p>
          <?php } else if($_POST["action"]=="shutdown") { ?>
            <h1>The system is going to shut down</h1>
            <p><br></p>
            <p>Once completed you can power off the robot.</p>
          <?php } ?>
          <p></p>
        </div>
      </div>
    </div>
    

    <script src="js/jquery-3.3.1.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>

  </body>
</html>

<?php
  if($_POST["action"] == "reboot") {
    shell_exec('sudo shutdown -r now > /dev/null 2>&1 &');
  }
  else if($_POST["action"] == "shutdown") {
    shell_exec('sudo shutdown -h now > /dev/null 2>&1 &');
  }
?>
