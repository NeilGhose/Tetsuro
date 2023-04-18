import pygame as pg
import numpy as np
from pygame.locals import *

class Button:
    def __init__(self, win, win_size, name, x, y, width, height, func, color=(200,200,200), text_color=(0,0,0), font_size=None):
        self.win = win
        self.win_size = win_size
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
        self.color = color
        self.text_color = text_color
        if font_size is None:
            self.font_size = min(int(self.height/2), int(2.5*self.width/len(name)))

        self.font = pg.font.Font(None, self.font_size)
        self.text = self.font.render(self.name, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))

    def draw(self):
        pg.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        self.win.blit(self.text, self.text_rect)

    def in_button(self, pos):
        return pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height

    def hover(self, pos):
        if self.in_button(pos):
            pg.draw.rect(self.win, (150,150,150), (self.x, self.y, self.width, self.height))
        else:
            pg.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        self.win.blit(self.text, self.text_rect)

    def change_name(self, name):
        self.name = name
        self.text = self.font.render(self.name, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        self.hover((self.x + self.width/2, self.y + self.height/2))

    def run_func(self, *args):
        self.func(self, *args)

    def resize(self, win_size):
        self.x = self.x * win_size[0] / self.win_size[0]
        self.y = self.y * win_size[1] / self.win_size[1]
        self.width = self.width * win_size[0] / self.win_size[0]
        self.height = self.height * win_size[1] / self.win_size[1]
        self.win_size = win_size
        self.font_size = min(int(self.height/2), int(2.5*self.width/len(self.name)))
        self.font = pg.font.Font(None, self.font_size)
        self.text = self.font.render(self.name, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))

    def render_font(self):
        self.font = pg.font.Font(None, self.font_size)
        self.text = self.font.render(self.name, True, self.text_color)
        self.text_rect = self.text.get_rect(center=(self.x + self.width/2, self.y + self.height/2))

