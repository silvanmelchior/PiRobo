<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/fontawesome-all.min.css">
    <title>PiRobo Start Page</title>
  </head>
  <body>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="index.php">PiRobo</a>      
      <ul class="navbar-nav mr-auto">
      </ul>
      <form action="icecoder" target="_blank">
        <button class="btn btn-outline-secondary my-2 my-sm-0" type="submit"><i class="fas fa-external-link-alt"></i> Code Editor</button>
      </form>
      <form action="user_ctrl" target="_blank">
        <button class="btn btn-outline-secondary my-2 my-sm-0 ml-2" type="submit"><i class="fas fa-external-link-alt"></i> Web Control</button>
      </form>
    </nav>

    <div class="container-fluid mt-2">
      <div class="row">
        <div class="col-md-3">

          <div class="card mb-4">
            <div class="card-header">
              Run Control
            </div>
            <div class="card-body">
              <button type="button" class="btn btn-lg btn-secondary btn-block" onclick="compile()">Compile</button>
              <div class="btn-group btn-block" role="group">
                <button type="button" style="width:50%;" class="btn btn-lg btn-success" onclick="run()">Run</button>
                <button type="button" style="width:50%;" class="btn btn-lg btn-danger" disabled>Stop</button>
              </div>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              System Information
            </div>
            <div class="card-body">
              <h5 class="card-title">System ID</h5>
              <p class="card-text"><code><?php echo file_get_contents("../ID.txt"); ?></code></p>
              <h5 class="card-title">SW Version</h5>
              <p class="card-text"><code><?php echo file_get_contents("../VERSION.txt"); ?></code></p>
            </div>
          </div>

        </div>
        <div class="col-md-9">

          <div class="card">
            <div class="card-header">
              Output
            </div>
            <div class="card-body">         
              <pre id="output_section">Loading...</pre>
            </div>
          </div>


        </div>
      </div>
    </div>

    
    <script src="js/jquery-3.3.1.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/main.js"></script>

  </body>
</html>
