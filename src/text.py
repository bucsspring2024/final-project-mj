import pygame
import os
from PIL import Image, ImageDraw, ImageFont

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
        self.pil_image = Image.new("RGBA", (1080, 1080), (255, 255, 255, 0)) # placeholder dimensions, transparent background
        
        self.position = position
        
        

    def create(self):
        """
        Create the text object as an image
        """
        # create text object onto Text image
        self.text_object = ImageDraw.Draw(self.pil_image, "RGBA")
        # create text with given font, size, and color
        self.text_object.text((0, 0), self.text, font=self.font, fill=self.color)
        self.pil_image = self.pil_image.crop(self.bbox)
        
        self.text_object = pygame.image.fromstring(self.pil_image.tobytes(), self.pil_image.size, self.pil_image.mode).convert_alpha()
        self.image = self.text_object
        self.rect = self.text_object.get_rect()
        self.rect.topleft = self.position

    def scale(self, w, h):
        """
        Scale the text
        
        Args:
            w float: width of the text
            h float: height of the text
        """
        self.pil_image = self.pil_image.resize((round(w), round(h)))
        self.text_object = pygame.image.fromstring(self.pil_image.tobytes(), self.pil_image.size, self.pil_image.mode).convert_alpha()
        self.image = self.text_object
        self.rect.width, self.rect.height = self.image.get_size()

    def move(self, x, y):
        """
        Move the text to a new location
        
        Args:
            x int: x-axis movement
            y int: y-axis movement
        """
        self.rect.x += x
        self.rect.y += y
        