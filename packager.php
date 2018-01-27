<?php
//Quickstore zip packager by pwsincd.
$apps = $_POST['data'];
$zip = new ZipArchive;
$date = date('m-d-Y_H:i:s');

if ($zip->open('appstore'.$date.'.zip', ZipArchive::CREATE) === TRUE) {
	$zip->addEmptyDir('wiiu/apps');
	foreach ($apps as $value) {
		$zip->addEmptyDir('wiiu/apps/'.$value['dir']);
    	$zip->addFile('../appstore/apps/'.$value['dir'].'/icon.png', 'wiiu/apps/'.$value['dir'].'/icon.png');
    	$zip->addFile('../appstore/apps/'.$value['dir'].'/meta.xml', 'wiiu/apps/'.$value['dir'].'/meta.xml');
    	$zip->addFile('../appstore/apps/'.$value['dir'].'/'.$value['binary'], 'wiiu/apps/'.$value['dir'].'/'.$value['binary']);
        if ($value['dir'] == "haxchi")
        {
            $zip->addEmptyDir('haxchi');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/haxchi/bootDrcTex.tga', 'haxchi/bootDrcTex.tga');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/haxchi/bootTvTex.tga', 'haxchi/bootTvTex.tga');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/haxchi/config.txt', 'haxchi/config.txt');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/haxchi/iconTex.tga', 'haxchi/iconTex.tga');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/haxchi/title.txt', 'haxchi/title.txt');
        }
        if ($value['dir'] == "cbhc")
        {
            $zip->addEmptyDir('cbhc');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/cbhc/bootDrcTex.tga', 'cbhc/bootDrcTex.tga');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/cbhc/bootTvTex.tga', 'cbhc/bootTvTex.tga');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/cbhc/config.txt', 'cbhc/config.txt');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/cbhc/iconTex.tga', 'cbhc/iconTex.tga');
            $zip->addFile('../appstore/apps/'.$value['dir'].'/sd/cbhc/title.txt', 'cbhc/title.txt');
        }
    }
    $zip->close();
    echo 'https://www.wiiubru.com/quickstore/appstore'.$date.'.zip';
} else {
    echo 'oops....something went wrong';
}
?>