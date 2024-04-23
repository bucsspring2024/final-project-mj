import pygame

class Image(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        """
        Initialize the image object
        Args:
            image_path str: path to img file
            position tuple: location of the image on the screen
        """
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.position = position