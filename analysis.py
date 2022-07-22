#!/usr/bin/python3
# coding=utf-8

# (c) 2022 Matthew
# This code is licensed under MIT license (see LICENSE.txt for details)
import os
import threading
import subprocess
import random
import time
import re
import Builder.payloadBuilder

text = r""" 
 ______  AutoSleuth 0.0.1
| |__| | an automated tool for cloning partitions from a device 
|  ()  | maintained by CR3A7OR
|______| https://github.com/CR3A7OR

Select one:
[1] Build a rubber ducky
[2] Skip straight to analysis
[3] Quit"""

def startup():
    choice = input("  : ")
    if choice.isdigit() or choice != 1 or choice != 2 or choice != 3:
        if choice == '1': 
            Builder.payloadBuilder.builder()
            return True
        elif choice == '2':
            return True
        elif choice == '3':
            raise SystemExit(0)
    return False



def analysing_partition(file_name):
    while True:
        # Grab the file size of the file passed
        # Wait 10 seconds before attempting to grab the file size again
        file_size = os.stat(file_name)
        time.sleep(10)
        new_file_size = os.stat(file_name)
        # If the two file sizes are the same then it is safe to assume
        # the PHP code has received all data surrounding the file
        if (file_size.st_size == new_file_size.st_size):
            print("Building Report...")
            break
    try:
        filename = file_name.replace('.dd', '').replace('.img', '') + '.txt' #Generate file name
        # Generate file and write stdout into it 
        f = open(filename, "w")
        f.write("############ FSSTAT ############ \n")
        f.write("Command: fsstat " + file_name + "\n")
        # flush title to maintain intended structure of final report
        f.flush()
        # Subprocess called to run Sleuthkit command and send output to stdout to be written into file
        subprocess.call(['fsstat', file_name], stdout=f, stderr=f)

        f.write("\n ############ FLS (UN-DELETED) ############ \n")
        f.write("Command: fls -l -u -r " + file_name + "\n")
        f.flush()
        subprocess.call(['fls', '-l', '-u', '-r', file_name], stdout=f, stderr=f)

        f.write("\n ############ FLS (DELETED) ############ \n")
        f.write("Command: fls -l -d -r " + file_name + "\n")
        f.flush()
        subprocess.call(['fls', '-l', '-d', '-r', file_name], stdout=f, stderr=f)

        # RUNNING COMMANDS INPUTTED BY USER
        with open('commands.txt') as execute_file:
            for i,line in enumerate(execute_file):
                if (i != 0):
                    f.write("\nCUSTOM COMMAND " + str(i) + '\n')
                    line = line.strip('\n')
                    line = line.replace('IMAGE_FILE', file_name)
                    output_str2 = line.split()
                    f.write("Command: " + output_str2 + "\n")
                    f.flush()
                    subprocess.call([*output_str2], stdout=f, stderr=f)
        print("Analysis Complete")
    except:
        print("Analysis Failed")
    
    return 1


def main():
    print(text)
    start_call = False
    while not start_call:
        start_call = startup()
    print("Starting Up...")
    print("Waiting...")
    
    partition_list = [] # list of image files already found 
    threads = [] # list of active threads running
    #found = False
    while True:
        # Search through every file within directory passed or current working directory by default
        # If a file ends with .dd or .img extension and has not alread beem discovered 
        for fname in os.listdir():
            if (fname.endswith('.dd') or fname.endswith('.img')) and (fname not in partition_list):
                partition_list.append(fname)
                found = True
                print("Found: ", fname + "\nAnalysing...")
                # Start new thread for running the analysis of the file
                thread1 = threading.Thread(target=analysing_partition, args=(fname,))
                threads.append(thread1)
                thread1.start()


if __name__ == "__main__":
    main()
