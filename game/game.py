from menu import Menu
import pygame as pg
import numpy as np
from pygame.locals import *
import random as rd
import time 

cscsc = []
def draw_rect(win, x, y, theta, size, color):
    global cscsc
    if cscsc == []:
        cscsc = [1/np.cos(np.radians(i)) for i in range(46)]
        cscsc += [cscsc[90-i] for i in range(46, 91)]
        cscsc = cscsc + cscsc[1:]
        cscsc = cscsc + cscsc[1:180]
    
    # for phi in range(360):
    #     angle = (phi - theta + 360) % 360
    #     pg.draw.line(win, color, (x, y), (x + cscsc[angle]*size/2*np.cos(np.radians(phi)), y + cscsc[angle]*size/2*np.sin(np.radians(phi))), 1)
    rotation = np.array([[np.cos(np.radians(theta)), -np.sin(np.radians(theta))], [np.sin(np.radians(theta)), np.cos(np.radians(theta))]])
    corners = np.array([[-size/2, -size/2], [size/2, -size/2], [size/2, size/2], [-size/2, size/2]])
    points = np.array([x, y]) + np.dot(rotation, corners.T).T

    pg.draw.polygon(win, color, points)

def check_key(k, prev_k, key):
    return k[key] and not prev_k[key]

class GameOverScreen:
    def __init__(self, win, win_size, color=(0,0,0)):
        self.win = win
        self.win_size = win_size
        self.square_size = min(win_size)
        self.color = color
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2

    def draw(self, score):
        font = pg.font.Font(None, int(self.square_size/10))
        text = font.render("Game Over!", True, self.color)
        self.win.blit(text, text.get_rect(center=(self.win_size[0]/2, .2*self.win_size[1])))
        font = pg.font.Font(None, int(self.square_size/20))
        text = font.render(f"Score: {score}", True, self.color)
        self.win.blit(text, text.get_rect(center=(self.win_size[0]/2, .5*self.win_size[1])))
        font = pg.font.Font(None, int(self.square_size/20))
        text = font.render("Press R to restart", True, self.color)
        self.win.blit(text, text.get_rect(center=(self.win_size[0]/2, .9*self.win_size[1])))

    def resize(self, win_size):
        self.win_size = win_size
        self.square_size = min(win_size)
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2

class OverheadText:
    def __init__(self, win, win_size, text, font=None, color=(0,0,0)):
        self.win = win
        self.win_size = win_size
        self.square_size = min(win_size)
        self.text = text
        self.font = pg.font.Font(font, int(self.square_size/10))
        self.color = color
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2

    def draw(self):
        text = self.font.render(self.text, True, self.color)
        self.win.blit(text, text.get_rect(center=(self.win_size[0]/2, .2*self.win_size[1])))

    def set_text(self, text):
        self.text = text

    def resize(self, win_size):
        self.win_size = win_size
        self.square_size = min(win_size)
        self.font = pg.font.Font(None, int(self.square_size/10))
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2

class Music():
    def __init__(self):
        self.paths = [f"music/{i*15}.wav" for i in range(6, 15)]
        self.bpm = 90
        self.music = pg.mixer.music.load(self.paths[0])
        self.playing = False

    def play(self):
        if not self.playing:
            pg.mixer.music.play(-1)
            self.playing = True

    def stop(self):
        if self.playing:
            pg.mixer.music.stop()
            self.playing = False

    def toggle(self):
        if self.playing:
            self.stop()
        else:
            self.play()

    def pause(self):
        if self.playing:
            pg.mixer.music.pause()
            self.playing = False

    def resume(self):
        if not self.playing:
            pg.mixer.music.unpause()
            self.playing = True

    def reset(self):
        pg.mixer.music.rewind()
        self.play()

    def set_bpm(self, bpm):
        self.bpm = bpm
        pg.mixer.music.load(self.paths[int(bpm/15 - 6)])
        self.play()

    def speed_up(self):
        if self.bpm < 210:
            self.stop()
            self.set_bpm(self.bpm + 15)
            return True
        return False

    def reset_speed(self):
        self.set_bpm(90)
        
