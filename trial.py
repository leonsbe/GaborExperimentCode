#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:06:36 2019

@author: marcoaqil
"""

from exptools2.core.trial import Trial
from psychopy import event
import numpy as np
import os

opj = os.path.join


class GaborTrial(Trial):
    
    # using *args any number of extra arguments can be tacked on to the current parameters
    def __init__(self, session, trial_nr, phase_durations, phase_names, parameters, timing, contrast, position_x, position_y, *args, **kwargs):
        
        #trial number and bar parameters   
        self.trial_nr = trial_nr
        self.contrast=contrast
        self.position_x = position_x
        self.position_y = position_y
        self.session=session
        
        # run __init__ statements of parent class. this modifies the passed parameters
        # QUESTION what happens first: binding the parameter to self or this modification?
        super().__init__(session, trial_nr, phase_durations, phase_names,
                        parameters, timing,
                        *args,
                        **kwargs )
            
        
    # this is drawn by parent method of Trial .run(), in session
    # why draw statements not here?
    def draw(self, *args, **kwargs):
        if self.phase == 0:  
           self.session.draw_ITI()
        else:  
           self.session.draw_stimulus()
                 
    
    # redefine get_events method, run after every stimulus daw
    def get_events(self):
        """ Logs responses/triggers """
        
        if self.phase == 1:
            # creates list of keys that were pressed
            events = event.getKeys(timeStamped=self.session.clock)
            
            if events: 
                # if q is pressed, save screenshots end the experiment
                # maybe add back logging the amount of button presses?
                if 'q' in [ev[0] for ev in events]:  # specific key in settings?
    
                    if self.session.settings['Task settings']['Screenshots']==True:
                        self.session.win.saveMovieFrames(opj(self.session.screen_dir, self.session.output_str+'_Screenshot.png'))
                         
                    self.session.close()
                    self.session.quit()
     
        
                # loops over keys and their times
                for key, t in events:
                    
                    if key == self.session.response_key:
                        
                        # labels responses and adds one to the count
                        event_type = 'response'
                        self.session.total_responses += 1
        
                        # for all key presses, get the number of rows in the log dataframe
                        # using the amount of rows, we refer to the next row and create a new column
                        # global_log is a pd DataFrame with columns as below
                        idx = self.session.global_log.shape[0]
                        self.session.global_log.loc[idx, 'trial_nr'] = self.trial_nr
                        self.session.global_log.loc[idx, 'onset'] = t
                        self.session.global_log.loc[idx, 'event_type'] = event_type
                        self.session.global_log.loc[idx, 'phase'] = self.phase
                        self.session.global_log.loc[idx, 'response'] = key
         
                        # if another parameter is given to this will also be logged
                        for param, val in self.parameters.items():
                            self.session.global_log.loc[idx, param] = val
                                            
                        # not sure why needed
                        self.last_resp = key
                        self.last_resp_onset = t
                    
                    else:
                        print(f"Wrong button pressed: {key}")
                        
            # implement something similar to check whether key was pressed during stimulus presentation?
            
            #update counter
            # dot count progresses so the calculation of percentage pressed and correct can be calculated
            #if self.session.dot_count < len(self.session.dot_switch_color_times): 
            #    # if the current global time is larger than the time in which to respond, add a dot press
            #    if self.session.clock.getTime() > self.session.dot_switch_color_times[self.session.dot_count] + \
            #        float(self.session.settings['Task settings']['response interval'])+0.1: #to give time to respond
            #        self.session.dot_count += 1   
            #        # print(f'dot count: {self.session.dot_count}') #testing
