import pygame
import pygame_gui

class Image:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.position = position

    def draw(self, surface):
        pass
        # Implement the logic to draw the image on the surface

    def edit(self):
        pass
        # Implement the logic to edit the image