class Element:
    def __init__(self, win, win_size, square_size, y, height, colors, player_size=.05):
        self.win = win
        self.win_size = win_size
        self.square_size = square_size
        self.width = square_size/3
        self.y = y
        self.height = max(height * self.square_size, 1)
        if height > 1:
            self.height = max(self.height, player_size * self.square_size * 2)
        
        if colors == None:
            self.colors = [(200,200,200) for i in range(3)]
        else:
            self.colors = colors
        self.player_size = player_size
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2
        self.rects = []
        self.set_rects()

    def __repr__(self) -> str:
        return f"Element({self.y}, {self.height}, {self.colors})"

    def set_rects(self):
        self.rects = [pg.Rect(self.offset_x + self.width*i-1, self.offset_y + self.y - self.height-1, self.width+2, self.height+2) for i in range(3)]

    def draw(self):
        for i in range(3):
            pg.draw.rect(self.win, self.colors[i], self.rects[i])

    def move(self, speed):
        self.y += speed
        for i in range(3):
            self.rects[i].y += speed
        return self.y - self.height > self.square_size

    def collide(self, top_color, hitbox):
        if self.colors == [(200,200,200) for i in range(3)]:
            return False
        
        min = int(3*(hitbox.x-self.offset_x)) // self.square_size
        max = int(3*(hitbox.x+hitbox.width-self.offset_x)) // self.square_size
        
        for i in range(min, max+1):
            if self.colors[i] != top_color and self.rects[i].colliderect(hitbox):
                return True
        return False
    
    def resize(self, win_size, square_size):
        self.y = self.y * square_size / self.square_size
        self.win_size = win_size
        self.square_size = square_size
        self.width = square_size/3
        self.height = max(self.height * self.square_size, 1)
        if self.height > 1:
            self.height = max(self.height, self.player_size * self.square_size * 2)
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2
        self.set_rects()

    def get_color(self, index):
        return self.colors[index]

class Stage:
    def __init__(self, win, win_size, square_size):
        self.win = win
        self.win_size = win_size
        self.square_size = square_size
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2
        self.elements = []
        self.colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,255), (255,255,0), (255,128,0)]
        self.base_p=.8
        self.p = self.base_p

    def rect(self, colors, height):
        if self.elements == []:
            y_offset = 0
        else:
            y_offset = self.elements[-1].y - self.elements[-1].height
            y_offset = min(y_offset, 0)

        if len(self.elements) < 10:
            self.elements.append(Element(self.win, self.win_size, self.square_size, y_offset, height, colors))

    def rect2(self, colors):
        self.elements.append(Element(self.win, self.win_size, self.square_size, 0, 1, colors))
        self.fix_element_height()

    def line(self):
        self.rect([(0,0,0) for i in range(3)], 0)

    def draw(self):
        for element in self.elements:
            if element.y > 0:
                element.draw()

    def move(self, speed): # weird movement means element skipped over when another element is removed
        speed = int(np.round(speed * self.square_size))
        remove = []
        for element in self.elements:
            if element.move(speed):
                remove.append(element)
        for element in remove:
            self.elements.remove(element)

    def collide(self, player):
        player_y = player.point_to_absolute(player.y, False)
        player_x = player.point_to_absolute(player.x, True)
        top_color = player.state.get_color(np.array((0,0,1)))
        mini_size = player.true_size * .4
        hitbox = pg.Rect(player_x - mini_size, player_y - mini_size, mini_size*2, mini_size*2)
        for element in self.elements:
            if element.y < player_y - mini_size or element.y - element.height > player_y + mini_size:
                continue
            if element.collide(top_color, hitbox):
                return True
        return False

    def add_obstacle(self, colors=None, height=None):
        if height is None:
            height = rd.random() * .5 + .25

        self.rect(colors, height)

    def add_obstacle2(self, colors=None):
        self.rect2(colors)

    def reset(self):
        self.elements = []
        self.p = self.base_p

    def resize(self, win_size):
        self.win_size = win_size
        self.square_size = min(self.win_size[0], self.win_size[1])
        self.offset_y = (self.win_size[1] - self.square_size) / 2
        self.offset_x = (self.win_size[0] - self.square_size) / 2
        for element in self.elements:
            element.resize(win_size, self.square_size)

    def add_random_obstacle(self):
        # self.add_obstacle2([rd.choice(self.colors) for i in range(3)])
        colors = []
        for i in (0,2):
            colors.append(self.pick_color(i, []))
        colors.insert(1, self.pick_color(1, colors))
        self.add_obstacle2(colors)

    def fix_element_height(self):
        if len(self.elements) < 2:
            return
        element = self.elements[-2]
        element.height = min(element.height, element.y)
        # self.elements[element_index] = element
        element.set_rects()

    def remove_all_unshown(self):
        remove = []
        for element in self.elements:
            if element.y < 0:
                remove.append(element)
        for element in remove:
            self.elements.remove(element)

    def pick_color(self, index, n):
        neighbors = [self.elements[-1].get_color(index)]
        if index == 1:
            neighbors += n

        if rd.random() < self.p:
            return rd.choice(neighbors)
        else:
            return rd.choice(self.colors)
        
    def update_p(self):
        self.p = .8*self.p

