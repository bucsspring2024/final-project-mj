import pygame
import pygame_gui.core.drawable_shapes
import pygame_gui.elements.ui_panel
import pygame_gui.elements.ui_window
import pygame_menu
import pygame_gui
from src.utility import Utility
from src.text import Text
from src.image import Image

# libraries I might need
    # request to get images
        # retry if it fails
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
        pygame.display.set_caption('Vision Board Creator')
        
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

        while self.state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "BOARD"
            menu.draw(self.surface)
            pygame.display.flip()
        
                  
    def boardloop(self):
        board = pygame.Surface(self.surface.get_size())

        manager = pygame_gui.UIManager((LENGTH, WIDTH))
        edit_panel = pygame_gui.elements.ui_window.UIWindow(rect=pygame.Rect((0, 0), (400, 200)), manager=manager, window_display_title='Edit Panel (DO NOT CLOSE) (Q to toggle)')
        panel_visibility = True
        text_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (100, 50)), text='Add Text', manager=manager, container=edit_panel, anchors={'centery':'centery', 'left':'left'})
        image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)), text='Add Image', manager=manager, container=edit_panel, anchors={'center':'center'})
        bg_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-120, 0), (100, 50)), text='Change BG Color', manager=manager, container=edit_panel, anchors={'centery':'centery', 'right':'right'})
        
        # initialize buttons
        # todo: implement save as image button in bottom right
        
        big_button = pygame.Rect(0, 0, 200, 100)
        big_button.bottomright = (-30, -20)
        save_button = pygame_gui.elements.UIButton(relative_rect=big_button, text='Save as Image', manager=manager, anchors={'bottom':'bottom', 'right':'right'})
        
        
        print('init done')
        
        text = pygame.sprite.Group()
        image = pygame.sprite.Group()
        
        while self.state == "BOARD":
            for event in pygame.event.get():
                manager.process_events(event)
                
                if event.type == pygame.QUIT:
                    self.state = "END"
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        panel_visibility = not panel_visibility
                        edit_panel.show() if panel_visibility else edit_panel.hide()
                    if event.key == pygame.K_z:
                        pass # implement saving of image/text data as a json file
                    if event.key == pygame.K_x:
                        pass # implement loading of image/text data from a json file  
                    
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == text_button:
                        self.place_object("text")
                        self.creator_gui("text")
                    if event.ui_element == image_button:
                        self.place_object("text")
                        self.creator_gui("image")
                    if event.ui_element == bg_button:
                        pass # set up gui for color picker
                    
                # todo: right click to delete text/image collidepoint yk
            
            # update the board with text and images

            manager.update(self.time_delta)
            
            self.surface.blit(board, (0, 0)) #?
            manager.draw_ui(self.surface)
            
            pygame.display.update()

    def endloop(self):
        while self.state == "END":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()

    
    
    def place_object(self, type):
        # show text with directions
        # choose location to place object by clicking
        # maybe creator_gui goes inside?
        pass
    
    def creator_gui(self, type):
        # type is either text or image
        # if text, then show text input box
        # if image, then show image input box
        pass
    

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

