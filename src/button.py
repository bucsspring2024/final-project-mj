import pygame
import pygame_gui

class Button(pygame_gui.elements.ui_button):
    def __init__(self, rect, text, action):
        self.rect = rect
        self.text = text
        self.action = action