class PlayerState:
    def __init__(self):
        fd = dict(color=(0,255,0), direction=np.array((0,1,0)))
        bk = dict(color=(0,0,255), direction=np.array((0,-1,0)))
        up = dict(color=(255,255,255), direction=np.array((0,0,1)))
        dn = dict(color=(255,255,0), direction=np.array((0,0,-1)))
        rt = dict(color=(255,128,0), direction=np.array((1,0,0)))
        lt = dict(color=(255,0,0), direction=np.array((-1,0,0)))
        self.state = [fd, bk, up, dn, rt, lt]
        self.rotate(np.array((0,0,1)))
        self.rotate(np.array((0,0,1)))

    def rotate(self, axis):
        for side in self.state:
            new_dir = np.cross(axis, side['direction'])
            if np.dot(new_dir, new_dir) != 0:
                side['direction'] = new_dir

    def get_color(self, direction):
        for side in self.state:
            if np.dot(side['direction'], direction) == 1:
                return side['color']

class Player:
    def __init__(self, win, win_size, square_size):
        self.win = win
        self.win_size = win_size
        self.square_size = square_size
        self.base_speed = 0.005
        self.speed = self.base_speed
        self.angle = 0
        self.goal_angle = 0
        self.base_angular_speed = 4
        self.angular_speed = self.base_angular_speed
        self.base_jump_speed = .02
        self.jump_speed = self.base_jump_speed
        self.color_ratio = .8
        self.double_flip = False
        self.dts = 1

        self.state = PlayerState()

        self.x = 0.5
        self.y = 0.8

        self.color = (100,100,100)
        self.s = .05
        self.size = 0.05
        self.absolute_offset = ((self.win_size[0] - self.square_size)/2, (self.win_size[1] - self.square_size)/2)
        self.true_size = self.size*square_size

        self.rotating = 0

        self.jumping = 0
        self.front_jump_dir = 0

    def point_to_absolute(self, p, on_x=True):
        if on_x:
            return self.absolute_offset[0] + p*(self.win_size[0] - 2*self.absolute_offset[0])
        else:
            return self.absolute_offset[1] + p*(self.win_size[1] - 2*self.absolute_offset[1])


    def draw_side(self, direction, angle):
        color = self.state.get_color(direction)
        direction = direction[:-1]
        direction = np.array((direction[0]*np.cos(np.radians(angle)) - direction[1]*np.sin(np.radians(angle)), direction[0]*np.sin(np.radians(angle)) + direction[1]*np.cos(np.radians(angle))))
        
        left = self.color_ratio * np.array((direction[1], -direction[0]))
        right = self.color_ratio * np.array((-direction[1], direction[0]))
        left_point = (self.point_to_absolute(self.x, True) + direction[0]*self.true_size/2 + left[0]*self.true_size/2, self.point_to_absolute(self.y, False) + direction[1]*self.true_size/2 + left[1]*self.true_size/2)
        right_point = (self.point_to_absolute(self.x, True) + direction[0]*self.true_size/2 + right[0]*self.true_size/2, self.point_to_absolute(self.y, False) + direction[1]*self.true_size/2 + right[1]*self.true_size/2)
        
        pg.draw.line(self.win, color, left_point, right_point, int(np.round(self.size/self.s)))

    def draw_jump_rotation(self, dir):
        if self.double_flip and dir==0:
            dir = 1
        
        j = self.jumping - (self.double_flip*.2)
        if j > .5:
            j = .5
        elif j < 0:
            j = 0
        theta = dir*j*90*(self.double_flip+1)*2
        
        x = self.point_to_absolute(self.x, True)
        y = self.point_to_absolute(self.y, False)
        size = self.true_size

        if theta%360 < 90:
            up_color = self.state.get_color(np.array((0,0,1)))
            down_color = self.state.get_color(np.array((0,1,0)))
        elif theta%360 < 180:
            up_color = self.state.get_color(np.array((0,1,0)))
            down_color = self.state.get_color(np.array((0,0,-1)))
        elif theta%360 < 270:
            up_color = self.state.get_color(np.array((0,0,-1)))
            down_color = self.state.get_color(np.array((0,-1,0)))
        else:
            up_color = self.state.get_color(np.array((0,-1,0)))
            down_color = self.state.get_color(np.array((0,0,1)))

        
        theta = theta%90
        edge = y + size/2 - (theta)/90*size
        scaling_factor = 0.2
        width = size * (scaling_factor * cscsc[int(theta)%90] + (1-scaling_factor))
        height = size/2 * cscsc[int(theta)%90]
        ratio = self.color_ratio

        pg.draw.polygon(self.win, self.color, ((x - size/2, y + height), (x - width/2, edge), (x - size/2, y - height), (x + size/2, y - height), (x + width/2, edge), (x + size/2, y + height)))

        pg.draw.line(self.win, (0,0,0), (x - width/2, edge), (x + width/2, edge), 1)
        pg.draw.polygon(self.win, (0,0,0), ((x - size/2, y + height), (x - width/2, edge), (x - size/2, y - height), (x + size/2, y - height), (x + width/2, edge), (x + size/2, y + height)), 1)

        up_buffer = (1-ratio)*(y+height-edge)/2
        down_buffer = (1-ratio)*(edge-y+height)/2
        new_width = ratio*width + (1-ratio)*size

        # if not self.double_flip or self.jumping < .25:
        #     if dir > 0:
        #         up_color = self.state.get_color(np.array((0,0,1)))
        #         down_color = self.state.get_color(np.array((0,1,0)))
        #     else:
        #         down_color = self.state.get_color(np.array((0,0,1)))
        #         up_color = self.state.get_color(np.array((0,-1,0)))
        # else:
        #     if dir > 0:
        #         down_color = self.state.get_color(np.array((0,0,-1)))
        #         up_color = self.state.get_color(np.array((0,1,0)))
        #     else:
        #         up_color = self.state.get_color(np.array((0,0,-1)))
        #         down_color = self.state.get_color(np.array((0,-1,0)))

        # if up_buffer < down_buffer:
        #     side_color = darken(side_color, down_buffer/up_buffer)
        # else:
        #     top_color = darken(top_color, up_buffer/down_buffer)

        pg.draw.polygon(self.win, down_color, ((x - ratio*new_width/2, edge + up_buffer), (x + ratio*new_width/2, edge + up_buffer), (x + ratio*size/2, y+height-up_buffer), (x - ratio*size/2, y+height-up_buffer)))
        pg.draw.polygon(self.win, up_color, ((x - ratio*new_width/2, edge - down_buffer), (x + ratio*new_width/2, edge - down_buffer), (x + ratio*size/2, y-height+down_buffer), (x - ratio*size/2, y-height+down_buffer)))
        
        left_color = self.state.get_color(np.array((-1,0,0)))
        right_color = self.state.get_color(np.array((1,0,0)))

        pg.draw.line(self.win, right_color, (x + new_width/2, edge - down_buffer), (x+size/2, y-height+up_buffer), 2)
        pg.draw.line(self.win, right_color, (x + size/2, y+height-up_buffer), (x + new_width/2, edge - down_buffer), 2)
        pg.draw.line(self.win, left_color, (x - new_width/2, edge - down_buffer), (x - size/2, y-height+up_buffer), 2)
        pg.draw.line(self.win, left_color, (x - size/2, y+height-up_buffer), (x - new_width/2, edge - down_buffer), 2)

    def draw(self):
        self.angle = self.angle % 360
        if self.double_flip or self.front_jump_dir != 0:
            self.draw_jump_rotation(self.front_jump_dir)
        else:
            draw_rect(self.win, self.point_to_absolute(self.x, True), self.point_to_absolute(self.y, False), self.angle, self.true_size, self.color)
            draw_rect(self.win, self.point_to_absolute(self.x, True), self.point_to_absolute(self.y, False), self.angle, self.true_size*self.color_ratio, self.state.get_color(np.array((0,0,1))))
            self.draw_side(np.array((0,1,0)), self.angle)
            self.draw_side(np.array((0,-1,0)), self.angle)
            self.draw_side(np.array((1,0,0)), self.angle)
            self.draw_side(np.array((-1,0,0)), self.angle)

        
    def rotate(self):
        if self.rotating == 0:
            return

        self.angle += self.rotating * self.angular_speed * self.dts
        self.angle = self.angle % 360

        if np.abs(self.goal_angle - self.angle) < self.angular_speed * self.dts:
            if self.rotating > 0:
                self.state.rotate(np.array((0,0,1)))
            else:
                self.state.rotate(np.array((0,0,-1)))
                
            self.angle = 0
            self.rotating = 0

    def jump(self):
        if self.jumping > 0:
            if self.angle != 0:
                if self.angle < 45 or self.angle > 315:
                    self.angle = 0
                    self.rotating = 0
                    self.goal_angle = 0
                elif self.angle >= 45 and self.angle < 135:                    
                    self.angle = 0
                    self.rotating = 0
                    self.goal_angle = 0
                    self.state.rotate(np.array((0,0,1)))
                else:
                    self.angle = 0
                    self.rotating = 0
                    self.goal_angle = 0
                    self.state.rotate(np.array((0,0,-1)))

            if self.jumping < .5:
                self.jumping += self.base_jump_speed * self.dts
            else:
                self.jumping += self.jump_speed * self.dts

            self.size = self.s * (2 - (2*self.jumping - 1)**2)
            self.true_size = self.size*self.square_size

            if self.jumping > 1:
                self.speed *= .5
                self.jumping = 0

                if self.double_flip:
                    self.state.rotate(np.array((1,0,0)))
                    self.state.rotate(np.array((1,0,0)))
                else:
                    if self.front_jump_dir > 0:
                        self.state.rotate(np.array((1,0,0)))
                    elif self.front_jump_dir < 0:
                        self.state.rotate(np.array((-1,0,0)))

                self.front_jump_dir = 0
                self.size = self.s
                self.true_size = self.size*self.square_size
                self.double_flip = False

    def move(self, move):
        # norm = np.linalg.norm(move)

        if move[0]==0:
            return
        
        self.x += self.speed * move[0] * self.dts
        # self.y += self.speed * move[1]/norm

        buffer = .0075

        if self.x < self.size*cscsc[int(self.angle)]/2 + buffer:
            self.x = self.size*cscsc[int(self.angle)]/2 + buffer
        elif self.x > 1-self.size*cscsc[int(self.angle)]/2 - buffer:
            self.x = 1-self.size*cscsc[int(self.angle)]/2 - buffer
        
        # if self.y < self.size*cscsc[self.angle]/2 + buffer:
        #     self.y = self.size*cscsc[self.angle]/2 + buffer
        # elif self.y > 1-self.size*cscsc[self.angle]/2 - buffer:
        #     self.y = 1-self.size*cscsc[self.angle]/2 - buffer
    
    def reset(self):
        self.x = .5
        self.y = .8
        self.angle = 0
        self.state = PlayerState()
        self.jumping = 0
        self.rotating = 0
        self.goal_angle = 0
        self.front_jump_dir = 0
        self.double_flip = False

        self.size = self.s
        self.true_size = self.size*self.square_size
        self.speed = self.base_speed
        self.angular_speed = self.base_angular_speed
        self.jump_speed = self.base_jump_speed

        self.dts = 1

    def resize(self, win_size):
        self.win_size = win_size
        self.square_size = min(win_size[0], win_size[1])
        self.true_size = self.size*self.square_size
        self.absolute_offset = ((self.win_size[0] - self.square_size)/2, (self.win_size[1] - self.square_size)/2)

        

