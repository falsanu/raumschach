import pygame
from utilities.matrix_helpers import *
from utilities.colors import *
from utilities.tools import *
from settings import *
from entities.figures.figure import Figure

class Box:
    """
    Box which defines one three dimensional box
    """
    def __init__(self, x, y, z, size, color, orig_vector, figure=None):
        self.points = []
        self.points.append(pygame.math.Vector3(-(size),-(size),-(size)))
        self.points.append(pygame.math.Vector3(-(size),(size),-(size)))
        self.points.append(pygame.math.Vector3((size),(size),-(size)))
        self.points.append(pygame.math.Vector3((size), -(size), -(size)))    

        self.points.append(pygame.math.Vector3(-(size), (size), (size)))
        self.points.append(pygame.math.Vector3((size), (size), (size)))
        self.points.append(pygame.math.Vector3((size), -(size), (size)))
        self.points.append(pygame.math.Vector3(-(size),-(size) ,(size)))

        self.orig_vector = orig_vector
        self.figure:Figure = figure


        self.offset = pygame.math.Vector3(x, y, z)
        self.size = size
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Vorderseite
            (4, 5), (5, 6), (6, 7), (7, 4),  # Rückseite
            (0, 7), (1, 4), (2, 5), (3, 6)   # Verbindungen
        ]
        self.color = color
        self.initial_color = color
        self.is_active = False
        
        font_path = "/System/Library/Fonts/Geneva.ttf"  # macOS
        self.font = pygame.font.Font(font_path, 10)

        self.is_highlighted = False

    def set_figure(self, figure):
        self.figure = figure
    
    

    def get_projected_vertices(self):
        projected = []
        for p in self.points:
            x, y, z = p.x + self.offset.x * (2*self.size), p.y - self.offset.y*(2*self.size), p.z + self.offset.z * (2*self.size)
            projected.append(pygame.math.Vector3(x, y, z))
        
        return projected
    
    def get_projected_center(self):
        projected = self.get_projected_vertices()

        # Mittelpunkt der 3D-Punkte (vor der Projektion)
        center_3d = pygame.math.Vector3(0, 0, 0)
        for p in projected:
            center_3d += p
        center_3d /= len(projected)  # Durchschnitt aller Eckpunkte
        return center_3d
    
    def highlight(self, color):
        self.is_highlighted = True
        self.color = color
    
    def un_highlight(self):
        self.is_highlighted = False
        self.color = self.initial_color

    def draw(self, screen, fov, distance, angles):
        # 1. Punkte rotieren und projizieren
        rotated_points = [rotate_point(p, angles) for p in self.get_projected_vertices()]
        projected_points = [
            project_3d_to_2d(p, screen.get_width(), screen.get_height(), fov, distance)
            for p in rotated_points
        ]

        # 2. Kanten zeichnen
        for start_idx, end_idx in self.edges:
            start = projected_points[start_idx]
            end = projected_points[end_idx]
            if self.is_active:
                pygame.draw.line(screen, WHITE, (start.x, start.y), (end.x, end.y), 1)
            else:
                pygame.draw.line(screen, self.color, (start.x, start.y), (end.x, end.y), 1)

        # 3. Mittelpunkt im 3D-Raum berechnen (vor der Projektion!)
        center_3d = pygame.math.Vector3(0, 0, 0)
        for p in self.get_projected_vertices():  # Originale 3D-Punkte (mit Offset)
            center_3d += p
        center_3d /= len(self.points)  # Durchschnitt der 3D-Punkte

        # 4. Text-Position rotieren und projizieren
        rotated_center = rotate_point(center_3d, angles)
        projected_center = project_3d_to_2d(
            rotated_center,
            screen.get_width(),
            screen.get_height(),
            fov,
            distance
        )

        text_surface = pygame.Surface((120, 20), pygame.SRCALPHA)  # Größe anpassen
        text_surface.fill((0, 0, 0, 0))  # Vollständig transparenter Hintergrund
        
        # 5. Text mittig platzieren (jetzt korrekt im 3D-Raum)
        box_text = self.font.render(
            f"E:{int(self.orig_vector.y)+1}, {number_to_char(int(self.orig_vector.x))}, {int(self.orig_vector.z)+1}",
            True,
            (255, 255, 255)
        )
        # 3. Zeichne den Text auf das transparente Surface
        # text_surface.blit(box_text, (0, 0))
        # text_surface.set_alpha(128)  # 10 = ~4% Transparenz (0=unsichtbar, 255=undurchsichtig)

        # text_rect = text_surface.get_rect(center=(int(projected_center.x), int(projected_center.y)))
        # screen.blit(text_surface, text_rect)
