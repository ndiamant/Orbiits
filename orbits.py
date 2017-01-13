import pygame, sys
from pygame.locals import *
import numpy as np

pygame.init()

width = 1700
height = 1000
v_i = 200
num = 10 
dt = 1

surface = pygame.display.set_mode((width, height), 0, 32)

pygame.display.set_caption('Orbits by ND')

def center(pos):
    return  pos + np.array([ width / 2, height / 2])

def uncenter(pos):
    return  pos - np.array([ width / 2, height / 2])

def step(moon_list, motion_law):

    for moon in moon_list:
        motion_law(moon) 
        moon.draw(surface)
    
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


while True:
    
    step(ml,linear)   

    for event in pygame.event.get():
        if event.type == QUIT:

            pygame.quit()

            sys.exit()
