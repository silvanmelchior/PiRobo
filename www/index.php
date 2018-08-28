<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/fontawesome-all.min.css">
    <link rel="stylesheet" href="css/main.css?v=1">
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
        <button type="button" class="btn btn-outline-secondary my-2 my-sm-0 ml-2" data-toggle="modal" data-target="#shutdownModal"><i class="fas fa-power-off"></i></button>
    </nav>

    <div class="container-fluid mt-2">
      <div class="row">
        <div class="col-md-9 order-md-last">

          <div class="collapse show" id="collapseCam">
            <div class="card mb-4">
              <div class="card-header">
                Camera View
              </div>
              <div class="card-body">
                <p>Blablabla</p>
              </div>
            </div>
          </div>

          <div class="collapse" id="collapseTouch">
            <div class="card mb-4">
              <div class="card-header">
                Touch Input
              </div>
              <div class="card-body">         
              </div>
            </div>
          </div>

          <div class="collapse" id="collapseKey">
            <div class="card mb-4">
              <div class="card-header">
                Keyboard Input
              </div>
              <div class="card-body">
                <div class="container-fluid">
                  <div class="row">
                    <div class="number_area">
                      <div id="key_1">1</div>
                      <div id="key_2">2</div>
                      <div id="key_3">3</div>
                      <div id="key_4">4</div>
                      <div id="key_5">5</div>
                      <div id="key_6">6</div>
                      <div id="key_7">7</div>
                      <div id="key_8">8</div>
                      <div id="key_9">9</div>
                      <div id="key_0">0</div>
                    </div>
    		          </div>
                  <div class="row">
                    <div class="col-md-6 mb-4">
		                  <div class="keyboard_area">
			                  <div id="key_w" class="keyboard_up">W</div>
			                  <div id="key_a" class="keyboard_left">A</div>
			                  <div id="key_s" class="keyboard_down">S</div>
			                  <div id="key_d" class="keyboard_right">D</div>
		                  </div>
      		          </div>
                    <div class="col-md-6 mb-4">
		                  <div class="keyboard_area">
			                  <div id="key_i" class="keyboard_up">I</div>
			                  <div id="key_j" class="keyboard_left">J</div>
			                  <div id="key_k" class="keyboard_down">K</div>
			                  <div id="key_l" class="keyboard_right">L</div>
		                  </div>
      		          </div>
    		          </div>
		            </div>
              </div>
            </div>
          </div>

          <div class="collapse show" id="collapseOut">
            <div class="card mb-4">
              <div class="card-header">
                Output
              </div>
              <div class="card-body">         
                <pre id="output_section">No output</pre>
              </div>
            </div>
          </div>

        </div>
        <div class="col-md-3 order-md-first">

          <div class="card mb-4">
            <div class="card-header">
              Run Control
            </div>
            <div class="card-body">
              <button id="compile_btn" type="button" class="btn btn-lg btn-secondary btn-block" onclick="compile()">Compile</button>
              <div class="btn-group btn-block" role="group">
                <button id="run_btn" type="button" style="width:50%;" class="btn btn-lg btn-success" onclick="run()">Run</button>
                <button id="stop_btn" type="button" style="width:50%;" class="btn btn-lg btn-danger" onclick="stop()">Stop</button>
              </div>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              Panel Selection
            </div>
            <div class="card-body">
              <div class="btn-group-vertical btn-block" role="group">
                <button class="btn-nohover btn btn-outline-secondary active" type="button" data-toggle="button" onclick="toggle_cam();">Camera</button>
                <button class="btn-nohover btn btn-outline-secondary" type="button" data-toggle="button" onclick="toggle_touch();">Touch Input</button>
                <button class="btn-nohover btn btn-outline-secondary" type="button" data-toggle="button" onclick="toggle_key();">Keyboard Input</button>
                <button class="btn-nohover btn btn-outline-secondary active" type="button" data-toggle="button" onclick="toggle_out();">Output</button>
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
      </div>
    </div>
    
    <div class="modal fade" id="shutdownModal" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Power Off</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Do you want to shutdown the system?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <form action="power.php" method="POST">
              <input type="hidden" name="action" value="reboot">
              <button type="submit" class="btn btn-danger"><i class="fas fa-redo"></i> Restart</button>
            </form>
            <form action="power.php" method="POST">
              <input type="hidden" name="action" value="shutdown">
              <button type="submit" class="btn btn-danger"><i class="fas fa-power-off"></i> Power Off</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    
    <script src="js/jquery-3.3.1.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/main.js?v=2"></script>
    <script src="js/keyboard.js?v=2"></script>

  </body>
</html>
