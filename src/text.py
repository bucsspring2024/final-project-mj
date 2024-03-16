import pygame
import pygame_gui

class Text(pygame.sprite.Sprite):
    def __init__(self, text, position):
        self.text = text
        self.position = position

    def draw(self, surface):
        pass
        # Implement the logic to draw the text on the surface

    def edit(self):
        pass
        # Implement the logic to edit the text