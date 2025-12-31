import pygame
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


def project_3d_to_2d(point_3d, screen_width, screen_height, fov, viewer_distance):
    # point_3d: (x, y, z)
    # fov: Field of View (z. B. 90 Grad)
    # viewer_distance: Abstand des "Auges" zur Projektionsebene
    factor = fov / (viewer_distance + point_3d.z)
    x = point_3d.x * factor + screen_width // 2
    y = point_3d.y * factor + screen_height // 2
    return pygame.math.Vector2(x, y)
