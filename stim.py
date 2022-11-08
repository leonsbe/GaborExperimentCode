
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
        self.grating = visual.GratingStim(
            win=self.session.win, name='grating', units='deg',
            tex='sin', mask='gauss', anchor='center',
            ori=0.0, sf= 5.0 / self.gabor_size, phase=0.0, size = self.gabor_size,
            color=[1,1,1], colorSpace='rgb',
            opacity=1.0, blendmode='avg',
            texRes=512.0, interpolate=True, depth=-1.0)


    
    # Draw a grating depending on the current trials contrast and position, which is passed from session
    # Could make it work through duration instead
    def draw(self, position_x, position_y, present_time, contrast):
        self.grating.contrast = contrast
        self.grating.setPos([position_x, position_y]) 
        self.grating.draw()
        

        

        





    


