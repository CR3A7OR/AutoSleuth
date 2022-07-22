<?php
// (c) 2022 Matthew
// This code is licensed under MIT license (see LICENSE.txt for details)

// function with a whitelist regex to only allow specific characters and any outside are replaced with a dash
function clean($string) {
    return preg_replace('/[^A-Za-z0-9\. -]/', '-', $string);
}

//Collect the offset and name from string query in request
$name = clean($_GET["name"]);
$offset = $_GET["offset"];
$data = file_get_contents('php://input');
//$length = (int) $_SERVER['CONTENT_LENGTH'];
$length = strlen($data);
$path = getcwd() . $name;

//Open offset.txt and store the previous offset saved to check against new one received
$fileoffset = fopen("offset.txt", "r");
if(filesize("offset.txt") > 0) {
	$poffset = fread($fileoffset, filesize("offset.txt"));
} 
else{$poffset = 0;}

//If previous offset of last packet is 65536 bytes less (or this is first packet)
if (intval($poffset) == (intval($offset) - 65536) || intval($offset) == 0) {
    //Update the offset value  
    file_put_contents('offset.txt', $offset);
    
    // Open or Create file using now clean name (a - Write only / b - Opens file as raw binary) 
    $file = fopen($name, "ab");
    // Lock the file exclusivly so no other threads can use it 
    if (flock($file, LOCK_EX)) {
        //Write 1MB of data chunks to file until all data from requests length is read and written
        if (filesize($name) == intval($offset)) {
            $CHUNK_SIZE = 1024 * 1024;
            $read = 0;
            while ($read < $length) {
                $to_size = min($CHUNK_SIZE, $length - $read);
                fwrite($file, $data ,$to_size);
                $read = intval($read) + intval($to_size);
            }
            //release lock and flush content to file
            fflush($file);
            flock($file, LOCK_UN);
        }
    }
    fclose($file);
    
    //http_response_code(200);

}
else {http_response_code(404);}

?>