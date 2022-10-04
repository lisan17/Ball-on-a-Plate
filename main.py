import pygame
import numpy as np
import Control as c

# initialising the window. You can ignore this part.

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 40)

# setting plate parameters

centerX = 400
centerY = 400
plateT = 60

r = 0.1 # the radius of the ball

# loading in images and transforming them to required sixes and angles. You can ignore this part.

plate = pygame.image.load("plate.png")
plate = pygame.transform.rotate(plate, -45)
ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, (40, 40))
pivot = pygame.image.load("plain-triangle.png")

# game control variable. This variable determines if the came continues to run. You can ignore this part.

run = True


# A function used to rotate an image about its center. You can ignore this part.
def blit_rot_center(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)


# initialising game parameters

theta = 0       # the variable stores the angle of the plate with the
                # horizontal and measured positive counterclockwise.

phi = 0         # the variable stores the angle of rotation
                # of the ball about its own axis.

x = 0           # the variable stores the distance of
                # the center of the ball form the pivot.

x_vel = 0

I_pre = 0

time = 0

X = 400
Y = 0

e_pre = 0.0

SP = 0.0

# Game loop
while run:

    # checking for mouse input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                X, Y = event.pos  # gets the x and y coordinates of the mouse left click
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                X, Y = event.pos  # gets the x and y coordinates of the mouse left click and moving.

    # This is your major task. Write a function which takes in
    # any number of parameters you like and output the new system
    # variables and any other parameter you would like to track.
    SP = X - 400
    sol = c.solve(x, SP, theta, x_vel, I_pre, time, e_pre)
    dx = sol[0]
    new_theta = sol[1]
    new_t = sol[2]
    new_I = sol[3]
    new_x_vel = sol[4]
    new_e = sol[5]

    x_vel = new_x_vel
    if abs(x+dx)<300:
        x = x+dx
        I_pre = new_I
    else:
        x = 300*np.sign(x+dx)
        x_vel = -x_vel

    e_pre = new_e

    theta = new_theta
    time = new_t


    # make sure the ball rotates
    dphi = dx / r
    phi += dphi

    # setting the background colour of the screen
    screen.fill((235, 62, 74))

    # displaying the images on the screen within appropriate physical parameters,
    # for example, it is ensured that the ball is always on the plate.

    blit_rot_center(screen, plate, (centerX - 364, centerY - 364), theta)
    blit_rot_center(screen, ball, (centerX - 20 + x * np.cos(np.radians(theta)) - plateT * np.sin(np.radians(theta)),
                                   centerY - 20 - plateT * np.cos(np.radians(theta)) - x * np.sin(np.radians(theta))),
                    -phi)
    screen.blit(pivot, (centerX - 32, centerY - 32 + plateT))

    pygame.display.update()

    if (abs(SP-x)<2 and abs(x_vel)<2):
        x = SP
        x_vel = 0.0
        time = 0.0
        theta = 0.0
