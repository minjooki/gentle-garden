import pygame
# import subprocess, threading, time

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = -1
        pygame.mixer.music.load(path)
    
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)
    
    def stop(self):
        pygame.mixer.music.stop()