class Game:
    def __init__(self, win, win_size):
        self.win = win
        self.win_size = win_size
        self.sqaure_size = min(win_size[0], win_size[1])
        self.bg_color = (200,200,200)
        self.player = Player(win, win_size, self.sqaure_size)
        self.stage = Stage(win, win_size, self.sqaure_size)
        self.hold_time = {}
        self.obstacle_speed = .005
        self.delay = 0
        self.p = time.time()
        self.start = False
        self.tutorial_obstacles = self.fill_tutorial_obstacles()
        self.transition_obstacles = self.fill_transition_obstacles()
        self.score = 0
        self.in_tutorial = True
        self.tutorial = True
        self.start_time = time.time()
        self.paused = False
        self.pause_start_time = 0
        self.pause_time = 0
        self.shift_time = 0
        self.space_hold_time = 0
        self.transition_start_time = 0

        self.game_over = False

        upgrade_buttons = {
        "Fall Speed Level 1": self.increase_jump_speed,
        "Angular Speed Level 1": self.increase_angular_speed,
        "Move Speed Level 1": self.increase_move_speed,
        }
    
        self.upgrade_menu = Menu(win, [1,1,1], upgrade_buttons, y_buffer=0.05, x_buffer=0.05, win_size=win_size)

        self.goal_scores = [100] + [100+50*i for i in range(1,7)]

        self.music = Music()
        self.music.play()

        self.overhead_text = OverheadText(win, win_size, "Press SPACE to start")

        self.invulnerable = False

        self.last_frame_time = time.time()
        self.current_frame_time = time.time()
        self.dts = 1

        pg.draw.rect(self.win, self.bg_color, ((self.win_size[0] - self.sqaure_size)/2,(self.win_size[1] - self.sqaure_size)/2,self.sqaure_size,self.sqaure_size))

    def fill_transition_obstacles(self):
        WHITE = (255,255,255)
        return [None, [WHITE]*3]*6

    def fill_tutorial_obstacles(self):
        WHITE = (255,255,255)
        RED = (255,0,0)
        GREEN = (0,255,0)
        BLUE = (0,0,255)
        YELLOW = (255,255,0)
        ORANGE = (255,128,0)
        # height = 4/3 * 100 * int(self.obstacle_speed * self.sqaure_size) / self.sqaure_size
        
        return [None, [BLUE]*3] + \
            [None, [YELLOW]*3] + \
            [None, [GREEN]*3] + \
            [None, [WHITE]*3] + \
            [None, [GREEN]*3] + \
            [None, [YELLOW]*3] + \
            [None, [BLUE]*3] + \
            [None, [WHITE]*3] + \
            [None, [RED]*3] + \
            [[RED]*3, [BLUE]*3] + \
            [[BLUE]*3, [WHITE]*3] + \
            [[WHITE]*3, [WHITE]*3] + \
            [[ORANGE]*3, [ORANGE]*3] + \
            [[BLUE]*3, [BLUE]*3] + \
            [[WHITE]*3, [WHITE]*3] + \
            [[WHITE]*3, [WHITE]*3] + \
            [[YELLOW]*3, [YELLOW]*3] + \
            [[WHITE]*3, [YELLOW]*3] + \
            [[WHITE]*3, [WHITE]*3] + \
            [[WHITE, YELLOW, WHITE], [YELLOW, WHITE, YELLOW]] + \
            [[GREEN]*3, [RED, BLUE, RED]] + \
            [[YELLOW, RED, WHITE], [WHITE, BLUE, YELLOW]] + \
            [[WHITE]*3, [WHITE]*3]             

    def run(self, events, k, prev_k):
        
        pg.draw.rect(self.win, self.bg_color, ((self.win_size[0] - self.sqaure_size)/2,(self.win_size[1] - self.sqaure_size)/2,self.sqaure_size,self.sqaure_size))
        self.stage.draw()
        self.player.draw()
        
        # self.invulnerable = k[pg.K_q] or self.invulnerable
        
        if self.game_over or (not self.invulnerable and self.player.jumping == 0 and self.stage.collide(self.player)):
            self.game_over = True
            return True
        
        if self.paused:
            self.resume()

        self.current_frame_time = time.time()
        
        self.dts = 100 * (self.current_frame_time - self.last_frame_time)

        self.player.dts = self.dts
        
        # if len(self.stage.elements) < 9:
        #     self.stage.add_obstacle(self.tutorial_obstacles[0]['colors'], self.tutorial_obstacles[0]['height'])
        #     self.tutorial_obstacles = self.tutorial_obstacles[1:]

        # print(time.time() - self.p - self.pause_time - self.shift_time)

        if time.time() - self.p - self.pause_time - self.shift_time > 120/self.music.bpm:
            self.score += (self.transition_start_time==0 and not k[pg.K_LSHIFT])
            self.p = time.time() - self.pause_time - self.shift_time
            if len(self.transition_obstacles) > 0:
                self.stage.add_obstacle2(self.transition_obstacles[0])
                self.transition_obstacles = self.transition_obstacles[1:]
            elif len(self.tutorial_obstacles) > 0:
                self.stage.add_obstacle2(self.tutorial_obstacles[0])
                self.tutorial_obstacles = self.tutorial_obstacles[1:]
            else:
                self.in_tutorial = False
                self.stage.add_random_obstacle()

        move = self.start and (not k[pg.K_LSHIFT] or len(self.transition_obstacles) == 0)
        self.stage.move(self.obstacle_speed*move*self.dts)

        self.player.move((k[pg.K_d]-k[pg.K_a], 0))

        space = k[pg.K_SPACE]

        if space:
            if pg.K_SPACE not in self.hold_time:
                self.hold_time[pg.K_SPACE] = time.time()
        else:
            if pg.K_SPACE in self.hold_time:
                del self.hold_time[pg.K_SPACE]

        if pg.K_SPACE in self.hold_time:
            self.space_hold_time = time.time() - self.hold_time[pg.K_SPACE]
            
        if k[pg.K_LSHIFT]:
            if pg.K_LSHIFT not in self.hold_time:
                self.hold_time[pg.K_LSHIFT] = time.time()
        else:
            if pg.K_LSHIFT in self.hold_time:
                if len(self.transition_obstacles) > 0 and self.start:
                    self.shift_time += time.time() - self.hold_time[pg.K_LSHIFT]
                del self.hold_time[pg.K_LSHIFT]

        if self.player.rotating != 0:
            self.player.rotate()
            self.player.goal_angle = (self.player.rotating*90 + 360)%360
        else:
            self.player.rotating = check_key(k, prev_k, pg.K_RIGHT) - check_key(k, prev_k, pg.K_LEFT)

        if self.player.jumping == 0:
            if space:
                self.player.jumping = .01
                self.player.speed *= 2
                self.player.front_jump_dir = k[pg.K_UP] - k[pg.K_DOWN]
        else:
            if pg.K_SPACE in self.hold_time and self.space_hold_time > .2:
                self.player.double_flip = self.player.front_jump_dir == 0

            self.player.jump()    
        
        if self.start:
            self.overhead_text.set_text(self.text(time.time() - self.start_time - self.pause_time - self.shift_time))
        else:
            self.start = k[pg.K_SPACE]
            if self.start:
                self.start_time = time.time()
        self.overhead_text.draw()

        if self.score in self.goal_scores:
            self.transition_obstacles = [None]
            if self.transition_start_time == 0:
                self.transition_start_time = time.time()
            elif time.time() - self.transition_start_time > 6:
                self.upgrade_menu.run(events)

        self.last_frame_time = self.current_frame_time

        return False
    
    def reset(self):
        self.player.reset()
        self.stage.reset()
        self.hold_time = {}
        self.p = time.time()
        if self.tutorial:
            self.tutorial_obstacles = self.fill_tutorial_obstacles()
        else:
            self.tutorial_obstacles = []
        self.start = False
        self.score = 0
        self.obstacle_speed = .005
        self.transition_obstacles = self.fill_transition_obstacles()
        self.in_tutorial = True
        self.start_time = time.time()
        self.overhead_text.set_text("Press SPACE to Start")
        self.pause_time = 0
        self.shift_time = 0
        self.game_over = False
        try:
            self.music.reset_speed()
            self.music.reset()
        except:
            pass

    def resize(self, win_size):
        self.win_size = win_size
        self.sqaure_size = min(win_size[0], win_size[1])
        self.player.resize(win_size)
        self.stage.resize(win_size)
        pg.draw.rect(self.win, self.bg_color, ((self.win_size[0] - self.sqaure_size)/2,(self.win_size[1] - self.sqaure_size)/2,self.sqaure_size,self.sqaure_size))
        self.upgrade_menu.resize(win_size)
        self.overhead_text.resize(win_size)

    def speed_up(self):
        self.stage.remove_all_unshown()
        self.transition_obstacles = self.fill_transition_obstacles()
        self.tutorial_obstacles = []
        self.obstacle_speed += .0002
        self.music.speed_up()
        self.stage.update_p()

    def text(self, time):
        tau = 4/3
        c = 2
        b = self.delay/1000+1
        if self.tutorial and self.in_tutorial:
            if time < b:
                return "TETSURO"
            elif time < b + tau*6*c:
                return "Tap [SPACE] to jump"
            elif time < b + tau*10*c:
                return "Hold [^] and tap [SPACE]"
            elif time < b + tau*14*c:
                return "Hold [v] and tap [SPACE]"
            elif time < b + tau*18*c:
                return "Tap [<] to rotate"
            elif time < b + tau*22*c:
                return "Tap [>] to rotate"
            elif time < b + tau*24*c:
                return "Hold [SPACE] to double flip"
            else:
                return "Use [A] and [D] to move"
            
        else:
            return str(self.score)
        
    def pause(self):
        self.paused = True
        self.pause_start_time = time.time()
        self.music.pause()

    def resume(self):
        self.paused = False
        self.pause_time = time.time() - self.pause_start_time
        self.music.resume()

    def increase_jump_speed(self, button):
        self.player.jump_speed += .01
        button.change_name("Fall Speed Level " + str(int(np.round((self.player.jump_speed - self.player.base_jump_speed)/.01)) + 1))
        self.upgrade_close()

    def increase_angular_speed(self, button):
        self.player.angular_speed += .5
        button.change_name("Angular Speed Level " + str(int(np.round((self.player.angular_speed - self.player.base_angular_speed)/.5)) + 1))
        self.upgrade_close()

    def increase_move_speed(self, button):
        self.player.speed += .0025
        button.change_name("Move Speed Level " + str(int(np.round((self.player.speed - self.player.base_speed)/.0025)) + 1))
        self.upgrade_close()

    def upgrade_close(self):
        self.transition_start_time = 0
        self.goal_scores = self.goal_scores[1:]
        self.speed_up()


