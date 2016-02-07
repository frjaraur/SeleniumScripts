#!/usr/bin/python3
import sys, getopt, ipaddress, os, re, socket

import threading
from queue import Queue

import numpy

import time
import subprocess

num_threads = 4

def do_Process(array_of_strings):
     # pretend to do some lengthy work.
    for string in array_of_strings:
        print ("STRING: "+string)
    
    # Make sure the whole print completes or threads can mix up output in one line.
    with lock:

        print (threading.current_thread().name, '[%s]' % ', '.join(map(str, ipaddresses))) 

# The worker thread pulls an item from the queue and processes it
def MainProcess(q, array_of_strings):
    while True:
        array_of_strings = q.get()
        do_Process(array_of_strings)
        q.task_done()


test_array=["uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve","diez"]


def main(argv):

        if test_array > num_threads :
            chunks = numpy.array_split(test_array, num_threads)
            # chunk_array(10, myips)
            q = Queue()
            for chunk in hunks: 
                t = threading.Thread(target=MainProcess, args=(q, chunk))
                t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
                t.start()
            
            for chunk in chunks:             
                q.put(ipchunk)
                    
            q.join() 
           # for ip in ipchunk: 
           #     print ("IP --> "+str(ip))
        else:
            # Discover one IP
            for ip in myips: 
                ADAMDiscover(ip)
                


if __name__ == "__main__":
    main(sys.argv[1:])

