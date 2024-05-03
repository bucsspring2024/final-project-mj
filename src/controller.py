import pygame
import pygame_menu
import pygame_gui
import copy
from src.utility import Utility
from src.text import Text
from src.image import Image


class Controller:

    
    def __init__(self):
        """
        Initialize the controller and the pygame window as well as core variables
        Takes no args and has no return
        """
        consts = Utility()
        self.WIDTH = consts.width
        self.HEIGHT = consts.height
        self.FRAMERATE = 60
        
        
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('assets/aruarian_dance.mp3')
        pygame.display.set_caption('Vision Board Creator')
    
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.time_delta = self.clock.tick(self.FRAMERATE) / 1000.0

        # init sprite groups
        self.texts = pygame.sprite.Group()
        self.images = pygame.sprite.Group()
        self.items = [self.texts, self.images]
        
        self.selected_texts = []
        self.selected_images = []
        self.selected = [self.selected_texts, self.selected_images]

        self.board = pygame.Surface(self.surface.get_size())
        self.bg_color = pygame.Color(0, 0, 0, 0)
        self.board.fill(self.bg_color)


        self.state = 'MENU'


        
    def mainloop(self):
        """
        The mainloop function to switch between states
        """
        while True:
            if self.state == 'MENU':
                self.menuloop()
            elif self.state == 'BOARD':
                self.boardloop()
            elif self.state == 'END':
                self.endloop()            
    
    
    
    def menuloop(self):
        """
        The menuloop that displays the menu screen
        """
        font = pygame_menu.font.FONT_FIRACODE
        my_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title_font=font, title_font_size=32, title_offset=(0, 0), widget_font=font, widget_font_size=24, widget_font_color=(255, 255, 255), widget_offset=(0, 0))
        menu = pygame_menu.Menu('The Vision Board Maker', theme=my_theme, width=self.WIDTH, height=self.HEIGHT)
        menu.add.label('Click to start your vision board experience.', max_char=-1, font_size=64)

        while self.state == "MENU":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "BOARD"
                    
            menu.draw(self.surface)
            pygame.display.flip()
      
        
                  
    def boardloop(self):
        """
        The boardloop that displays the board screen. Most of the time using this program is spent here
        """
        # unfortunately pygame_gui doesn't let me take the dimensions of given gui elements, so I have to use magic numbers
                        
        # init core gui
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT), theme_path='etc/style.json')
        
        edit_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (self.WIDTH / 3, self.HEIGHT / 5)), manager=self.manager, window_display_title='Edit Panel', draggable=False, resizable=False)
        panel_visibility = True
        text_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((37.5, 0), (150, 50)), text='Add Text', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'left':'left'})
        image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (150, 50)), text='Add Image', manager=self.manager, container=edit_panel, anchors={'center':'center'})
        bg_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-187.5, 0), (150, 50)), text='Change BG', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'right':'right'})
        
        big_button = pygame.Rect(0, 0, round(self.WIDTH / 9), round(self.HEIGHT / 10))
        big_button.bottomright = (-30, -20)
        save_button = pygame_gui.elements.UIButton(relative_rect=big_button, text='Save as Image', manager=self.manager, anchors={'bottom':'bottom', 'right':'right'})
        
        tips_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.WIDTH - (self.WIDTH / 6), 0), (self.WIDTH / 6, self.HEIGHT / 4)), manager=self.manager, window_display_title='Tips', draggable=False, resizable=False)
        tips = ['Click to select and drag', 'Click and UP/DOWN to scale', 'Right click to delete', 'Q to toggle edit panel', 'Z to save', 'C to load', 'M to mute']
        for i, tip in enumerate(tips):
            tip_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, (i - len(tips)/2) * 25), (250, 25)), text=tip, manager=self.manager, container=tips_panel, anchors={'center':'center'})
        
        pygame.mixer.music.play(-1, 0.0, 5000)
        pygame.mixer.music.set_volume(0.1)
        mute = False
         
        selecting_color = False
        
        # Board loop
        while self.state == "BOARD":
            for event in pygame.event.get():
                self.manager.process_events(event)
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        panel_visibility = not panel_visibility
                        (edit_panel.show(), tips_panel.show()) if panel_visibility else (edit_panel.hide(), tips_panel.hide())
                    elif event.key == pygame.K_z:
                        self.save_board()
                    elif event.key == pygame.K_c:
                        self.load_board()
                    elif event.key == pygame.K_m:
                        mute = not mute
                        pygame.mixer.music.set_volume(0) if mute else pygame.mixer.music.set_volume(0.1)
                    elif event.key == pygame.K_UP:
                        for item in self.selected:
                            for obj in item:
                                ratio = obj.rect.width / obj.rect.height
                                new_width = obj.rect.width + 5
                                new_height = new_width / ratio
                                obj.scale(new_width, new_height)
                    elif event.key == pygame.K_DOWN:
                        for item in self.selected:
                            for obj in item:
                                ratio = obj.rect.width / obj.rect.height
                                new_width = obj.rect.width - 5
                                new_height = new_width / ratio
                                obj.scale(new_width, new_height)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not selecting_color: # left click
                        for item in self.items:
                            for obj in item:
                                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                                    self.selected_texts.append(obj) if item == self.texts else self.selected_images.append(obj)
                    elif event.button == 3: # right click
                        for item in self.items:
                            for obj in item:
                                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                                    obj.kill()
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.selected_texts = []
                    self.selected_images = []
                    self.selected = [self.selected_texts, self.selected_images]
                    
                elif event.type == pygame.MOUSEMOTION:
                    for item in self.selected:
                        for obj in item:
                            obj.move(event.rel[0], event.rel[1])
                
                
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    edit_panel.disable()
                    save_button.disable()
                    if event.ui_element == text_button:
                        self.place_element("text")
                    if event.ui_element == image_button:
                        self.place_element("image")
                    if event.ui_element == bg_button:
                        text_button.disable()
                        image_button.disable()
                        bg_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect((self.WIDTH / 2 - 300, self.HEIGHT / 2 - 300), (600, 600)), manager=self.manager, window_title='Background Color Picker', object_id='#bg_picker')
                        selecting_color = True
                    if event.ui_element == save_button:
                        pygame.image.save(self.board, 'etc/board.png')
                        edit_panel.kill()
                        tips_panel.kill()
                        save_button.kill()
                        self.state = "END"
                        
                    edit_panel.enable()
                    save_button.enable()
                    
                    
                elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED and event.ui_object_id == '#bg_picker':
                    self.bg_color = copy.deepcopy(event.colour) # deepcopy here to fix bg bug OMG!
                    bg_picker.kill()
                    selecting_color = False
                    text_button.enable()
                    image_button.enable()

                # it seems pygame_gui has no method to make a window not closable, so if you close it I just have to make it again
                elif event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == edit_panel:
                    edit_panel = pygame_gui.elements.UIWindow(rect=pygame.Rect((0, 0), (self.WIDTH / 3, self.HEIGHT / 5)), manager=self.manager, window_display_title='Edit Panel', draggable=False, resizable=False)
                    text_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((37.5, 0), (150, 50)), text='Add Text', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'left':'left'})
                    image_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (150, 50)), text='Add Image', manager=self.manager, container=edit_panel, anchors={'center':'center'})
                    bg_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-187.5, 0), (150, 50)), text='Change BG', manager=self.manager, container=edit_panel, anchors={'centery':'centery', 'right':'right'})

            # update board
            self.board.fill(self.bg_color)
            self.images.draw(self.board)
            self.texts.draw(self.board)
            self.update_bundle()



    def endloop(self):
        """
        The end state where we can either go back into board state or quit the program
        """
        end_gui = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.WIDTH / 2 - self.WIDTH / 8, self.HEIGHT / 2 - self.HEIGHT / 12), (self.WIDTH / 4, self.HEIGHT / 6)), manager=self.manager, window_display_title='Thanks for making a board!')
        end_program_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-75, 0), (150, 50)), text='End Program', manager=self.manager, container=end_gui, anchors={'center':'center'})
        back_to_board_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((75, 0), (150, 50)), text='Back to Board', manager=self.manager, container=end_gui, anchors={'center':'center'})
        
        
        while self.state == "END":
            for event in pygame.event.get():
                self.manager.process_events(event)
                
                if event.type == pygame.QUIT or (event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == end_gui):
                    pygame.quit()
                    exit()
                    
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == end_program_button:
                        pygame.quit()
                        exit()
                    if event.ui_element == back_to_board_button:
                        self.state = "BOARD"
                    
                        
            self.update_bundle()










    def place_element(self, type):
        """
        Place an element on the board
        Args:
            type (_type_): _description_
        """
        # pull up creator gui
        settings = self.creator_gui(type)
        if settings is not None:
            # choose location
            location = self.choose_location()
                        
            # place the object on the board
            self.create_object(type, settings, location)

        
    
    def create_object(self, type, settings, location):
        """
        Create an image and add it to a Sprite group so it can be drawn on the board
        Args:
            type (str): Either text or image
            settings list | str: If object is text, returns a list of text settings, if object is image, returns a string of the prompt
            location tuple: (x, y) of the object on the board
        """
        # if text then create a Text object with settings and location and add to group
        if type == 'text':
            text = Text(settings, location)
            text.create()
            self.texts.add(text)
        
        # if image then create an Image object with settings and location and add to group
        elif type == 'image':
            image = Image(settings, location)
            image.create()
            image.scale(self.WIDTH / 6, self.WIDTH / 6)
            self.images.add(image)
    
    
    
    def creator_gui(self, type):
        """
        The core creator GUI that allows the user to create text or image objects
        Args:
            type (str): Image or text

        Returns:
            list: If the object is text, returns text settings
            str: If the object is image, returns the prompt
        """
        # type is either text or image
        text_gui = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.WIDTH / 2, self.HEIGHT / 2 - 150), (600, 300)), manager=self.manager)
        
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
        
        color_picker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect(((self.WIDTH / 8), (self.HEIGHT / 2) - 200), (600, 400)), manager=self.manager, window_title='Color Picker', object_id='#text_color_picker')
        text_color = pygame.Color(0, 0, 0, 255)
        color_label_2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 125), (500, 25)), text='Click OK to lock in the color', manager=self.manager, container=color_picker, anchors={'center':'center'})
        
        text_submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 75), (100, 50)), text='Submit', manager=self.manager, container=text_gui, anchors={'center':'center'})
        
        
        
        image_gui = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.WIDTH / 2 - 300, self.HEIGHT / 2 - 150), (600, 300)), manager=self.manager)

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
        '''
        Get the location for the new object on the board
        
        Returns:
            tuple: (x, y) location of the object on the board
        '''
        location_prompt = pygame_gui.elements.UIWindow(rect=pygame.Rect((self.WIDTH / 2 - 250, self.HEIGHT / 2 - 75), (500, 150)), manager=self.manager, window_display_title='Click to place object')
        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.board.get_rect().collidepoint(pygame.mouse.get_pos()):
                    location = pygame.mouse.get_pos()
                    location_prompt.kill()
                    return location
                
            self.update_bundle()



    def update_bundle(self):
        '''
        An organization function to update the board and GUI elements
        '''
        self.manager.update(self.time_delta)
        self.surface.blit(self.board, (0, 0))
        self.manager.draw_ui(self.surface)
        pygame.display.update()

    
    
    # for reasons I don't understand, this fixes a bg color bug I've had the entire time.
    def save_board(self):
        '''
        Save the board state
        '''
        self.saved_settings = [copy.deepcopy(self.texts), copy.deepcopy(self.images), copy.copy(self.bg_color)] # deepcopy to save as new object this is esoteric technology
    
    def load_board(self):
        '''
        Load the board state
        '''
        if hasattr(self, 'saved_settings'):
            self.texts = copy.deepcopy(self.saved_settings[0])
            self.images = copy.deepcopy(self.saved_settings[1])
            self.bg_color = copy.copy(self.saved_settings[2])