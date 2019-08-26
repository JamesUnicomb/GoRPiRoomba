#
# A module for playing sounds in the 'sounds' path
#

import pygame, os, sys, random
import os, sys

def playSound():
    pygame.mixer.init()
    
    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    sounds_path = os.path.join(script_path, 'sounds')
    
    #
    # Choose a random sound from the sounds folder.
    #
    sound_file = random.choice(os.listdir(sounds_path))
    sound_file = os.path.join(sounds_path, sound_file)
    
    #
    # Play the sound with pygame
    #
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
