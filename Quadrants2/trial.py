#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:06:36 2019

@author: marcoaqil
"""

from exptools2.core.trial import Trial
from psychopy import event
import os

opj = os.path.join


class GaborTrial(Trial):

    # using *args any number of extra arguments can be tacked on to the current parameters
    def __init__(self, session, trial_nr, phase_durations, phase_names, parameters, timing, Target_contrast, Target_position_x, Target_position_y,
                Distr1_position_x, Distr1_position_y, Distr2_position_x, Distr2_position_y, Distr3_position_x, Distr3_position_y, *args, **kwargs):

        #trial number and bar parameters
        self.trial_nr = trial_nr
        self.Target_contrast = Target_contrast
        self.position_x = Target_position_x
        self.position_y = Target_position_y
        self.session = session
        self.Target_position_x = Target_position_x
        self.Target_position_y = Target_position_y
        
        self.Distr1_position_x = Distr1_position_x
        self.Distr1_position_y = Distr1_position_y
        self.Distr2_position_x = Distr2_position_x
        self.Distr2_position_y = Distr2_position_y
        self.Distr3_position_x = Distr3_position_x
        self.Distr3_position_y = Distr3_position_y

        # run __init__ statements of parent class. this modifies the passed parameters
        # QUESTION what happens first: binding the parameter to self or this modification?
        super().__init__(session, trial_nr, phase_durations, phase_names,
                        parameters, timing,
                        *args,
                        **kwargs )


    # this is drawn by parent method of Trial .run(), in session
    # why draw statements not here?
    def draw(self, *args, **kwargs):
        self.session.fix_cross.draw()
        
        if self.phase == 0:
           self.session.draw_stimulus()
        elif self.phase == 1:
           self.session.draw_responseScreen()


    # run after every stimulus daw:
    def get_events(self):
        """ Logs responses/triggers """

        print("Get_events started")
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

            if self.phase == 1:
                self.exit_phase=True


            # loops over keys and their times
            for key, t in events:

                # count total responses
                self.session.total_responses += 1
                
                # distinguish responses and log
                if key == self.session.upleft or self.session.upright or self.session.lowleft or self.session.lowright:

                    # labels responses and adds one to the count
                    if self.phase == 1:
                        event_type = 'valid response'
                        self.session.valid_responses += 1
                    else:
                        event_type = 'outise of response screen'
                else: 
                    self.session.wrongkeypresses += 1
                    print(f"Wrong button pressed: {key}")
                    
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

                # log wherre the patch appeared and whether response was correct
                # upleft (-3,3)
                if self.position_x == self.session.settings['Stimulus settings']['Positions'][2] and self.position_y == self.session.settings['Stimulus settings']['Positions'][0]:
                    self.session.global_log.loc[idx, 'Quadrant'] = "Upper left"
                    if key == self.session.upleft:
                        self.session.global_log.loc[idx, 'Accuracy'] = 1
                        self.session.correct_responses += 1
                    else:
                        self.session.global_log.loc[idx, 'Accuracy'] = 0

                #upright (3,3)
                if self.position_x == self.session.settings['Stimulus settings']['Positions'][0] and self.position_y == self.session.settings['Stimulus settings']['Positions'][0]:
                    self.session.global_log.loc[idx, 'Quadrant'] = "Upper right"
                    if key == self.session.upright:
                        self.session.global_log.loc[idx, 'Accuracy'] = 1
                        self.session.correct_responses += 1
                    else:
                        self.session.global_log.loc[idx, 'Accuracy'] = 0

                #lowleft (-3,-3)
                if self.position_x == self.session.settings['Stimulus settings']['Positions'][2] and self.position_y == self.session.settings['Stimulus settings']['Positions'][2]:
                    self.session.global_log.loc[idx, 'Quadrant'] = "Lower left"
                    if key == self.session.lowleft:
                        self.session.global_log.loc[idx, 'Accuracy'] = 1
                        self.session.correct_responses += 1
                    else:
                        self.session.global_log.loc[idx, 'Accuracy'] = 0

                #lowright (3,-3)
                if self.position_x == self.session.settings['Stimulus settings']['Positions'][0] and self.position_y == self.session.settings['Stimulus settings']['Positions'][2]:
                    self.session.global_log.loc[idx, 'Quadrant'] = "Lower right"
                    if key == self.session.lowright:
                        self.session.global_log.loc[idx, 'Accuracy'] = 1
                        self.session.correct_responses += 1
                    else:
                        self.session.global_log.loc[idx, 'Accuracy'] = 0

                # if another parameter is given to this will also be logged
                for param, val in self.parameters.items():
                    self.session.global_log.loc[idx, param] = val

                # not sure why needed
                self.last_resp = key
                self.last_resp_onset = t

            
                    

        # implement something similar to check whether key was pressed during stimulus presentation?

        #update counter
        # dot count progresses so the calculation of percentage pressed and correct can be calculated
        #if self.session.dot_count < len(self.session.dot_switch_color_times):
        #    # if the current global time is larger than the time in which to respond, add a dot press
        #    if self.session.clock.getTime() > self.session.dot_switch_color_times[self.session.dot_count] + \
        #        float(self.session.settings['Task settings']['response interval'])+0.1: #to give time to respond
        #        self.session.dot_count += 1
        #        # print(f'dot count: {self.session.dot_count}') #testing
