import pygame
import pygame_menu
import pygame_gui
import json
from src.utility import Utility
from src.text import Text
from src.image import Image


class Controller:

    
    def __init__(self):
        # TODO: make gui dynamic to window size
        consts = Utility()
        self.LENGTH = consts.length
        self.WIDTH = consts.width
        self.FRAMERATE = 60
        
        
        pygame.init()
        pygame.display.set_caption('Vision Board Creator')
    
        self.surface = pygame.display.set_mode((self.LENGTH, self.WIDTH))
        
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(self.FRAMERATE) / 1000.0

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
        menu = pygame_menu.Menu('Menu', self.LENGTH, self.WIDTH)
        menu.add.label('Click to start.', max_char=-1, font_size=32)

        while self.state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "BOARD"
                    
            menu.draw(self.surface)
            pygame.display.flip()
      
        
                  
    def boardloop(self):
        # init board
        self.board = pygame.Surface(self.surface.get_size())
        self.bg_color = pygame.Color(0, 0, 0, 0)
        self.board.fill(self.bg_color)
        
        # init core gui
        self.manager = pygame_gui.UIManager((self.LENGTH, self.WIDTH), theme_path='etc/style.json')
        
        edit_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (600, 200)), manager=self.manager, window_display_title='Edit Panel')
        panel_visibility = True
        text_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((37.5, 0), (150, 50)), text='Add Text', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'left':'left'})
        image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (150, 50)), text='Add Image', manager=self.manager, container=edit_panel, anchors={'center':'center'})
        bg_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-187.5, 0), (150, 50)), text='Change BG', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'right':'right'})
        
        big_button = pygame.Rect(0, 0, 200, 100)
        big_button.bottomright = (-30, -20)
        save_button = pygame_gui.elements.UIButton(relative_rect=big_button, text='Save as Image', manager=self.manager, anchors={'bottom':'bottom', 'right':'right'})
        
        tips_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.LENGTH - 300, 0), (300, 300)), manager=self.manager, window_display_title='Tips')
        tips = ['Right click to delete', 'Q to toggle edit panel', 'Z to save', 'C to load']
        for i, tip in enumerate(tips):
            tip_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, (i - len(tips)/2) * 25), (200, 25)), text=tip, manager=self.manager, container=tips_panel, anchors={'center':'center'})
        
        # init sprite groups
        self.texts = pygame.sprite.Group()
        self.images = pygame.sprite.Group()
        
        # mainloop
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
                        self.save_board()
                    if event.key == pygame.K_c:
                        self.load_board()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3: # right click
                        for image in self.images:
                            if image.rect.collidepoint(pygame.mouse.get_pos()):
                                image.kill()
                        for text in self.texts:
                            if text.rect.collidepoint(pygame.mouse.get_pos()):
                                text.kill()
                
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    edit_panel.disable()
                    save_button.disable()
                    if event.ui_element == text_button:
                        self.place_element("text")
                    if event.ui_element == image_button:
                        self.place_element("image")
                    if event.ui_element == bg_button:
                        bg_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect((self.LENGTH / 2 - 300, self.WIDTH / 2 - 300), (600, 600)), manager=self.manager, window_title='Background Color Picker', object_id='#bg_picker')
                        text_button.disable()
                        image_button.disable()
                    if event.ui_element == save_button:
                        pygame.image.save(self.board, 'etc/board.png')
                    edit_panel.enable()
                    save_button.enable()
                    
                    
                elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED and event.ui_object_id == '#bg_picker':
                    self.bg_color = event.colour
                    bg_picker.kill()
                    text_button.enable()
                    image_button.enable()

                # it seems pygame_gui has no method to make a window not closable
                elif event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == edit_panel:
                    edit_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (400, 200)), manager=self.manager, window_display_title='Edit Panel')
                    text_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (100, 50)), text='Add Text', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'left':'left'})
                    image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)), text='Add Image', manager=self.manager, container=edit_panel, anchors={'center':'center'})
                    bg_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-120, 0), (100, 50)), text='Change BG Color', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'right':'right'})

            # update board
            self.board.fill(self.bg_color)
            self.images.draw(self.board)
            self.texts.draw(self.board)

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
        if settings is not None:
            # choose location
            location = self.choose_location()
                        
            # place the object on the board
            self.create_object(type, settings, location)

        
    
    def create_object(self, type, settings, location):
        # if text then create a Text object with settings and location and add to group
        if type == 'text':
            text = Text(settings, location)
            text.create()
            self.texts.add(text)
        
        # if image then create an Image object with settings and location and add to group
        elif type == 'image':
            image = Image(settings, location)
            image.create()
            self.images.add(image)
    
    
    
    def creator_gui(self, type):
        # type is either text or image
        text_gui = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.LENGTH / 2, self.WIDTH / 2 - 150), (600, 300)), manager=self.manager)
        
        text_gui.set_display_title('Add Text')
        text_input_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (200, 50)), initial_text='sample', placeholder_text='Your text here', manager=self.manager, container=text_gui, anchors={'center':'center'})
        text = 'sample'
        text_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, -50), (250, 25)), text='Your text here!', manager=self.manager, container=text_gui, anchors={'center':'center'})

        
        text_size_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((-200, 0), (150, 50)), start_value=48, value_range=(24, 72), manager=self.manager, container=text_gui, anchors={'center':'center'})
        text_size = text_size_slider.get_current_value()
        text_size_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((-200, -50), (250, 25)), text=f'Text size: {text_size}', manager=self.manager, container=text_gui, anchors={'center':'center'})
        
        fonts = ['Cambria', 'Comic Sans MS', 'Helvetica']
        font_dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect((200, 0), (150, 50)), manager=self.manager, container=text_gui, anchors={'center':'center'}, options_list=fonts, starting_option=fonts[0])
        font = fonts[0]
        font_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((200, -50), (250, 25)), text='Choose your font', manager=self.manager, container=text_gui, anchors={'center':'center'})
        
        color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect(((self.LENGTH / 8), (self.WIDTH / 2) - 200), (600, 400)), manager=self.manager, window_title='Color Picker', object_id='#text_color_picker')
        text_color = pygame.Color(0, 0, 0, 255)
        color_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 100), (500, 25)), text='Choose your text color (change BG back after)', manager=self.manager, container=color_picker, anchors={'center':'center'})
        color_label_2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 125), (500, 25)), text='Click OK to lock in the color', manager=self.manager, container=color_picker, anchors={'center':'center'})
        
        text_submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 75), (100, 50)), text='Submit', manager=self.manager, container=text_gui, anchors={'center':'center'})
        
        
        
        image_gui = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.LENGTH / 2 - 300, self.WIDTH / 2 - 150), (600, 300)), manager=self.manager)

        image_gui.set_display_title('Generate AI Image')
        
        ai_prompt_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (200, 50)), initial_text='A beautiful sunset', placeholder_text='AI Prompt', manager=self.manager, container=image_gui, anchors={'center':'center'})
        ai_prompt_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, -75), (250, 25)), text='What\'s your prompt?', manager=self.manager, container=image_gui, anchors={'center':'center'})
        ai_prompt_label_2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, -50), (500, 25)), text='Warning: Stable Diffusion takes a while', manager=self.manager, container=image_gui, anchors={'center':'center'})
        ai_prompt = 'A beautiful sunset'
        
        image_submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 75), (100, 50)), text='Submit', manager=self.manager, container=image_gui, anchors={'center':'center'})
        
        if type == "text":
            image_gui.hide()

        elif type == "image":
            text_gui.hide()
            color_picker.hide()
        
        # use GUI events to get various stuff        
        creating = True
        while creating:
            
            for event in pygame.event.get():
                self.manager.process_events(event)                 
                
                if event.type == pygame_gui.UI_WINDOW_CLOSE and (event.ui_element == text_gui or event.ui_element == image_gui):
                    color_picker.kill()
                    text_gui.kill()
                    image_gui.kill()
                    return None
                elif event.type == pygame_gui.UI_BUTTON_PRESSED and (event.ui_element == text_submit_button or event.ui_element == image_submit_button):
                    creating = False
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == text_size_slider:
                    text_size = text_size_slider.get_current_value()
                    text_size_prompt = f"Text size: {text_size}"
                    text_size_label.set_text(text_size_prompt)
                elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    font = event.text
                elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED and event.ui_object_id == '#text_color_picker':
                    text_color = event.colour
                elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_element == text_input_box:
                        text = text_input_box.get_text()
                    elif event.ui_element == ai_prompt_box:
                        ai_prompt = ai_prompt_box.get_text()

                
                            
            self.update_bundle()
        
        # after done creating, kill GUI and return necessary stuff
        color_picker.kill()
        text_gui.kill()
        image_gui.kill()
           
        if type == "text":
            text_settings = [text, text_size, font, text_color]
            return text_settings
        elif type == "image":
            return ai_prompt
    
    
    
    def choose_location(self):
        location_prompt = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.LENGTH / 2 - 250, self.WIDTH / 2 - 75), (500, 150)), manager=self.manager, window_display_title='Click to place object')
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.board.get_rect().collidepoint(pygame.mouse.get_pos()):
                    location = pygame.mouse.get_pos()
                    print(location)
                    location_prompt.kill()
                    return location
                
            self.update_bundle()



    def update_bundle(self):
        self.manager.update(self.time_delta)
        self.surface.blit(self.board, (0, 0))
        self.manager.draw_ui(self.surface)
        pygame.display.update()

    
    def save_board(self):
        self.saved_texts = self.texts.copy()
        self.saved_images = self.images.copy()
    
    def load_board(self):
        self.texts = self.saved_texts
        self.images = self.saved_images