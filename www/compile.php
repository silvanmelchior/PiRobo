<?php

  $source = "/home/pi/usercode";
  $target = "/home/pi/build";
  $main = "main.c";
  $includes = "inc";
  
  # copy data
  $dir = opendir($source);
  while(false !== ($file = readdir($dir))) {
    if(($file != '.') && ($file != '..')) {
      if(!is_dir($source . '/' . $file) ) {
        if($file != $includes) {
          copy($source . '/' . $file, $target . '/' . $file);
        }
      }
    }
  }
  
  # compile
  $res = shell_exec("gcc -pthread -o $target/main $target/main.c $target/inc/pirobo.c 2>&1");
  if($res == "") echo "Compilation successful!";
  else echo $res;

?>
