import pygame
import pygame_gui
from src.utility import Utility
from PIL import Image, ImageDraw, ImageFont

consts = Utility()

class Text(pygame.sprite.Sprite):
    def __init__(self, settings, position):
        """
        Initialize the text object

        Args:
            text str: the text to be displayed
            position tuple: location of the text on the screen
        """
        super().__init__()
        
        self.text = settings[0]
        self.font = settings[1]
        self.size = settings[2]
        self.color = settings[3]

        # file = "assets/testimage.png"
        self.image = Image.new("RGBA", (consts.length, consts.width), (255, 255, 255, 0))
        # self.rect = self.image.get_rect()
        # self.rect.center = position
        

    def create(self):
        """
        Create the text object
        """
        # create text object onto Text image
        self.text_object = ImageDraw.Draw(self.image, "RGBA")
        # create text with given font, size, and color
        self.text_object.text((0, 0), self.text, font=self.font, fill=self.color)
        # resize the image to fit the text's bounding box
        pass

# TODO: Creation of text using PIL / pygame; save this text as an image then load it into the object