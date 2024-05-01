import pygame

class Utility:
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h
        self.framerate = 60