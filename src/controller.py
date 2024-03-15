import pygame
import pygame_menu
from . import utility

# is this how constants work LOL ???
consts = utility.Utility()
LENGTH = consts.length
WIDTH = consts.width
MAX_TEXT = consts.max_text
MAX_IMAGES = consts.max_images

class Controller:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('My Cool Final Project!11!!!1')
        
        self.surface = pygame.display.set_mode((LENGTH, WIDTH))
        pygame.display.flip()
        
        self.state = 'MENU'


        
    def mainloop(self):
        
        while True:
            if self.state == 'MENU':
                self.menuloop()
            elif self.state == 'BOARD':
                self.boardloop()
            elif self.state == 'END':
                self.endloop()            
    
    
    
    def menuloop(self):
        self.menu = pygame_menu.Menu('Menu', LENGTH, WIDTH)
        self.menu.add.label('Click to start.', max_char=-1, font_size=32)
        self.menu.draw(self.surface)

        while self.state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "BOARD"
            pygame.display.flip()
        
                  
    def boardloop(self):
        exit()



    def endloop(self):
        pass

# EXPECTED STATES
    # MENU 
    # BOARD
    # ADD_TEXT / ADD_IMAGE
    # PLACE_TEXT / PLACE_IMAGE
    # EDIT_TEXT / EDIT_IMAGE
    # SAVE

# REQUIRED CLASSES
    # TEXT CLASS
    # IMAGE CLASS
    # BOARD CLASS?
    # 
