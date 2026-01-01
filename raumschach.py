import pygame
from pygame.locals import *
from utilities.matrix_helpers import *
from utilities.colors import *
from settings import *
from entities.board import Board
import os


import numpy as np

# #
# FONT Handling
# #

# Pfad zu den Homebrew-SDL2-Bibliotheken setzen
# os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')
# os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/opt/homebrew/lib'


# #
# Pygame initialization
# #


pygame.init()
font_path = "/System/Library/Fonts/Geneva.ttf"  # macOS
font = pygame.font.Font(font_path, 14)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.get_surface().set_alpha(None)  # Alpha-Blending einschalten

fpsClock = pygame.time.Clock() #1

# Board erstellen und befüllen
board = Board(ROWS, LEVEL, COLUMNS)


# Isometrische Winkel (X, Y, Z in Radians)
angles = [
    math.radians(30),  # X-Achse: 30° nach unten geneigt
    math.radians(45),  # Y-Achse: 45° gedreht
    0                  # Z-Achse: keine Rotation
]


# #
# Key Flag Initialisierung
# #
mousedown = False
shift_pressed = False

while True:
    event = pygame.event.poll()
    screen.fill((0,0,0))
    
    if event.type == pygame.QUIT:
        pygame.quit()
        exit
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            angles = [
                math.radians(30),  # X-Achse: 30° nach unten geneigt
                math.radians(45),  # Y-Achse: 45° gedreht
                0                  # Z-Achse: keine Rotation
            ]
        if event.key == pygame.K_LSHIFT:
            shift_pressed = True
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LSHIFT:
            shift_pressed = False

        if event.key == pygame.K_d:
            x,y,z = board.active_box
            x+=1
            if x > board.columns -1:
                x = 0
            
            board.active_box.x = x
            
        if event.key == pygame.K_a:
            x,y,z = board.active_box
            x-=1
            if x < 0:
                x = board.columns - 1
            board.active_box.x = x

        if event.key == pygame.K_s:
            x,y,z = board.active_box
            z-=1
            if z < 0:
                z = board.rows - 1
            board.active_box.z = z

        if event.key == pygame.K_w:
            x,y,z = board.active_box
            z+=1
            if z > board.rows - 1:
                z = 0
            board.active_box.z = z
        
        if event.key == pygame.K_e:
            x,y,z = board.active_box
            y+=1
            if y > board.level - 1:
                y = 0
            board.active_box.y = y
        
        if event.key == pygame.K_q:
            x,y,z = board.active_box
            y-=1
            if y < 0:
                y = board.level -1
            board.active_box.y = y
        if event.key == pygame.K_SPACE:
            print("SPACE")
            board.set_selected_box(board.active_box)
            

    # # 
    # Mouse-Handling
    # #

    if event.type == MOUSEWHEEL:
        if shift_pressed:
            FOV += event.y
        else:
            DISTANCE+=event.y

    if event.type == MOUSEBUTTONDOWN:
        mousedown = True
        last_mouse_pos = pygame.mouse.get_pos()  # Startposition speichern

    if event.type == MOUSEBUTTONUP:
        mousedown = False
        last_mouse_pos = None  # Zurücksetzen, wenn die Maustaste losgelassen wird


    if mousedown and last_mouse_pos is not None:
        current_mouse_pos = pygame.mouse.get_pos()
        delta_x = current_mouse_pos[0] - last_mouse_pos[0]
        angles[1] += math.radians(delta_x * -0.3)  # Flüssige Rotation basierend auf Mausbewegung
        last_mouse_pos = current_mouse_pos  # Aktuelle Position speichern

    
    # active_x, active_y, active_z = active_box
    board.draw(screen, angles)
    # Befüllen mit Box-Objekten
    # for z in range(ROWS):
    #     for y in range(LEVEL):
    #         for x in range(COLUMNS):

    #             box = board[z][y][x]
    #             box.is_active = False
    #             if active_x == x and active_y == y and active_z == z:
    #                 box.is_active = True
    #             box.draw(screen, FOV, DISTANCE, angles)
                
    
    fps = int(fpsClock.get_fps())
    fps_text = font.render(f"FPS: {fps}, FOV: {FOV}, DISTANCE: {DISTANCE}, ROT_X:{int(angles[0])}, ROT_Y:{int(angles[1])}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))  # Oben links
    
    mouse_x,mouse_y = pygame.mouse.get_pos()
    mouse_text = font.render(f"Mouse_X: {mouse_x}, Mouse_Y: {mouse_y}", True, (255, 255, 255))
    screen.blit(mouse_text, (10, 30))  # Oben links
    pygame.display.update()      
    fpsClock.tick(60) #11

pygame.quit()


