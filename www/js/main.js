function compile() {

  $("#output_section").html("Compiling...<br>");
  
  $.get("compile.php?"+ new Date(),
    function(data) {
      $("#output_section").append(data);
    }
  );

}


function run() {

  $.get("run.php?"+ new Date());

}


function update_done(res) {

  var msg = JSON.parse(res)
  $("#output_section").html(msg.data);
  update(msg.hash);

}


function update(hash) {

  $.ajax({
    url: "status.php",
    data: "hash="+hash,
    success: update_done,
    error: function() {setTimeout("update('')", 2000)}
  });

}


update('');
