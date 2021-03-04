import pygame, sys, random
from canvas import Canvas
from colors import *
from vector import Vec2
from mymath import get_line_pixels

pygame.init()

width = 1280
height = 720
win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Pyxel v0.0.1-dev")

canvas = Canvas(width / 2, height / 2, 64, 64, 1)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                canvas.scale_zoom(1.1)
            elif event.y == -1:
                canvas.scale_zoom(0.9)
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL]:
                if keys[pygame.K_z]:
                    canvas.undo()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        canvas.selected_color = Vec4(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            255
        )

    win.fill(GRAY.as_tuple())
    canvas.update()
    canvas.draw(win)
    pygame.display.update()
    
pygame.quit()
sys.exit()
