<?php

  class FileDB {
  
    public function __construct() {
      if(!file_exists($this->teams_file) || !file_exists($this->tasks_file)) {
        echo "Scoreboard not initialized";
        die();
      }
      // Tasks
      $tasks_data = preg_split('/\r\n|\n|\r/', trim(file_get_contents($this->tasks_file)));
      for($i=0; $i<count($tasks_data); $i++) {
        $this->tasks[$i] = explode(';', $tasks_data[$i]);
      }
      // Teams
      $teams_data = preg_split('/\r\n|\n|\r/', trim(file_get_contents($this->teams_file)));
      for($i=0; $i<count($teams_data); $i++) {
        $this->teams[$i] = explode(';', $teams_data[$i]);
      }
      // Points
      if(!file_exists($this->points_file)) {
        for($i=0; $i<count($teams_data); $i++) {
          $this->points[$i] = array();
          for($j=0; $j<count($tasks_data); $j++) {
            $this->points[$i][$j] = 0;
          }
        }
        $this->save_points();
      }
      else {
        $points_data = preg_split('/\r\n|\n|\r/', trim(file_get_contents($this->points_file)));
        for($i=0; $i<count($this->teams); $i++) {
          $this->points[$i] = explode(';', $points_data[$i]);
          for($j=0; $j<count($this->tasks); $j++) {
            $this->points[$i][$j] = $this->points[$i][$j]*1;
          }
        }
      }

    }

    public function set_state($team_id, $task_id, $value) {
      if($value) $this->points[$team_id][$task_id] = 1;
      else $this->points[$team_id][$task_id] = 0;
      $this->save_points();
    }
    
    public function get_state() {
      return $this->points;
    }

    public function get_tasks() {
      return $this->tasks;
    }

    public function get_teams() {
      return $this->teams;
    }

    private function save_points() {
      $str_points = "";
      for($i=0; $i<count($this->teams); $i++) {
        for($j=0; $j<count($this->tasks); $j++) {
          if($j != 0) $str_points .= ';';
          $str_points .= strval($this->points[$i][$j]);
        }
        $str_points .= "\n";
      }
      file_put_contents($this->points_file, $str_points);
    }
    
    private $teams_file = "data/teams.txt";
    private $tasks_file = "data/tasks.txt";
    private $points_file = "data/points.txt";
    private $tasks = array();
    private $teams = array();
    private $points = array();
    public $id_name = 0;
    public $id_points = 1;
    public $id_code = 2;
  
  }
  
?>