class Menu:
    def __init__(self, win, button_format, buttons, y_buffer=0, x_buffer=0, win_size=(0,0)):
        self.win = win
        self.buttons = buttons
        self.button_format = button_format
        self.y_buffer = y_buffer
        self.x_buffer = x_buffer
        self.win_size = win_size
        self.ratio = win_size[0]/win_size[1]
        self.button_positions = []
        self.win_width = min(win_size[0], win_size[1]*self.ratio)
        self.win_height = min(win_size[1], win_size[0]/self.ratio)
        self.width = self.win_width * (1 - 2*self.x_buffer)
        self.height = self.win_height * (1 - 2*self.y_buffer)
        self.button_height = self.height * (1 - self.y_buffer*(len(self.button_format)+1))/ len(self.button_format)
        self.button_widths = [self.width * (1 - self.x_buffer*(num_buttons+1))/ num_buttons for num_buttons in self.button_format]
        self.actual_buttons = []
        self.define_buttons()
        self.fix_font_sizes()

    def define_buttons(self):
        name_ind = 0
        for num_buttons_ind in range(len(self.button_format)):
            self.button_positions.append([])
            num_buttons = self.button_format[num_buttons_ind]
            y_dist = (self.win_size[1] - self.height) / 2 + self.y_buffer * (self.height * (num_buttons_ind + 1)) + self.button_height * num_buttons_ind

            for button in range(num_buttons):
                x_dist = (self.win_size[0] - self.width) / 2 + self.x_buffer * (self.width * (button + 1)) + self.button_widths[num_buttons_ind] * button
                name = list(self.buttons.keys())[name_ind]
                name_ind += 1
                # self.button_positions[num_buttons_ind].append(Button(self.win, name, x_dist, y_dist, self.button_widths[num_buttons_ind], self.button_height))
                self.actual_buttons.append(Button(self.win, self.win_size, name, x_dist, y_dist, self.button_widths[num_buttons_ind], self.button_height, self.buttons[name]))

    def draw(self):
        # self.win_width = min(self.win_size[0], self.win_size[1]*self.ratio)
        # self.win_height = min(self.win_size[1], self.win_size[0]/self.ratio)

        # self.width = self.win_width * (1 - 2*self.x_buffer)
        # self.height = self.win_height * (1 - 2*self.y_buffer)
        # self.button_widths = []
        pg.draw.rect(self.win, (100,100,100), ((self.win_size[0] - self.width) / 2, (self.win_size[1] - self.height) / 2, self.width, self.height))

        # name_ind = 0

        # self.button_height = self.height * (1 - self.y_buffer*(len(self.button_format)+1))/ len(self.button_format)
        # for num_buttons_ind in range(len(self.button_format)):
        #     self.button_positions.append([])
        #     num_buttons = self.button_format[num_buttons_ind]
        #     self.button_widths.append(self.width * (1 - self.x_buffer*(num_buttons+1))/ num_buttons)
        #     y_dist = (self.win_size[1] - self.height) / 2 + self.y_buffer * (self.height * (num_buttons_ind + 1)) + self.button_height * num_buttons_ind

        #     for button in range(num_buttons):
        #         x_dist = (self.win_size[0] - self.width) / 2 + self.x_buffer * (self.width * (button + 1)) + self.button_widths[num_buttons_ind] * button
        #         pg.draw.rect(self.win, (200,200,200), (x_dist, y_dist, self.button_widths[num_buttons_ind], self.button_height))
        #         name = list(self.buttons.keys())[name_ind]
        #         name_ind += 1
        #         self.button_positions[num_buttons_ind].append(name)
        #         font = pg.font.Font(None, min(int(self.button_height/2), int(2.5*self.button_widths[num_buttons_ind]/len(name))))
        #         text = font.render(name, True, (0,0,0))
        #         text_rect = text.get_rect(center=(x_dist + self.button_widths[num_buttons_ind]/2, y_dist + self.button_height/2))
        #         self.win.blit(text, text_rect)
        for button in self.actual_buttons:
            button.draw()

    def get_button(self, pos):
        # for num_buttons_ind in range(len(self.button_format)):
        #     num_buttons = self.button_format[num_buttons_ind]
        #     for button in range(num_buttons):
        #         x_dist = (self.win_size[0] - self.width) / 2 + self.x_buffer * (self.width * (button + 1)) + self.button_widths[num_buttons_ind] * button
        #         y_dist = (self.win_size[1] - self.height) / 2 + self.y_buffer * (self.height * (num_buttons_ind + 1)) + self.button_height * num_buttons_ind
        #         if pos[0] > x_dist and pos[0] < x_dist + self.button_widths[num_buttons_ind] and pos[1] > y_dist and pos[1] < y_dist + self.button_height:
        #             return (num_buttons_ind, button)
        for button_ind in range(len(self.actual_buttons)):
            button = self.actual_buttons[button_ind]
            if button.in_button(pos):
                return button_ind


    def click(self, pos):
        # button = self.get_button(pos)
        # if button:
        #     self.buttons[self.button_positions[button[0]][button[1]]]()#self.button_positions[button[0]][button[1]])
        button = self.get_button(pos)
        if button != None:
            self.actual_buttons[button].run_func()

    def hover(self, pos):
        # button = self.get_button(pos)
        # if button:
        #     num_buttons_ind = button[0]
        #     button = button[1]
        #     button_width = self.button_widths[num_buttons_ind]
        #     x_dist = (self.win_size[0] - self.width) / 2 + self.x_buffer * (self.width * (button + 1)) + button_width * button
        #     y_dist = (self.win_size[1] - self.height) / 2 + self.y_buffer * (self.height * (num_buttons_ind + 1)) + self.button_height * num_buttons_ind
        #     pg.draw.rect(self.win, (150,150,150), (x_dist, y_dist, button_width, self.button_height))
        #     try:
        #         st = self.button_positions[num_buttons_ind][button]
        #     except:
        #         self.draw()
        #         return
        #     font = pg.font.Font(None, min(int(self.button_height/2), int(2.5*button_width/len(st))))
        #     text = font.render(st, True, (0,0,0))
        #     text_rect = text.get_rect(center=(x_dist + button_width/2, y_dist + self.button_height/2))
        #     self.win.blit(text, text_rect)
        # else:
        #     self.draw()
        for button in self.actual_buttons:
            button.hover(pos)
        
    def run(self, events):
        self.draw()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            elif event.type == pg.VIDEORESIZE:
                self.resize(event.size)
                self.draw()
                return
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                self.click(pos)
                return
            
            elif event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
                self.hover(pos)
                return
        
        pos = pg.mouse.get_pos()
        for button in self.actual_buttons:
            if button.in_button(pos):
                button.hover(pos)
                return
    
    def resize(self, win_size):
        self.win_size = win_size
        self.win_width = win_size[0]
        self.win_height = win_size[1]

        self.width = self.win_width * (1 - 2*self.x_buffer)
        self.height = self.win_height * (1 - 2*self.y_buffer)

        for button in self.actual_buttons:
            button.resize(win_size)

        self.fix_font_sizes()

    def fix_font_sizes(self):
        smallest = 10000
        for button in self.actual_buttons:
            smallest = min(smallest, button.font_size)
        for button in self.actual_buttons:
            button.font_size = smallest
            button.render_font()

if __name__ == "__main__":
    def button_call(button=None):
        print(button, "pressed")

    pg.init()

    win_size = (1600,800)
    win=pg.display.set_mode(win_size, RESIZABLE)
    pg.display.set_caption("Game")
    bg_color = (255,255,255)
    win.fill(bg_color)
    run = True

    scene = Menu(win, [1,2,3], {"2":button_call, 
                                "1":button_call, 
                                "3":button_call, 
                                "4":button_call, 
                                "5":button_call, 
                                "6":button_call}, .1, .1, win_size)
    scene.draw()
    while run:
        pg.time.delay(10)
        scene.run(pg.event.get())
            

        k = pg.key.get_pressed()
                
        if k[pg.K_ESCAPE]:
            run=False    

        pg.display.update()