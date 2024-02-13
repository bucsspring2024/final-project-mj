import pygame
from src.controller import Controller

def main():
    pygame.init()
    controller = Controller()
    
    controller.mainloop()
    
    ###### NOTHING ELSE SHOULD GO IN main(), JUST THE ABOVE 3 LINES OF CODE ######

# https://codefather.tech/blog/if-name-main-python/
if __name__ == '__main__':
    main()
