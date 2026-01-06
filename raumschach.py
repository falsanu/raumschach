import pygame
from pygame.locals import *
from settings import *

from utilities.matrix_helpers import *
from utilities.colors import *
from entities.board import Board
from utilities.input_handling import InputHandler
from entities.ui import Ui

# #
# Pygame initialization
# #

pygame.init()

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
pygame.display.get_surface().set_alpha(None)  # Alpha-Blending einschalten



# Isometrische Winkel (X, Y, Z in Radians)
angles = [
    math.radians(30),  # X-Achse: 30° nach unten geneigt
    math.radians(45),  # Y-Achse: 45° gedreht
    0                  # Z-Achse: keine Rotation
]

# Board erstellen und befüllen
board = Board(ROWS, LEVEL, COLUMNS)

# Ui erstellen
ui = Ui(board)

# Input Handling initialisieren
input_handler = InputHandler(board, angles, ui)


while True:
    
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        
        # # 
        # Keyboard  Handling
        # #
        
        if event.type == pygame.KEYDOWN:
            input_handler.key_down(event)
        
        if event.type == pygame.KEYUP:
            input_handler.key_up(event)

        # # 
        # Mouse Handling
        # #

        if event.type == MOUSEWHEEL:
            input_handler.mouse_wheel(event)

        if event.type == MOUSEBUTTONDOWN:
            input_handler.mouse_button_down()

        if event.type == MOUSEBUTTONUP:
            input_handler.mouse_button_up()
        
        if event.type == pygame.MOUSEMOTION:
        # Leite die Mausbewegung an den InputHandler weiter
            input_handler.mouse_motion(event.pos)

    input_handler.update()

    
    board.draw(screen, angles)
    ui.draw(screen, angles)
    
    pygame.display.update()      
    

pygame.quit()


