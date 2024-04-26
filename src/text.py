import pygame
import pygame_gui

class Text(pygame.sprite.Sprite):
    def __init__(self, settings, position):
        """
        Initialize the text object

        Args:
            text str: the text to be displayed
            position tuple: location of the text on the screen
        """
        super().__init__()
        
        # self.text = settings[0]
        # self.font = settings[1]
        # self.size = settings[2]
        # self.color = settings[3]
        file = "assets/testimage.png"
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.center = position
        



# TODO: Creation of text using PIL / pygame; save this text as an image then load it into the object