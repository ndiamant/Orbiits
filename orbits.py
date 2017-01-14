import pygame, sys
from pygame.locals import *
import numpy as np

pygame.init()

refresh = False
width = 1700
height = 1000
v_i = 200
num = 2 
dt = 7 
size_min = 0
size_max = 1

surface = pygame.display.set_mode((width, height), 0, 32)

pygame.display.set_caption('Orbits by ND')

def center(pos):
    return  pos + np.array([ width / 2, height / 2])

def uncenter(pos):
    return  pos - np.array([ width / 2, height / 2])

def step(moon_list, motion_law, color_rule = None, size_rule = None, refresh = False):
    if refresh:
        surface.fill((0,0,0))
    for moon in moon_list:
        motion_law(moon) 
        moon.draw(surface)
        if color_rule:
            color_rule(moon)
        if size_rule:
            size_rule(moon)
    
    pygame.display.update()

class Moon:
    def __init__(self, pos, color, size, vel):
        self.pos = pos
        self.color = color
        self.size = size
        self.vel = vel

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.pos[0]), int(self.pos[1])), self.size, 0)

# Moon list
ml = [Moon(pos = np.array([np.random.rand() * width, np.random.rand() * height]), color = np.random.randint(0,255,3), size = np.random.randint(size_min, size_max), vel = np.random.randn(2) * v_i) for _ in range(num)]

# Take 2x1 np array and cap magnitude to lim
# TODO: make this description true
def max_lim(vel, lim = 10000):
    signs = vel / np.abs(vel)
    vel = np.abs(vel)
    vel[vel > lim] = lim 
    vel *= signs
    return vel

# example motion laws
def gravity(moon):
    pos = moon.pos
    vel = moon.vel 
    acc = -100000000 * uncenter(pos) / np.linalg.norm(uncenter(pos))**3
    acc = max_lim(acc)
    vel += acc * dt / 1000
    pos += vel * dt / 1000

def linear(moon):
    pos = moon.pos
    vel = moon.vel
    acc = -100000 * uncenter(pos) / np.linalg.norm(uncenter(pos))**2
    acc = max_lim(acc)
    vel += acc * dt / 1000
    pos += vel * dt / 1000


def zero(moon):
    pos = moon.pos
    vel = moon.vel
    acc = -1000 * uncenter(pos) / np.linalg.norm(uncenter(pos))
    vel += acc * dt / 1000
    pos += vel * dt / 1000

# example size rules
def lin_dist(moon):
    moon.size = int(50 - min(48, 10e-2 *  np.linalg.norm(uncenter(moon.pos))))

# example color rules

# used in x color dependence imange
#color_list = [(3*i%255, 5*i%255, 7*i%255) for i in range(255)]

# all RGB combos, used in velocity color
#color_list = [(10*i,10*j,10*k) for i in range(25) for j in range(25) for k in range(25)]

# black and white
#color_list = [(i,i,i) for i in range(255)]

# black and white opposite order
#color_list = [(255-i,255-i,255-i) for i in range(255)]

# black and red
color_list = [(255-i,0,0) for i in range(255)]

# modify existing colors
def permute(moon):
    r,g,b = moon.color
    r = (r+1) % 255
    g = (g+1) % 255
    b = (b+1) % 255
    moon.color = (r,g,b)


def dist_fade(moon):
    d = np.linalg.norm(uncenter(moon.pos))
    l = len(color_list)
    ind = int(l - 1 - min(90 * d / l, l-1))  
    moon.color = color_list[ind]

def vel_color(moon):
    moon.color = color_list[int(moon.vel[0]) % len(color_list)]

def x_color(moon):
    moon.size = int(50 - min(48, 10e-2 *  np.linalg.norm(uncenter(moon.pos))))

# Where everything runs. change arguments of step for customization
while True:
    
    step(moon_list = ml, motion_law = linear, refresh = refresh, color_rule = permute, size_rule =lin_dist)   

    for event in pygame.event.get():
        if event.type == QUIT:

            pygame.quit()

            sys.exit()
