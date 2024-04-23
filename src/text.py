import pygame
import pygame_gui

class Text(pygame.sprite.Sprite):
    def __init__(self, text, position):
        """
        Initialize the text object

        Args:
            text str: the text to be displayed
            position tuple: location of the text on the screen
        """
        self.text = text
        self.position = position