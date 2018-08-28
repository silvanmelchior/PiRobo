<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="main.js?v=1"></script>
    <link rel="stylesheet" href="main.css?v=1">
    <title>PiRobo Remote Ctrl</title>
  </head>
  <body>
    <h1 id="title" onclick="hide_text()">PiRobo Remote Ctrl</h1>
    <div id="table_out">Loading List...</div>
    <div id="controls">
      <br>
      <button onclick="shutdown_all()" type="button">Broadcast Shutdown</button>
      <button onclick="reboot_all()" type="button">Broadcast Reboot</button>
    </div>

    <script>discover()</script>
    <script>setInterval("discover()", 10000)</script>
  </body>
</html>
