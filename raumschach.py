import pygame
from pygame.locals import *

import numpy as np

pygame.init()
screen = pygame.display.set_mode((640,480))
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
FOV= 100
DISTANCE = 2
LINE_WIDTH = 1

WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (0, 255, 0)

fpsClock = pygame.time.Clock() #1

points = []
points.append(pygame.math.Vector3(-1,-1,-1))
points.append(pygame.math.Vector3(-1,1,-1))
points.append(pygame.math.Vector3(1,1,-1))
points.append(pygame.math.Vector3(1, -1, -1))    

points.append(pygame.math.Vector3(-1, 1, 1))
points.append(pygame.math.Vector3(1, 1, 1))
points.append(pygame.math.Vector3(1, -1, 1))
points.append(pygame.math.Vector3(-1,-1 ,1))



import math

def rotation_matrix_x(angle):
    # Angle in Radians
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        [1,    0,      0],
        [0,    cos_a, -sin_a],
        [0,    sin_a,  cos_a]
    ]

def rotation_matrix_y(angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        [cos_a,  0,    sin_a],
        [0,      1,    0],
        [-sin_a, 0,    cos_a]
    ]

def rotation_matrix_z(angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ]

def multiply_matrix_vector(matrix, vector):
    x = matrix[0][0] * vector.x + matrix[0][1] * vector.y + matrix[0][2] * vector.z
    y = matrix[1][0] * vector.x + matrix[1][1] * vector.y + matrix[1][2] * vector.z
    z = matrix[2][0] * vector.x + matrix[2][1] * vector.y + matrix[2][2] * vector.z
    return pygame.math.Vector3(x, y, z)


def rotate_point(point, angles):
    # angles = (x_angle, y_angle, z_angle) in Radians
    matrix_x = rotation_matrix_x(angles[0])
    matrix_y = rotation_matrix_y(angles[1])
    matrix_z = rotation_matrix_z(angles[2])

    # Rotationsreihenfolge: Z → Y → X
    rotated = multiply_matrix_vector(matrix_z, point)
    rotated = multiply_matrix_vector(matrix_y, rotated)
    rotated = multiply_matrix_vector(matrix_x, rotated)
    return rotated


edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Vorderseite
    (4, 5), (5, 6), (6, 7), (7, 4),  # Rückseite
    (0, 7), (1, 4), (2, 5), (3, 6)   # Verbindungen
]



def project_3d_to_2d(point_3d, screen_width, screen_height, fov, viewer_distance):
    # point_3d: (x, y, z)
    # fov: Field of View (z. B. 90 Grad)
    # viewer_distance: Abstand des "Auges" zur Projektionsebene
    factor = fov / (viewer_distance + point_3d.z)
    x = point_3d.x * factor + screen_width // 2
    y = point_3d.y * factor + screen_height // 2
    return pygame.math.Vector2(x, y)


counter = 0
angles = [0, 0, 0]  # [x_angle, y_angle, z_angle] in Radians
mousedown = False
while True:
    event = pygame.event.poll()
    screen.fill((0,0,0))

    
    pygame.mouse.get_pos()
    if event.type == pygame.QUIT:
        pygame.quit()
        exit
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit
    if event.type == MOUSEWHEEL:
        DISTANCE+=event.y

    if event.type == MOUSEBUTTONDOWN:
        mousedown = True
    if event.type == MOUSEBUTTONUP:
        mousedown = False
        print(mousedown)
        
        #angels = [event.x, event.y, 0]

    if mousedown:
        mousepos = pygame.mouse.get_pos()
        print(math.radians(mousepos[0]))
        angles = [math.radians(mousepos[1]), math.radians(mousepos[0]), 0]
    
    
    #angles[0] += 0.01  # X-Achse
    #angles[1] += 0.02  # Y-Achse
    # Alle Punkte rotieren
    rotated_points = [rotate_point(p, angles) for p in points]
    projected_points = [project_3d_to_2d(p, SCREEN_WIDTH, SCREEN_HEIGHT, FOV, DISTANCE) for p in rotated_points]
    


# The magic happens here
    for point in projected_points:
        pygame.draw.circle(screen, WHITE, (point.x, point.y), 3)
       
    # Zeichne alle Kanten
    for start_idx, end_idx in edges:
        start = projected_points[start_idx]
        end = projected_points[end_idx]
        pygame.draw.line(screen, (255, 255, 255), start, end, 1)
    
    
    pygame.display.update()      
    fpsClock.tick(60) #11

pygame.quit()
