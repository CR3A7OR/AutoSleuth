use std::io; // Module for traits, helpers, and type definitions for core I/O functionality
use std::env; //Module for inspection and manipulation of the process’s environment
use std::io::{Read, Write};
extern crate reqwest;
extern crate static_vcruntime;
//use reqwest::StatusCode;
//use bytes::Bytes;
//use std::fs::OpenOptions;

// (c) 2022 Matthew
// This code is licensed under MIT license (see LICENSE.txt for details)


const CHUNK: usize = 1024 * 976;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    //access the command line arguments passed and collect into a Vector, store in variable ip
    let args: Vec<String> = std::env::args().collect();
    let ip = args.get(1).map(|s| s.to_owned()).unwrap_or(String::from("http://localhost:80"));
    let mut offset = 0;
    let name = &args[2];
    let mut buffer = vec![0u8; CHUNK];
    let mut errorflag = true;
    /*
    let mut file: Box<dyn std::io::Read> = if let Some(file_name) = args.get(3) {
        Box::new(OpenOptions::new().read(true).open(file_name)?)
    } else {
        Box::new(io::stdin())
    };
    */
    let mut input = 0;
    loop {
        // If error flag is true then no error has occured and new chunk offset can be read
        if errorflag {
            // io function returns a standard structure
            // . read() takes a mutable reference to fixed size buffer returns number of bytes read on success
            // match file.read(buffer.as_mut())
            input = match io::stdin().lock().read(&mut buffer) {
                Ok(0) => break,
                Ok(x) => x,
                Err(_) => break,
            };
        } else {};

        // HTTP CODE
        // Formulate and send POST request to be made parsing in the data, offset & name string query
        let client = reqwest::blocking::Client::new();
        let res = client.post(&ip)
            .body(Vec::from(&buffer[..input]))
            .query(&[("offset", offset.to_string().as_str()) , ("name", name.to_string().as_str())])
            .send();

        match res {
            //Try read response from request
            Ok(res) => {
                // If response is 200 OK increment offset and turn set error checking to not intervene
                if res.status().is_success() {
                    println!("{}", res.status());
                    offset += input;
                    errorflag = true;
                }  else if res.status().is_server_error() {
                    println!("Server Error!");
                    break;
                } else {
                    println!("ERROR: Status: {:?}", res.status());
                    break;
                }
            },
            // If response can't be read / timeout then set error flag to false meaning no new chunks will be read
            Err(_e) => {
                eprintln!("{:?}", _e);
		        errorflag = false;
            },
        };
        //offset += input;

    }
    eprintln!("Total bytes read: {}", offset);
    Ok(())
}
