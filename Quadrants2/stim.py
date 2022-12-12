
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:07:02 2019

@author: marcoaqil
"""
from psychopy import visual
from psychopy import tools

# creates new PRFStim class, object inheritance redundant I think
class StimulusClass(object):  
    def __init__(self, session, gabor_size, **kwargs):
        
        
        # bind parameters to self, so they describe the current instance of the classobject
        self.session = session
        self.gabor_size = gabor_size
        
        # grating stim 
        self.gratingTarget = visual.GratingStim(
            win=self.session.win, name='grating', units='deg',
            tex='sin', mask='gauss', 
            ori=0.0, sf= 1 / self.gabor_size, phase=0.0, size = self.gabor_size,
            color=[1,1,1], colorSpace='rgb',
            opacity=1.0, blendmode='avg',
            texRes=512.0, interpolate=True, depth=-1.0)

        self.distractors = []

        for i in range(3):
            self.distractors.append(visual.GratingStim(
            win=self.session.win, name='grating', units='deg',
            tex='sin', mask='gauss', contrast = 0.2,
            ori=0.0, sf= 1 / self.gabor_size, phase=0.0, size = self.gabor_size,
            color=[1,1,1], colorSpace='rgb',
            opacity=1.0, blendmode='avg',
            texRes=512.0, interpolate=True, depth=-1.0))

#anchor='center',

    
    # Draw a grating depending on the current trials contrast and position, which is passed from session
    # also draw distractors based on passed position
    def draw(self, Target_contrast, Target_position_x, Target_position_y, Distr1_position_x,Distr1_position_y, Distr2_position_x,Distr2_position_y, Distr3_position_x, Distr3_position_y):
        
        # Target
        self.gratingTarget.contrast = Target_contrast
        self.gratingTarget.setPos([Target_position_x, Target_position_y]) 
        self.gratingTarget.draw()

        # Distractors
        Distractor1 = self.distractors[0]
        Distractor2 = self.distractors[1]
        Distractor3 = self.distractors[2]

        Distractor1.setPos([Distr1_position_x, Distr1_position_y])
        Distractor2.setPos([Distr2_position_x, Distr2_position_y])
        Distractor3.setPos([Distr3_position_x, Distr3_position_y])

        Distractor1.draw()
        print(f"Distractor 1 drawn at position {Distr1_position_x}/{Distr1_position_y}")
        Distractor2.draw()
        print(f"Distractor 2 drawn at position {Distr2_position_x}/{Distr2_position_y}")
        Distractor3.draw()
        print(f"Distractor 3 drawn at position {Distr3_position_x}/{Distr3_position_y}")

        

        





    


