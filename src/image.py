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
        
            # self.image = pygame.image.load(settings)
            # self.rect = self.image.get_rect()
        self.prompt = prompt
        self.position = position
    
    
    
    def create(self):
        """
        Create the image object
        """
        genai = StableDiffusion(self.prompt)
        self.image = genai.get_image()
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode).convert()
        
        self.resize()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position