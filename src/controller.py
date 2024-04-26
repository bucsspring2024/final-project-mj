import pygame
import pygame_gui.core.drawable_shapes
import pygame_gui.elements.ui_drop_down_menu
import pygame_gui.elements.ui_horizontal_slider
import pygame_gui.elements.ui_panel
import pygame_gui.elements.ui_text_entry_line
import pygame_gui.elements.ui_window
import pygame_gui.windows.ui_colour_picker_dialog
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


# TODO: make gui dynamic to window size
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
        # TODO: make gui dynamic to window size
        menu = pygame_menu.Menu('Menu', LENGTH, WIDTH)
        menu.add.label('Click to start.', max_char=-1, font_size=32)

        while self.state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "BOARD"
            menu.draw(self.surface)
            pygame.display.flip()
        
                  
    def boardloop(self):
        self.board = pygame.Surface(self.surface.get_size())

        self.manager = pygame_gui.UIManager((LENGTH, WIDTH))
        edit_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (400, 200)), manager=self.manager, window_display_title='Edit Panel (DO NOT CLOSE) (Q to toggle)')
        panel_visibility = True
        text_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (100, 50)), text='Add Text', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'left':'left'})
        image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)), text='Add Image', manager=self.manager, container=edit_panel, anchors={'center':'center'})
        bg_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-120, 0), (100, 50)), text='Change BG Color', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'right':'right'})
        
        # initialize buttons
        # todo: implement save as image button in bottom right
        
        big_button = pygame.Rect(0, 0, 200, 100)
        big_button.bottomright = (-30, -20)
        save_button = pygame_gui.elements.UIButton(relative_rect=big_button, text='Save as Image', manager=self.manager, anchors={'bottom':'bottom', 'right':'right'})
        
        
        print('init done')
        
        self.texts = pygame.sprite.Group()
        self.images = pygame.sprite.Group()
        
        while self.state == "BOARD":
            for event in pygame.event.get():
                self.manager.process_events(event)
                
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
                        # add max checker
                        self.place_element("text")
                    if event.ui_element == image_button:
                        # add max checker
                        self.place_element("image")
                    if event.ui_element == bg_button:
                        pass # set up gui for color picker
                    
                # todo: right click to delete text/image collidepoint yk
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                
            # update board
            self.board.fill((255, 255, 255))
            self.texts.draw(self.board)
            self.images.draw(self.board)

            self.update_bundle()


    def endloop(self):
        while self.state == "END":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()





    def place_element(self, type):
        # pull up creator gui
        settings = self.creator_gui(type)
        print(settings)
        
        # choose location
        location = self.choose_location()
        
        # place the object on the board
        self.place_object(type, settings, location)
        
        
        # adds element to group, returns nothing
        pass
    
    
    
    def place_object(self, type, settings, location):
        # if text then create a Text object with settings and location and add to group
        if type == 'text':
            text = Text(settings, location)
            self.texts.add(text)
            print(self.texts)
        # if image then create an Image object with settings and location and add to group
        pass
    
    
    
    def creator_gui(self, type):
        # type is either text or image
        creator_gui = pygame_gui.elements.UIWindow(rect=pygame.Rect((LENGTH / 2 - 300, WIDTH / 2 - 150), (600, 300)), manager=self.manager)
        if type == "text":
            creator_gui.set_display_title('Add Text')
            text_input_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (200, 50)), initial_text='', manager=self.manager, container=creator_gui, anchors={'center':'center'})
            text =''
            
            text_size_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((-200, 0), (100, 25)), start_value=24, value_range=(12, 120), manager=self.manager, container=creator_gui, anchors={'center':'center'})
            text_size = text_size_slider.get_current_value()
            
            font_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((200, -50), (150, 50)), manager=self.manager, container=creator_gui, anchors={'center':'center'}, options_list=['Arial', 'Times New Roman', 'Comic Sans MS'], starting_option='Arial')
            font = 'Arial'
            
            color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect((LENGTH / 5 - 100, WIDTH / 2), (200, 200)), manager=self.manager, window_title='Color Picker')
            text_color = '#000000'
            
            # text_preview_window = pygame_gui.elements.ui_window.UIWindow(rect=pygame.Rect((LENGTH / 2 - 100, WIDTH / 2 + 200), (200, 200)), manager=self.manager, window_display_title='Text Preview')
            # preview_text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), text_preview_window.get_container().get_size()), manager=self.manager, container=text_preview_window, html_text='')
        
        elif type == "image":
            creator_gui.set_display_title('Choose Image Type')
            image_type_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((0, 0), (150, 50)), manager=self.manager, container=creator_gui, anchors={'0':'center'}, options_list=['Local', 'URL'], starting_option='Local')
            image_type = 'local'
            # image_input =
            
        submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 75), (100, 50)), text='Submit', manager=self.manager, container=creator_gui, anchors={'center':'center'})
        
        
        # use GUI events to get various stuff
        # this might go outside of the function in order to follow SRP
        creating = True
        while creating:
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == creator_gui:
                    creating = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == submit_button:
                        # save stuff | might not be necessary since events are updated live anyway
                        if type == "image":
                            pass # implement file
                        creating = False
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == text_size_slider:
                        text_size = text_size_slider.get_current_value()
                        print(text_size)
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == font_dropdown:
                        font = event.text
                        print(font)
                    if event.ui_element == image_type_dropdown:
                        image_type = event.text
                        print(image_type)
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_element == text_input_box:
                    text = text_input_box.get_text()
                    # we might have to use pure pygame to have a text preview; let's find out how to actually implement the text on screen first. use PIL?

            self.update_bundle()
        
        
        # this probably will return something
        creator_gui.kill()
        
        if type == "text":
            color_picker.kill()
            text_settings = [text, text_size, font, text_color]
            return text_settings
        elif type == "image":
            return image
    
    
    
    def choose_location(self):
        location_prompt = pygame_gui.elements.UIWindow(rect=pygame.Rect((LENGTH / 2 - 150, WIDTH / 2 - 75), (300, 150)), manager=self.manager, window_display_title='Click to place object')
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.board.get_rect().collidepoint(pygame.mouse.get_pos()):
                    location = pygame.mouse.get_pos()
                    print(location)
                    location_prompt.kill()
                    return location
                
                
                
            self.update_bundle()
        # returns location as tuple
        pass


    

    def update_bundle(self):
        self.manager.update(self.time_delta)
        self.surface.blit(self.board, (0, 0))
        self.manager.draw_ui(self.surface)
        pygame.display.update()

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