def exit(button):
    pg.quit()
    quit()

if __name__ == "__main__":
    pg.init()
    win_size = (800, 600)
    win = pg.display.set_mode(win_size, RESIZABLE)
    pg.display.set_caption("Menu Test")
    paused = False
    game = Game(win, win_size)
    is_over = False
    difficulty = 0

    def reset(button):
        global paused, is_over
        game.reset()
        paused = False
        is_over = False

    def increase_delay(button):
        game.delay += 100
        game.reset() 

    def toggle_tutorial(button):
        game.tutorial = not game.tutorial
        name = "Tutorial On" if game.tutorial else "Tutorial Off"
        if not game.tutorial and len(game.transition_obstacles) > 0:
            game.tutorial_obstacles = []
        button.change_name(name)

    def change_difficulty(button):
        global difficulty
        difficulty = (difficulty + 1)%3
        game.stage.base_p = [.8, .5, .3][difficulty]
        name = "Difficulty: " + ["Easy", "Medium", "Hard"][difficulty]
        if not game.start or time.time() - game.start_time < 20:
            game.stage.p = game.stage.base_p
        button.change_name(name)

    def resume(button):
        global paused
        paused = False

    button_format = [2, 2, 1]
    buttons = {
            "Reset": reset,
            "Tutorial On": toggle_tutorial,
            "Difficulty: Easy": change_difficulty,
            "Quit Game": exit,
            "Resume": resume,
            }

    menu = Menu(win, button_format, buttons, y_buffer=0.05, x_buffer=0.05, win_size=win_size)

    running = True
    prev_k = pg.key.get_pressed()

    game_over = GameOverScreen(win, win_size)

    p = time.time()

    while running:
        pg.time.delay(10)

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                win_size = event.size
                menu.resize(event.size)
                game.resize(event.size)
                game_over.resize(event.size)

        k = pg.key.get_pressed()
                
        if check_key(k, prev_k, pg.K_ESCAPE):
            paused = not paused
            if paused:
                menu.draw()
                game.pause()

        if check_key(k, prev_k, pg.K_r):
            reset(None)

        if paused:
            menu.run(events)
        else:
            win.fill((0,0,0))
            is_over = game.run(events, k, prev_k) or is_over
            if is_over:
                game.start = False
                try:
                    game.music.pause()
                except:
                    pass
                game_over.draw(game.score)

        pg.display.update()
        prev_k = k

    pg.quit()
    quit()