import pygame
from pygame.locals import *
from utilities.matrix_helpers import *
from utilities.colors import *
from settings import *
from entities.board import Board


# #
# Pygame initialization
# #

pygame.init()
font = pygame.font.SysFont("Arial", 10)


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
opposite_view = False
while True:
    event = pygame.event.poll()
    screen.fill((0,0,0))
    
    if event.type == pygame.QUIT:
        pygame.quit()
        exit
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB:
            # toggle views    
            opposite_view = not opposite_view

            if not opposite_view:
                angles = [
                    math.radians(30),  # X-Achse: 30° nach unten geneigt
                    math.radians(45),  # Y-Achse: 45° gedreht
                    0                  # Z-Achse: keine Rotation
                ]
            else:
                angles = [
                    math.radians(30),  # X-Achse: 30° nach unten geneigt
                    math.radians(225),  # Y-Achse: 225° gedreht
                    0                  # Z-Achse: keine Rotation
                ]

        if event.key == pygame.K_1:
            angles = [
                math.radians(30),  # X-Achse: 30° nach unten geneigt
                math.radians(0),  # Y-Achse: 0°° gedreht
                0                  # Z-Achse: keine Rotation
            ]
        if event.key == pygame.K_2:
            angles = [
                math.radians(30),  # X-Achse: 30° nach unten geneigt
                math.radians(90),  # Y-Achse: 90° gedreht
                0                  # Z-Achse: keine Rotation
            ]
        if event.key == pygame.K_3:
            angles = [
                math.radians(30),  # X-Achse: 30° nach unten geneigt
                math.radians(180),  # Y-Achse: 180° gedreht
                0                  # Z-Achse: keine Rotation
            ]
        if event.key == pygame.K_4:
            angles = [
                math.radians(30),  # X-Achse: 30° nach unten geneigt
                math.radians(270),  # Y-Achse: 270° gedreht
                0                  # Z-Achse: keine Rotation
            ]
        if event.key == pygame.K_ESCAPE:
            board.unselect_box()
        if event.key == pygame.K_LSHIFT:
            shift_pressed = True
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LSHIFT:
            shift_pressed = False

        if event.key == pygame.K_d:
            if opposite_view == True:
                x,y,z = board.active_box
                x-=1
                if x < 0:
                    x = board.columns - 1
                board.active_box.x = x
            else:
                x,y,z = board.active_box
                x+=1
                if x > board.columns -1:
                    x = 0
                
                board.active_box.x = x
            
        if event.key == pygame.K_a:
            if opposite_view == True:
                x,y,z = board.active_box
                x+=1
                if x > board.columns -1:
                    x = 0
                
                board.active_box.x = x            
            else:
                x,y,z = board.active_box
                x-=1
                if x < 0:
                    x = board.columns - 1
                board.active_box.x = x

        if event.key == pygame.K_s:
            if opposite_view == True:
                x,y,z = board.active_box
                z+=1
                if z > board.rows - 1:
                    z = 0
                board.active_box.z = z
            else:

                x,y,z = board.active_box
                z-=1
                if z < 0:
                    z = board.rows - 1
                board.active_box.z = z

        if event.key == pygame.K_w:
            if opposite_view == True:
                x,y,z = board.active_box
                z-=1
                if z < 0:
                    z = board.rows - 1
                board.active_box.z = z
            else:
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
        # delta_y = current_mouse_pos[0] - last_mouse_pos[0]
        angles[1] += math.radians(delta_x * -0.3)  # Flüssige Rotation basierend auf Mausbewegung
        # angles[0] += math.radians(delta_y * -0.3)  # Flüssige Rotation basierend auf Mausbewegung
        last_mouse_pos = current_mouse_pos  # Aktuelle Position speichern

    
    board.draw(screen, angles)
    
    fps = int(fpsClock.get_fps())
    fps_text = font.render(f"FPS: {fps}, FOV: {FOV}, DISTANCE: {DISTANCE}, ROT_X:{int(angles[0])}, ROT_Y:{int(angles[1])}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))  # Oben links
    
    mouse_x,mouse_y = pygame.mouse.get_pos()
    mouse_text = font.render(f"Mouse_X: {mouse_x}, Mouse_Y: {mouse_y}", True, (255, 255, 255))
    screen.blit(mouse_text, (10, 30))  # Oben links
    
    if board.current_team == TEAM_WHITE:
        team_text = "Team WHITE"
    else:
        team_text = "Team BLACK"

    game_infos = font.render(f"Team: {team_text}", True, (255, 255, 255))
    screen.blit(game_infos, (10, screen.get_width() - 100))  # Oben links
    
    
    pygame.display.update()      
    fpsClock.tick(60) #11

pygame.quit()


