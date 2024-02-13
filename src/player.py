import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img="assets/player.png"):
        super().__init__()
        
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y