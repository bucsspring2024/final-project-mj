import pygame
import pygame_menu
import pygame_gui
from src.utility import Utility
from src.text import Text
from src.image import Image

# libraries I might need
    # request to get images
    # PIL to process images
    # tkinter is standard so no extra credit but might need for save
    

# is this how constants work LOL ???
consts = Utility()
LENGTH = consts.length
WIDTH = consts.width
MAX_TEXT = consts.max_text
MAX_IMAGES = consts.max_images
FRAMERATE = 60

class Controller:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('My Cool Final Project!11!!!1')
        
        self.surface = pygame.display.set_mode((LENGTH, WIDTH))
        
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(FRAMERATE) / 1000.0

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
        menu = pygame_menu.Menu('Menu', LENGTH, WIDTH)
        menu.add.label('Click to start.', max_char=-1, font_size=32)
        menu.draw(self.surface)

        while self.state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "BOARD"
            pygame.display.flip()
        
                  
    def boardloop(self):
        board = pygame.Surface(self.surface.get_size())

        self.manager = pygame_gui.UIManager((LENGTH, WIDTH))
        
        # initialize buttons
        
        while self.state == "BOARD":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "END"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check collision points
                    # collide with add text or add image button - then do that
                    # button class needed, use pygame_gui
                    pass
                # are there other events? most things are clicking related
                # maybe a right click to edit? sounds good
            
            # update the board with text and images
            # update ui manager ?
            
            self.surface.blit(board, (0, 0))
            pygame.display.flip()

    def endloop(self):
        while self.state == "END":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()

# EXPECTED STATES
    # MENU 
    # BOARD
    # ADD_TEXT / ADD_IMAGE
    # PLACE_TEXT / PLACE_IMAGE
    # EDIT_TEXT / EDIT_IMAGE
    # None of the above 3 are states, they're actions. All go in boardloop.
    # SAVE

# REQUIRED CLASSES
    # TEXT CLASS
    # IMAGE CLASS
    # BOARD CLASS?
    #

