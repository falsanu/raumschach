import pygame
import pygame.gfxdraw # For hardware accellerated drawing

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
       
        self.faces = [
            (0, 1, 2, 3),  # Vorderseite (z = -size)
            (7, 6, 5, 4),  # Rückseite (z = size)
            (0, 3, 6, 7),  # Untere Seite (y = -size)
            (1, 4, 5, 2),  # Obere Seite (y = size)
            (0, 1, 4, 7),  # Linke Seite (x = -size)
            (3, 2, 5, 6)   # Rechte Seite (x = size)
        ]
        # self.faces = []
        
        self.color = color
        self.initial_color = color

        self.is_active = False
        self.is_highlighted = False
        
        self.font = pygame.font.SysFont("Impact", 16)

        self.projected = self.get_projected_vertices()
        

    def set_figure(self, figure):
        self.figure = figure
    
    

    def get_projected_vertices(self):
        projected = []
        for p in self.points:
            x, y, z = p.x + self.offset.x * (2*self.size), p.y - self.offset.y*(2*self.size), p.z + self.offset.z * (2*self.size)
            projected.append(pygame.math.Vector3(x, y, z))
        
        return projected
    
    def get_projected_center(self):
        # Mittelpunkt der 3D-Punkte (vor der Projektion)
        center_3d = pygame.math.Vector3(0, 0, 0)
        for p in self.projected:
            center_3d += p
        center_3d /= len(self.projected)  # Durchschnitt aller Eckpunkte
        return center_3d
    

    
    def highlight(self, color):
        self.is_highlighted = True
        self.color = color
    
    def un_highlight(self):
        self.is_highlighted = False
        if self.figure != None:
            self.color = self.figure.get_color()
        else:
            self.color = self.initial_color

    def draw(self, screen, fov, distance, angles, current_team):
        # 1. Punkte rotieren und projizieren
        rotated_points = [rotate_point(p, angles) for p in self.projected]
        projected_points = [
            project_3d_to_2d(p, screen.get_width(), screen.get_height(), fov, distance)
            for p in rotated_points
        ]

        if self.is_active:
            # Flächen zeichnen (mit Transparenz)
            for face in self.faces:
                # Punkte der Fläche extrahieren
                face_points = [projected_points[i] for i in face]

                # Transparente Fläche erstellen
                face_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

                # Farbe basierend auf dem Team setzen
            
                color = pygame.Color(0)
                if current_team == TEAM_WHITE:
                    color.hsla = (49, 100, 80)
                    color.a = 128 # Alpha-Wert (128 = 50% Transparenz)
                else:
                    color.hsla = (298, 100, 80)
                    color.a = 128 # Alpha-Wert (128 = 50% Transparenz)

                # Polygon auf die transparente Oberfläche zeichnen
                pygame.gfxdraw.filled_polygon(
                    face_surface,
                    [(int(p.x), int(p.y)) for p in face_points],  # Punkte als ganzzahlige Koordinaten
                    (color)  # Farbe inkl. Alpha-Wert (als RGBA-Tuple)
                )
                pygame.draw.polygon(face_surface, color, [(p.x, p.y) for p in face_points])

                # Oberfläche auf den Bildschirm blitten
                screen.blit(face_surface, (0, 0))

        # Kanten zeichnen
        for start_idx, end_idx in self.edges:
            start = projected_points[start_idx]
            end = projected_points[end_idx]
            if self.is_active:
                color = pygame.Color(0)  # Erstelle ein Color-Objekt (Farbe ist zunächst irrelevant)
                if current_team == TEAM_WHITE:
                    color.hsla = (49, 100, 80)  # Setze HSV-Werte (Hue, Saturation, Value, Alpha)
                else:
                    color.hsla = (298, 100, 80)  # Setze HSV-Werte (Hue, Saturation, Value, Alpha)
                pygame.draw.line(screen, color, (start.x, start.y), (end.x, end.y), 1)
                # pygame.gfxdraw.line(screen, int(start.x), int(start.y), int(end.x), int(end.y), self.color)
            else:
                pygame.draw.line(screen, self.color, (start.x, start.y), (end.x, end.y), 1)
                # pygame.gfxdraw.line(screen, int(start.x), int(start.y), int(end.x), int(end.y), self.color)

        # Mittelpunkt im 3D-Raum berechnen (vor der Projektion!)
        center_3d = pygame.math.Vector3(0, 0, 0)
        for p in self.projected:  # Originale 3D-Punkte (mit Offset)
            center_3d += p
        center_3d /= len(self.points)  # Durchschnitt der 3D-Punkte

        # Text-Position rotieren und projizieren
        rotated_center = rotate_point(center_3d, angles)
        projected_center = project_3d_to_2d(
            rotated_center,
            screen.get_width(),
            screen.get_height(),
            fov,
            distance
        )



        
        text_surface = pygame.Surface((self.size, 20), pygame.SRCALPHA)  # Größe anpassen
        text_surface.fill((0, 0, 0, 0))  # Vollständig transparenter Hintergrund
        if self.figure != None:
            box_text = self.font.render(
                    f"{self.figure.label}",
                    True,
                    self.figure.get_color()
                )
            text_surface.blit(box_text, (0, 0))
            text_surface.set_alpha(255)  # 10 = ~4% Transparenz (0=unsichtbar, 255=undurchsichtig)

            text_rect = text_surface.get_rect(center=(int(projected_center.x), int(projected_center.y)))
            screen.blit(text_surface, text_rect)
            
        if DEBUG:
            # 5. Text mittig platzieren (jetzt korrekt im 3D-Raum)
            box_text = self.font.render(
                f"E:{int(self.orig_vector.y)+1}, {number_to_char(int(self.orig_vector.x))}, {int(self.orig_vector.z)+1}",
                True,
                (255, 255, 255)
            )

            # 3. Zeichne den Text auf das transparente Surface
            text_surface.blit(box_text, (0, 0))
            text_surface.set_alpha(128)  # 10 = ~4% Transparenz (0=unsichtbar, 255=undurchsichtig)

            text_rect = text_surface.get_rect(center=(int(projected_center.x), int(projected_center.y)))
            screen.blit(text_surface, text_rect)
