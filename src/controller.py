import pygame
import pygame_menu


class Controller:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('My Cool Final Project!11!!!1')
        
        self.width = 960
        self.height = 540
        self.surface = pygame.display.set_mode((self.width, self.height))
    
        pygame.display.flip()
        
        self.state = 'START'


        
    def mainloop(self):
        while True:
            if self.state == 'START':
                self.startloop()
            elif self.state == 'GAME':
                self.gameloop()
            elif self.state == 'END':
                self.endloop()            
    
    
    
    def startloop(self):
        self.menu = pygame_menu.Menu('Menu', self.width, self.height)
        self.menu.add.label('Click to start.', max_char=-1, font_size=32)
        self.menu.draw(self.surface)
        running = True

        while running:
            self.menu.update(pygame.event.get())
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "GAME"
            print(self.state)
            pygame.display.flip()
        

                  
    def gameloop(self):
        exit()



    def endloop(self):
        pass