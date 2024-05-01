import pygame
import pygame_gui
import os
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
        self.size = settings[1]
        fonts = [f.rsplit('.')[0] for f in os.listdir('assets') if f.endswith('.ttf')]
        for font in fonts:
            if font == settings[2]:
                self.font = ImageFont.truetype(f'assets/{font}.ttf', self.size)
                self.bbox = self.font.getbbox(self.text)
        self.color = (settings[3].r, settings[3].g, settings[3].b, settings[3].a)

        # file = "assets/testimage.png"
        self.image = Image.new("RGBA", (consts.length, consts.width), (255, 255, 255, 0))
        
        self.position = position
        
        

    def create(self):
        """
        Create the text object as an image
        """
        # create text object onto Text image
        self.text_object = ImageDraw.Draw(self.image, "RGBA")
        # create text with given font, size, and color
        self.text_object.text((0, 0), self.text, font=self.font, fill=self.color)
        self.image = self.image.crop(self.bbox)
        
        self.text_object = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode).convert_alpha()
        self.rect = self.text_object.get_rect()
        self.rect.topleft = self.position
        
        self.image = self.text_object

# TODO: Creation of text using PIL / pygame; save this text as an image then load it into the object