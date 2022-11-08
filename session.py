#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:05:10 2019

@author: marcoaqil
"""
# Importing packages
import numpy as np
import os
import random
from psychopy import visual

from exptools2.core.session import Session 
from trial import GaborTrial #from trial.py import PRFTrial, which is
from stim import StimulusClass

# used later to ensure path syntax is correct
opj = os.path.join


# creating a child class that inherits from exptools2 Session parent class 
class GaborSession(Session):
    # init statements that are run automatically when an object is instantiated using this class
    def __init__(self, output_str, output_dir, settings_file): # initializes attributes passed as parameters when declaring an object using this class
        """
        Parameters
        ----------
        output_str : str
            Basename for all output-files (like logs), e.g., "sub-01_task-stroop_run-1"
        output_dir : str
            Path to desired output-directory (default: None, which results in $pwd/logs)
        settings_file : str
            Path to yaml-file with settings (default: None, which results in the package's
            default settings file (in data/default_settings.yml)
        """

        # initialize parent class statements
        super().__init__(output_str=output_str, output_dir=output_dir, settings_file=settings_file) 
        
        ## add some initialization statements specific for this experiment:
        
        # specify response key
        self.response_key = self.settings['Task settings']['Response key']
        
        # if screenshots are wanted, set screenshot directory 
        if self.settings['Task settings']['Screenshots']==True: 
            self.screen_dir=output_dir+'/'+output_str+'_Screenshots' 
            if not os.path.exists(self.screen_dir):  
                os.mkdir(self.screen_dir)
             
        # number of trials, should be divisible by amount of contrast
        self.n_trials = self.settings['Task settings']['number of trials']
        print(f' This run includes {self.n_trials} trials')
             
        # Creating stimuli and trials in the beginning, ensures that stimuli and trial related calculations are not made everytime we draw something
        self.create_stimuli()
        self.create_trials()  
        
        ## END OF __init__
    
    
    
    # New class method, run by default during initialization
    def create_stimuli(self):
        """generates Gabor stimuli by instantiating PRFStim class object"""

        ## Create Gabor patch
        # refers back to this session, so stim objects have access to Session methods and attributes like win
        self.stim = StimulusClass(session=self, gabor_size = self.settings['Stimulus settings']['Size gabor patch in degrees'])
        
        ## Create fixation cross 
        self.fix_cross = visual.ShapeStim(win=self.win, vertices='cross',units='deg', 
                    size=self.settings['Stimulus settings']['fixation cross size in degrees'],
                    ori=0.0, pos=(0, 0), anchor='center', lineWidth=1.0, colorSpace='rgb',
                    lineColor='white', fillColor='white',
                    opacity=None, depth=0.0, interpolate=True)
        
        ## Create white noise (make parameters in settings file)
        self.noise = visual.NoiseStim(
                    win=self.win, name='noise',units='norm', 
                    noiseImage=None, mask=None,
                    ori=0.0, pos=(0, 0), size=(2, 2), sf=None,
                    phase=0.0,
                    color=[1,1,1], colorSpace='rgb',     opacity=None, blendmode='avg', contrast=1.0,
                    texRes=256, filter=None,
                    noiseType='White', noiseElementSize=[0.000000001], 
                    noiseBaseSf=8.0, noiseBW=1.0,
                    noiseBWO=30.0, noiseOri=0.0,
                    noiseFractalPower=0.0,noiseFilterLower=1.0,
                    noiseFilterUpper=8.0, noiseFilterOrder=0.0,
                    noiseClip=3.0, imageComponent='Amplitude', interpolate=False, depth=0.0)
        
        # build here but refresh in draw chain
        self.noise.buildNoise()

        ## END OF create_stimuli



    # New class method, run by default during initialization
    def create_trials(self):
        """creates trials by setting up prf stimulus sequence""" 
        
        # used for logging
        self.total_responses = 0

        ## Create trial list Gabor task
        
        # create contrast values
        self.contrast = np.resize(self.settings['Stimulus settings']['contrast values'], self.n_trials)
        random.shuffle(self.contrast)
        
        # create position values REWORK TO MAKE 3 ECCENTRICITIES
        #degree units (potentially use degFlatPos to account for screen pixel change?)
        self.position_x = np.random.uniform(-5, 5, size=(self.n_trials))
        self.position_y = np.random.uniform(-5, 5, size=(self.n_trials))
        
        ## Create trial list
        self.trial_list=[]
        # this trial list will be used in a loop of the .run function to define the current trials parameters
        for i in range(self.n_trials):
            self.trial_list.append(GaborTrial(session=self,
                                           trial_nr=i,
                                           phase_durations=self.settings['Task settings']['phase durations'],
                                           timing = self.settings['Task settings']['phase unit'],
                                           phase_names=('ITI', 'stim'),
                                           parameters={'contrast': self.contrast[i], 'x_pos': self.position_x[i], 'y_pos': self.position_y[i]},
                                           contrast = self.contrast[i],
                                           position_x = self.position_x[i], 
                                           position_y = self.position_y[i]))
        
            
      
        # previously the code did some live analysis of correct detections, I don't think I need that
        # I might want to track total amount of responses and print this to the experimenter
        
        #only for testing purposes
        # saves switch times to a file and prints window size
        #np.save(opj(self.output_dir, self.output_str+'_DotSwitchColorTimes.npy'), self.dot_switch_color_times)
        #print(self.win.size)

        ## END OF create_trials


  
    # this method is called by the .draw method of trial class objects. That .draw method is called by the trial parent method .run, which itself is executed for every trial below in a loop that goes over the trial
    def draw_stimulus(self):
        """ part of draw chain, sets current trial parameters and draws stimuli """
        
        ## calling to draw method of stim object
        # current trial with attribute specifying contrast and position is defined when .run is executed below
        self.present_time = self.clock.getTime()
        
        #self.noise.updateNoise()
        
        self.fix_cross.draw()
        self.stim.draw(position_x = self.current_trial.position_x,
                       position_y = self.current_trial.position_y,
                       contrast = self.current_trial.contrast,
                       present_time = self.present_time)
        ## END OF draw_stimulus
    
    
    def draw_ITI(self):
        """ called by stim draw method if phase == 0 """
        #self.display_text(f'ITI of trial {self.current_trial.trial_nr}', duration=(0.1))
        #self.text_drawtest_ITI.draw()
        self.present_time = self.clock.getTime()
        
        #self.noise.updateNoise()
        
        self.fix_cross.draw()
        #self.noise.updateNoise()

        ## END OF draw_ITI

    

   # New method called by main.py
    def run(self):
        """loop over trials"""
        
        # parent method that draws and flips text, defines key to continue
        self.display_text('Press SPACEBAR to start', keys= 'space')
        
        # parent method, includes timing parameters, optional wait times
        self.start_experiment()
        
        
        ## Actually loading current trial and drawing it
        # loops over trial list, saves trial start time and draws the stimuli of current trial
        # saves current trials start time but how does it not overwrite? CHECK LOGGING
        for trial_idx in range(len(self.trial_list)):
            self.current_trial = self.trial_list[trial_idx]
            self.current_trial_start_time = self.clock.getTime()
            self.current_trial.run() 
            
        ## Check whether distractor task was followed
        # CHECK AGAIN FOR LOGGING
        # print for experimenter how many responses were expected and given
        #print(f"Expected number of responses: {len(self.dot_switch_color_times)}")
        #print(f"Total subject responses: {self.total_responses}")
        #print(f"Correct responses (within {self.settings['Task settings']['response interval']}s of dot color change): {self.correct_responses}")
        # next these three numbers are saved to a file in the directory
        # creates numpy array with expected number of responses, total responses and correct responses
        #np.save(opj(self.output_dir, self.output_str+'_simple_response_data.npy'), {"Expected number of responses":len(self.dot_switch_color_times),
        #														                      "Total subject responses":self.total_responses,
        #														                      f"Correct responses (within {self.settings['Task settings']['response interval']}s of dot color change)":self.correct_responses})
        #print('Percentage of correctly answered trials: %.2f%%'%(100*self.correct_responses/len(self.dot_switch_color_times)))
        
        # Psychopy function to save frames I think
        # LOOK AT THIS AGAIN WHEN UNDERSTANDING LOGGING
        if self.settings['Stimulus settings']['Screenshot']==True:
            self.win.saveMovieFrames(opj(self.screen_dir, self.output_str+'_Screenshot.png'))
            
        self.close()
        # LOOK AT THIS AGAIN WHEN UNDERSTANDING LOGGING

        ## END OF run

        

