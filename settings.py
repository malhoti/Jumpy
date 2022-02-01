import math
# window settings
TITLE = "JUMPY"
screen_width=700
screen_height = 800
title = "Game"
fps = 60
font = 'arial'
HIGHSCORE_FILE = 'highscore.txt'

# player settings
PLAYER_acceleration = 0.5
PLAYER_friction = -0.05
PLAYER_velocity = 3
PLAYER_gravity = 0.9
PLAYER_jump = 20

#Platfroms
PLATFROM_ARRAY = [(2,0, screen_height-40, screen_width,40)]
START_plat_num = int(math.ceil(screen_height/140))
                

#global varibales
white=(255,255,255)
red=(255,0,0)
dimmed_red = (125,0,0)
green=(0,255,0)
dimmed_green = (0,125,0)
blue= (0,0,255)
grey = (125,125,125)
black = (0,0,0)
bgcolour = (0,155,155)