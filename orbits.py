import pygame, sys
from pygame.locals import *
import numpy as np

pygame.init()

refresh = False
width = 1700
height = 1000
v_i = 200
num = 5 
dt = 4

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
ml = [Moon(pos = np.array([np.random.rand() * width, np.random.rand() * height]), color = np.random.randint(0,255,3), size = np.random.randint(2,5), vel = np.random.randn(2) * v_i) for _ in range(num)]

# Take 2x1 np array and cap magnitude to lim
# TODO: make this description true
def max_lim(vel, lim = 10000):
    signs = vel / np.abs(vel)
    vel = np.abs(vel)
    vel[vel > lim] = lim 
    vel *= signs
    return vel

# An example of a motion law
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

def lin_dist(moon):
    moon.size = int(50 - min(48, 10e-2 *  np.linalg.norm(uncenter(moon.pos))))

#color_list = [(3*i%255, 5*i%255, 7*i%255) for i in range(255)]
color_list = [(10*i,10*j,10*k) for i in range(25) for j in range(25) for k in range(25)]

def vel_color(moon):
    moon.color = color_list[int(moon.vel[0]) % len(color_list)]

def x_color(moon):
    moon.size = int(50 - min(48, 10e-2 *  np.linalg.norm(uncenter(moon.pos))))

# Where everything runs. change arguments of step for customization
while True:
    
    step(moon_list = ml, motion_law = linear, refresh = refresh, color_rule = vel_color, size_rule = lin_dist)   

    for event in pygame.event.get():
        if event.type == QUIT:

            pygame.quit()

            sys.exit()
