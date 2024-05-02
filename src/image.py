import pygame
from src.stablediffusion import StableDiffusion

class Image(pygame.sprite.Sprite):
    def __init__(self, prompt, position):
        """
        Initialize the image object
        Args:
            settings str: image prompt / path
            position tuple: location of the image on the screen
        """
        super().__init__()
        
        self.prompt = prompt
        self.position = position
    
    
    
    def create(self):
        """
        Create the image object
        """
        genai = StableDiffusion(self.prompt)
        self.pil_image = genai.get_image()
        self.image_object = pygame.image.fromstring(self.pil_image.tobytes(), self.pil_image.size, self.pil_image.mode).convert()
        
        self.image = self.image_object
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        
    def scale(self, w, h):
        """
        Scale the image
        """
        self.pil_image = self.pil_image.resize((round(w), round(h)))
        self.image_object = pygame.image.fromstring(self.pil_image.tobytes(), self.pil_image.size, self.pil_image.mode).convert_alpha()
        self.image = self.image_object
        self.rect.width, self.rect.height = self.image.get_size()
    
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        
        