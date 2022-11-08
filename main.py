#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:04:44 2019

@author: marcoaqil
"""
import sys # access command line arguments when experiment is run
import os # used to concatenate folders in path creation
from session import GaborSession # Imports session object class 
from datetime import datetime # to get current date and time
datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create function that is used to run the experiment
# sys.argv[1] will refer to the first command line argument that is passed to this script (python main.py sub-xxx ses-x task-NameTask run-x)
# So it's getting the sess, task and run based on filename, which is specified by user
def main():
    subject = sys.argv[1]
    sess =  sys.argv[2]
    
    # define specific output string for this session
    # session.py calles to this and attaches a string at the end
    output_str= subject+'_'+sess
    
    # define directory to save to, uses just defined string (this will later be used by )
    output_dir = './'+output_str+'_Logs'
    
    # checks if directory already exists, if yes renames with current time and date
    if os.path.exists(output_dir):
        print("Warning: output directory already exists. Renaming to avoid overwriting.")
        output_dir = output_dir + datetime.now().strftime('%Y%m%d%H%M%S')
    
    # sets setting file variable
    settings_file='./expsettings.yml'

    # instantiates session class and passes output parameters and settings file
    ts = GaborSession(output_str=output_str, output_dir=output_dir, settings_file=settings_file)

    # executes run method of Session which runs the whole experiment
    ts.run()
    
# runs the current file
if __name__ == '__main__':
    main()

# Instead of "python main.py sub-xxx ses-x task-NameTask run-x" I shortened it to "python main.py sub-xxx ses-x"