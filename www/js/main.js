
function compile() {

  $("#output_section").html("Compiling...<br>");
  
  $.get("compile.php?"+ new Date(),
    function(data) {
      $("#output_section").append(data);
    }
  );

}
