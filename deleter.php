<?php
//Find all files that are .zip's in the quickstore directory's subdirs.
$files = glob('/home/wiiubru/public_html/quickstore/*.zip');
foreach ($files as $file) {
$x = 900;
//timestamp
$current_time = time();
//file timestamp
$file_creation_time = filemtime($file);
//extract difference
$difference = $current_time - $file_creation_time;
//if difference = $x...then delete file
if ($difference >= $x) {
unlink($file);
}//EndIf
}//EndForeach
?>