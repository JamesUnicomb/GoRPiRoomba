import pygame, os, random

def playSound():
    pygame.mixer.init()
    soundfile = random.choice(os.listdir('sounds'))
    soundpath = os.path.join('sounds', soundfile)
    pygame.mixer.music.load(soundpath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
