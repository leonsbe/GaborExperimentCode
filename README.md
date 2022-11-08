# GaborExperimentCode
The code in the repository enables the presentation of gabor patches in visual noise at different eccentricities and contrasts. Participant's are asked to fixate the center of the screen and 
press the response button when detecting a gabor patch. Response timings are logged paired with trial information. 

Requirements: psychopy and exptools2


### Usage

Modify expsettings.yml to specify screen and monitor setings, response button, gabor patch size, contrast values, number of trials, phase durations and more. 

Within an environment where exptools2 and psychopy are installed, navigate to the folder with the experiment filed and run:

``` python main.py sub-xxx ses-x ```

Insert subject number and session number. To quit the experiment press q. 
