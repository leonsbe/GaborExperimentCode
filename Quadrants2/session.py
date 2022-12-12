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
from psychopy import visual, core

from exptools2.core.session import Session
from exptools2.core.eyetracker import PylinkEyetrackerSession
from trial import GaborTrial #from trial.py import PRFTrial, which is
from stim import StimulusClass

# used later to ensure path syntax is correct
opj = os.path.join


# creating a child class that inherits from exptools2 Session parent class
class GaborSession(PylinkEyetrackerSession):
    # init statements that are run automatically when an object is instantiated using this class
    def __init__(self, output_str, output_dir, settings_file, eyetracker_on=True): # initializes attributes passed as parameters when declaring an object using this class
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
        super().__init__(output_str=output_str, output_dir=output_dir, settings_file=settings_file, eyetracker_on=eyetracker_on)

        ## add some initialization statements specific for this experiment:

        # specify response key(s)
        #self.response_key = self.settings['Task settings']['Response key']
        self.upleft = self.settings['Task settings']['Upper left']
        self.upright = self.settings['Task settings']['Upper right']
        self.lowleft = self.settings['Task settings']['Lower left']
        self.lowright = self.settings['Task settings']['Lower right']

        
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
                    ori=0.0, pos=(0, 0), lineWidth=1.0, colorSpace='rgb',
                    lineColor='white', fillColor='white',
                    opacity=None, depth=0.0, interpolate=True)
        #anchor='center',

        ## END OF create_stimuli



    # New class method, run by default during initialization
    def create_trials(self):
        """creates trials by setting up prf stimulus sequence"""

        # used for live logging
        self.total_responses = 0
        self.valid_responses = 0
        self.wrongkeypresses = 0
        self.correct_responses = 0

        ## Create trial list Gabor task

        # Target contrast values for each trial
        self.contrastValuesTarget = np.linspace(self.settings['Stimulus settings']['lowest contrast'],self.settings['Stimulus settings']['highest contrast'],
                                         num= self.settings['Stimulus settings']['contrast steps'])
        self.contrastListTarget = np.resize(self.contrastValuesTarget, self.n_trials)
        random.shuffle(self.contrastListTarget)

        # Target and distractor position for each trial
        self.Target_position_x = np.resize(self.settings['Stimulus settings']['Positions'], self.n_trials)
        self.Target_position_y = np.resize(self.settings['Stimulus settings']['Positions'], self.n_trials)
        random.shuffle(self.Target_position_x)
        random.shuffle(self.Target_position_y)

        # Distractor position
        self.Distr1_position_x = []
        self.Distr1_position_y = []
        self.Distr2_position_x = []
        self.Distr2_position_y = []
        self.Distr3_position_x = []
        self.Distr3_position_y = []

        for p in range(self.n_trials):
            # Target top right
            if self.Target_position_x[p] == self.settings['Stimulus settings']['Positions'][0] and self.Target_position_y[p] == self.settings['Stimulus settings']['Positions'][0]:
              
                self.Distr1_position_x.append(self.settings['Stimulus settings']['Positions'][0])
                self.Distr1_position_y.append(self.settings['Stimulus settings']['Positions'][2])
                
                self.Distr2_position_x.append(self.settings['Stimulus settings']['Positions'][2])
                self.Distr2_position_y.append(self.settings['Stimulus settings']['Positions'][0])
                
                self.Distr3_position_x.append(self.settings['Stimulus settings']['Positions'][2])
                self.Distr3_position_y.append(self.settings['Stimulus settings']['Positions'][2])
            # Target bottom right
            elif self.Target_position_x[p] == self.settings['Stimulus settings']['Positions'][0] and self.Target_position_y[p] == self.settings['Stimulus settings']['Positions'][2]:
              
                self.Distr1_position_x.append(self.settings['Stimulus settings']['Positions'][0])
                self.Distr1_position_y.append(self.settings['Stimulus settings']['Positions'][0])
                
                self.Distr2_position_x.append(self.settings['Stimulus settings']['Positions'][2])
                self.Distr2_position_y.append(self.settings['Stimulus settings']['Positions'][0])
                
                self.Distr3_position_x.append(self.settings['Stimulus settings']['Positions'][2])
                self.Distr3_position_y.append(self.settings['Stimulus settings']['Positions'][2])
            # Target top left
            elif self.Target_position_x[p] == self.settings['Stimulus settings']['Positions'][2] and self.Target_position_y[p] == self.settings['Stimulus settings']['Positions'][0]:
              
                self.Distr1_position_x.append(self.settings['Stimulus settings']['Positions'][0])
                self.Distr1_position_y.append(self.settings['Stimulus settings']['Positions'][0])
                
                self.Distr2_position_x.append(self.settings['Stimulus settings']['Positions'][0])
                self.Distr2_position_y.append(self.settings['Stimulus settings']['Positions'][2])
                
                self.Distr3_position_x.append(self.settings['Stimulus settings']['Positions'][2])
                self.Distr3_position_y.append(self.settings['Stimulus settings']['Positions'][2])
            # Target bottom left
            elif self.Target_position_x[p] == self.settings['Stimulus settings']['Positions'][2] and self.Target_position_y[p] == self.settings['Stimulus settings']['Positions'][2]:
              
                self.Distr1_position_x.append(self.settings['Stimulus settings']['Positions'][0])
                self.Distr1_position_y.append(self.settings['Stimulus settings']['Positions'][0])
                
                self.Distr2_position_x.append(self.settings['Stimulus settings']['Positions'][0])
                self.Distr2_position_y.append(self.settings['Stimulus settings']['Positions'][2])
                
                self.Distr3_position_x.append(self.settings['Stimulus settings']['Positions'][2])
                self.Distr3_position_y.append(self.settings['Stimulus settings']['Positions'][0])
       
              

        ## Create trial list
        self.trial_list=[]
        # this trial list will be used in a loop of the .run function to define the current trials parameters
        for i in range(self.n_trials):
            self.trial_list.append(GaborTrial(session=self,
                                           trial_nr=i,
                                           phase_durations=self.settings['Task settings']['phase durations'],
                                           timing = self.settings['Task settings']['phase unit'],
                                           phase_names=('Stimulus', 'Response'),
                                           parameters={'contrast': self.contrastListTarget[i], 'x_posT': self.Target_position_x[i], 'y_posT': self.Target_position_x[i]},
                                           Target_contrast = self.contrastListTarget[i],
                                           Target_position_x = self.Target_position_x[i],
                                           Target_position_y = self.Target_position_y[i],
                                           Distr1_position_x = self.Distr1_position_x[i],
                                           Distr1_position_y = self.Distr1_position_y[i],
                                           Distr2_position_x = self.Distr2_position_x[i],
                                           Distr2_position_y = self.Distr2_position_y[i],
                                           Distr3_position_x = self.Distr3_position_x[i],
                                           Distr3_position_y = self.Distr3_position_y[i]))


        ## TESTING
        print(f' create_trials: The first target is at {self.Target_position_x[0]}/{self.Target_position_y[0]} with contrast {self.contrastListTarget[0]}')
        print(f' create_trials: First trial Distractor 1 position: {self.Distr1_position_x[0]}/{self.Distr1_position_y[0]}')
        print(f' create_trials: First trial Distractor 2 position: {self.Distr2_position_x[0]}/{self.Distr2_position_y[0]}')
        print(f' create_trials: First trial Distractor 3 position: {self.Distr3_position_x[0]}/{self.Distr3_position_y[0]}')


        print(f' create_trials: The second target is at {self.Target_position_x[1]}/{self.Target_position_y[1]} with contrast {self.contrastListTarget[1]}')
        print(f' create_trials: Second trial Distractor 1 position: {self.Distr1_position_x[1]}/{self.Distr1_position_y[1]}')
        print(f' create_trials: Second trial Distractor 2 position: {self.Distr2_position_x[1]}/{self.Distr2_position_y[1]}')
        print(f' create_trials: First trial Distractor 3 position: {self.Distr3_position_x[1]}/{self.Distr3_position_y[1]}')



        #only for testing purposes
        # saves switch times to a file and prints window size
        #np.save(opj(self.output_dir, self.output_str+'_DotSwitchColorTimes.npy'), self.dot_switch_color_times)
        #print(self.win.size)

        ## END OF create_trials



    # this method is called by the .draw method of trial class objects. That .draw method is called by the trial parent method .run, which itself is executed for every trial below in a loop that goes over the trial
    def draw_stimulus(self):
        """ called by stim draw method if phase ==0, sets current trial parameters and draws stimuli """

        ## calling to draw method of stim object
        # current trial with attribute specifying contrast and position is defined when .run is executed below
        self.present_time = self.clock.getTime()
        core.wait(1)
        self.stim.draw(Target_position_x = self.current_trial.Target_position_x,
                       Target_position_y = self.current_trial.Target_position_y,
                       Target_contrast = self.current_trial.Target_contrast,
                       Distr1_position_x = self.current_trial.Distr1_position_x,
                       Distr1_position_y = self.current_trial.Distr1_position_y,
                       Distr2_position_x = self.current_trial.Distr2_position_x,
                       Distr2_position_y = self.current_trial.Distr2_position_y,
                       Distr3_position_x = self.current_trial.Distr3_position_x,
                       Distr3_position_y = self.current_trial.Distr3_position_y)

        ## END OF draw_stimulus


    def draw_responseScreen(self):
        """ called by stim draw method if phase == 1 """
        #self.display_text(f'ITI of trial {self.current_trial.trial_nr}', duration=(0.1))
        #self.text_drawtest_ITI.draw()
        self.present_time = self.clock.getTime()

        self.display_text('Now indicate the position of the stimuli with the highest contrast. If you are unsure, make a guess. \nNumPad 4: Top left \nNumPad 5: Top right \nNumPad 1: Bottom left \nNumPad2: Bottom right \n\n When ready to continue with the next trial press SPACEBAR',
                         keys = 'space ', pos = (0,-0.4), units = "norm", height = 0.06)

        #duration = self.settings['Task settings']['phase durations'][1]
        ## END OF draw_ITI



   # New method called by main.py
    def run(self):
        """loop over trials"""

        if self.eyetracker_on:
            self.calibrate_eyetracker()

        # parent method that draws and flips text, defines key to continue
        self.fix_cross.draw()
        self.display_text('You will be shown four circles with varying contrast. You will then be asked to indicate which stimuli had the highest contrast (most visible). Please maintain your gaze on the fixation cross at the center of the screen. \n\n Press SPACEBAR when you are ready to start',
                         keys= 'space', pos = (0,-0.4), units = "norm", height = 0.06 )

        # parent method, includes timing parameters, optional wait times
        self.start_experiment()

        if self.eyetracker_on:
            self.start_recording_eyetracker()

        # show fixation cross and wait one second
        self.fix_cross.draw()
        

        ## Actually loading current trial and drawing it
        # loops over trial list, saves trial start time and draws the stimuli of current trial
        for trial_idx in range(len(self.trial_list)):
            self.current_trial = self.trial_list[trial_idx]
            self.current_trial_start_time = self.clock.getTime()
            self.current_trial.run()
            if self.settings['Task settings']['Screenshots']==True:
                            self.win.getMovieFrame()

        ## Check whether distractor task was followed
        # CHECK AGAIN FOR LOGGING
        # print for experimenter how many responses were expected and given
        #print(f"Expected number of responses: {len(self.dot_switch_color_times)}")
        print(f"Total subject responses: {self.total_responses}")
        print(f"Valid responses {self.valid_responses}")
        print(f"Correct responses {self.correct_responses}")
        print(f"Wrong key presses: {self.wrongkeypresses}")
        if self.settings['Stimulus settings']['Screenshot']==True:
            self.win.saveMovieFrames(opj(self.screen_dir, self.output_str+'_Screenshot.png'))

        self.close()
        # LOOK AT THIS AGAIN WHEN UNDERSTANDING LOGGING

        ## END OF run
