#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 This script creates a pseudo serial ports using pseudoterminals
 It can be used to run sensor data from GPS or Vectornav
Authors: Jagatpreet Singh, Kris Dorsey, Arun Anbu
"""

import os, pty
from serial import Serial
import threading
import time 
import argparse

class SerialEmulator:
    
    def __init__(self,file, sample_time, loop_type):
        self.sample_time = sample_time  
        self.file = file 
        self.driver = None
        self.driven = None
        self.loop_type = loop_type
        
    def write_file_to_pt(self):
        f = open(self.file, 'r') 
        Lines = f.readlines()
        for line in Lines:
            write_string = line.rstrip() + '\r\n'
            write_bytes = str.encode(write_string, encoding='utf-8')
            os.write(self.driver, write_bytes)
            time.sleep(self.sample_time)
        f.close()
        print("Sensor emulator has reached the end of the file")
    
    def emulate_device(self):
        """Start the emulator"""
        self.driver,self.driven = pty.openpty() #open the pseudoterminal
        print("The Pseudo device address: %s"%os.ttyname(self.driven))
        try:
            self.write_file_to_pt()
            while self.loop_type == 'yes':
                print("Restarting...\n")
                self.write_file_to_pt()
            self.stop_simulator()
                
        except KeyboardInterrupt:
            self.stop_simulator()
            pass
    
    def start_emulator(self):
        self.emulate_device()

    def stop_simulator(self):
        os.close(self.driver)
        os.close(self.driven)
        print("Terminated")
        
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Command line options for Serial emulator.\
                                     Press Ctrl-C to stop execution')
    parser.add_argument('-f','--file', required=True, type=str, dest='file',
                    help='data file to simulate device')   

    parser.add_argument('-dev','--device_type', required = 'true', type=str, dest='device_type',
                    help="Device type must be 'gps', 'imu', or 'rtk'")
    
    parser.add_argument('-V','--VN_reg', default = b'$VNWRG,07,200*XX', type=str, dest='VN_reg',
                    help='Write register command for sample rate to pass to VN')
    
    parser.add_argument('-l','--loop', default = 'yes', type=str, dest='loop_behavior',
                    help="This should be 'yes' for looping ")
    
    args = parser.parse_args()
    valid_devices = ['gps','rtk','imu']

    try: 
        f = open(args.file, 'r') 
        time.sleep(0.1)
        f.close()   
        if args.device_type == 'gps':
            sample_rate = 5 #GPS pucks publish 5 nav sets every second
        elif args.device_type == 'rtk':
            sample_rate = 12 #RTK hardware publishes 12 nav sets every second
        elif args.device_type == 'imu':
            if type(args.VN_reg) == bytes:
                VN_reg = args.VN_reg.decode('utf-8')
            else:
                VN_reg = args.VN_reg
            VN_list = VN_reg.split(",")
            if (VN_list[0] == '$VNWRG'  and type(args.VN_reg) == bytes) or (VN_list[0] == 'b$VNWRG'  and type(args.VN_reg) == str) and VN_list[1] == '07':
                sample_rate = VN_list[2].split('*')
                sample_rate = float(sample_rate[0])
            
        print("Starting", args.device_type, "emulator with sample rate:", str(sample_rate), "Hz")
        se = SerialEmulator(args.file, 1/sample_rate, args.loop_behavior)
        se.start_emulator() 

    except FileNotFoundError:
        print("You did not specify the correct file name. Please try again.")
    except NameError:
        print("You did not specify the correct device type or VectorNav write register command. Please try again.")