import pygame
from pygame.locals import *
from utilities.matrix_helpers import *
from utilities.colors import *
from entities.Box import Box
from settings import *
import os


import numpy as np

# Pfad zu den Homebrew-SDL2-Bibliotheken setzen
os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')
os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/opt/homebrew/lib'

print(pygame.get_sdl_version())  # Sollte die SDL-Version ausgeben
print(pygame.font.get_init())    # Sollte True ausgeben
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.get_surface().set_alpha(None)  # Alpha-Blending einschalten



fpsClock = pygame.time.Clock() #1


rows = ROWS # front back
level = LEVEL # up - down
cols = COLUMNS # left - right


size = SIZE

# 3D-Array mit None initialisieren
board = [[[None for _ in range(rows)]
             for _ in range(level)]
            for _ in range(cols)]

# Mittelpunkt des Boards berechnen
center_x = (cols - 1) / 2  # Mitte der Spalten (X-Achse)
center_y = (level - 1) / 2  # Mitte der Ebenen (Y-Achse)
center_z = (rows - 1) / 2   # Mitte der Reihen (Z-Achse)

box_counter = 0
# Befüllen des Boards mit Box-Objekten
for z in range(rows):
    for y in range(level):
        for x in range(cols):
            box_counter+=1 
            color = pygame.Color(0)  # Erstelle ein Color-Objekt (Farbe ist zunächst irrelevant)
            color.hsva = ((y * 360 // level) % 360, 100, 100, 50)  # Setze HSV-Werte (Hue, Saturation, Value, Alpha)
            
             # Offset relativ zum Mittelpunkt
            offset_x = x - center_x
            offset_y = (y - center_y) * (size + Y_SPACING)/size
            offset_z = z - center_z

            board[z][y][x] = Box(offset_x, offset_y, offset_z, size, color, pygame.math.Vector3(x,y,z))




counter = 0
# Isometrische Winkel (X, Y, Z in Radians)
angles = [
    math.radians(30),  # X-Achse: 30° nach unten geneigt
    math.radians(45),  # Y-Achse: 45° gedreht
    0                  # Z-Achse: keine Rotation
]
mousedown = False
font_path = "/System/Library/Fonts/Geneva.ttf"  # macOS
font = pygame.font.Font(font_path, 14)


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
        angles[1] += math.radians(delta_x * -0.2)  # Flüssige Rotation basierend auf Mausbewegung
        last_mouse_pos = current_mouse_pos  # Aktuelle Position speichern

    # if mousedown:
    #     mousepos = pygame.mouse.get_pos()
    #     # Nur die Y-Achse (angles[1]) mit der Maus steuern (X-Mausposition)
    #     angles[1] = math.radians(mousepos[0] * -0.5)  # Skalierung für langsamere Rotation
    

    # Befüllen mit Box-Objekten
    for z in range(rows):
        for y in range(level):
            for x in range(cols):
                box = board[z][y][x]
                box.draw(screen, FOV, DISTANCE, angles)
                
    
    fps = int(fpsClock.get_fps())
    fps_text = font.render(f"FPS: {fps}, FOV: {FOV}, DISTANCE: {DISTANCE}, ROT_X:{int(angles[0])}, ROT_Y:{int(angles[1])}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))  # Oben links
    
    mouse_x,mouse_y = pygame.mouse.get_pos()
    mouse_text = font.render(f"Mouse_X: {mouse_x}, Mouse_Y: {mouse_y}", True, (255, 255, 255))
    screen.blit(mouse_text, (10, 30))  # Oben links
    pygame.display.update()      
    fpsClock.tick(60) #11

pygame.quit()


