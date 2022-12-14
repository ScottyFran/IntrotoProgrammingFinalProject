import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
# Import os is used for images
import os
# Mixer Library is used for music 
from pygame import mixer
vec = pg.math.Vector2


# game settings 
WIDTH = 1000
HEIGHT = 600
FPS = 30


# player settings/ sets score at 0 to start
PLAYER_GRAV = 1.0
PLAYER_FRIC = 2.0
SCORE = 0


# define colors
WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)