<?php
$backups_dir = 'root/backups/';
$database_dir = "root/broker_bot/";

backup($database_dir, $backups_dir);

function clear_old_backups($backups_dir) {
    if (file_exists($backups_dir)) {
        $files = scandir($backups_dir);
        if ($files !== false) {
            foreach ($files as $file) {
                if ($file != "." && $file != "..") {
                    $date = explode('_', $file)[0];
                    if (strtotime($date) - strtotime(date('d-m-Y')) <= -2592000) {
                        @unlink($backups_dir.$file);
                    }
                }
            }
        }
    }
}

function backup($database_dir, $backups_dir) {
    @mkdir($backups_dir);
    clear_old_backups($backups_dir);
    $filename = $database_dir.'DataBase.sqlite3';
    print("Attempt to copy file: ".$filename.PHP_EOL);
    if (file_exists($filename)) {
        print('DataBase file exists!'.PHP_EOL);
        $time = date('d-m-Y');
        $new_filename = $time."_backup.sqlite3";
        $count = 1;
        while(file_exists($backups_dir.$new_filename)) {
            $new_filename = $time."_backup_".$count.".sqlite3";
            $count++;
        }
        if (copy($filename, $backups_dir.$new_filename)) {
            print('Backup successfully created!'.PHP_EOL);
        }else{
            print('Backup failed!'.PHP_EOL);
        }
        sleep(86400);
    }else{
        print('DataBase file does not exist! Next attempt in 30 seconds...'.PHP_EOL);
        sleep(30);
    }
    backup($database_dir, $backups_dir);
}