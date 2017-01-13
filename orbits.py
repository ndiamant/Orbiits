import pygame, sys
from pygame.locals import *
import numpy as np

pygame.init()

width = 1700
height = 1000
v_i = 200
num = 1000 
dt = 50

surface = pygame.display.set_mode((width, height), 0, 32)

pygame.display.set_caption('Orbits by ND')

def center(pos):
    return  pos + np.array([ width / 2, height / 2])

def uncenter(pos):
    return  pos - np.array([ width / 2, height / 2])

def step(moon_list, motion_law):
    #surface.fill((0,0,0))

    for moon in moon_list:
        moon.step(motion_law)
        moon.draw(surface)
    
    pygame.display.update()
    #pygame.time.wait(dt)


class Moon:
    def __init__(self, pos, color, size, vel):
        self.pos = pos
        self.color = color
        self.size = size
        self.vel = vel

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.pos[0]), int(self.pos[1])), self.size, 0)

    def step(self, motion_law):
        motion_law(self.pos, self.vel)

ml = [Moon(pos = np.array([np.random.rand() * width, np.random.rand() * height]), color = np.random.randint(0,255,3), size = np.random.randint(2,5), vel = np.random.randn(2) * v_i) for _ in range(num)]

def max_lim(vel, lim = 10000):
    signs = vel / np.abs(vel)
    vel = np.abs(vel)
    vel[vel > lim] = lim 
    vel *= signs
    return vel

def gravity(pos, vel):
    acc = -100000000 * uncenter(pos) / np.linalg.norm(uncenter(pos))**3
    acc = max_lim(acc)
    vel += acc * dt / 1000
    pos += vel * dt / 1000

def linear(pos, vel):
    acc = -100000 * uncenter(pos) / np.linalg.norm(uncenter(pos))**2
    acc = max_lim(acc)
    vel += acc * dt / 1000
    pos += vel * dt / 1000


def zero(pos, vel):
    acc = -1000 * uncenter(pos) / np.linalg.norm(uncenter(pos))
    vel += acc * dt / 1000
    pos += vel * dt / 1000
while True:
    
    step(ml,linear)   

    for event in pygame.event.get():
        if event.type == QUIT:

            pygame.quit()

            sys.exit()
