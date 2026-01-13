import pygame
from entities.box import Box
from entities.team import Team
from entities.figures.pawn import Pawn
from entities.figures.king import King
from entities.figures.bishop import Bishop
from entities.figures.knight import Knight
from entities.figures.rook import Rook
from entities.figures.queen import Queen
from utilities.matrix_helpers import rotate_point
from utilities.matrix_helpers import project_3d_to_2d

import settings

class Board:
    def __init__(self, rows, level, columns):
        self.rows = rows #z
        self.level = level #y
        self.columns = columns #x
        self.boxes = []
        self.active_box = pygame.math.Vector3(3,3,3)
        self.selected_box:Box = None 

        self.no_visibility = settings.NO_VISIBILITY
        self.current_team = settings.TEAM_WHITE
        

        self.board = [[[None for _ in range(self.rows)]
                        for _ in range(self.level)]
                            for _ in range(self.columns)]
        
        # Mittelpunkt des Boards berechnen
        center_x = (self.columns - 1) / 2  # Mitte der Spalten (X-Achse)
        center_y = (self.level - 1) / 2  # Mitte der Ebenen (Y-Achse)
        center_z = (self.rows - 1) / 2   # Mitte der Reihen (Z-Achse)
        self.center = (center_x, center_y, center_z)

        # Befüllen des Boards mit Box-Objekten
        for z in range(self.rows): #                  Z von vorne nach hinten
            for y in range(self.level): #Oben         Y von unten nach oben
                for x in range(self.columns):       # X von links nach rechts
                    color = pygame.Color(0)  # Erstelle ein Color-Objekt (Farbe ist zunächst irrelevant)
                    color.hsva = ((y * 360 // self.level) % 360, 100, 40, 70)  # Setze HSV-Werte (Hue, Saturation, Value, Alpha)
                    
                    # Box Offset relativ zum Mittelpunkt (da über die Mitte rotiert wird)
                    offset_x = (x - center_x) * (settings.SIZE + settings.BOX_SPACING)/settings.SIZE
                    offset_y = (y - center_y) * ((settings.SIZE + settings.BOX_SPACING)/settings.SIZE) * (settings.SIZE + settings.Y_SPACING)/settings.SIZE
                    offset_z = (z - center_z) * (settings.SIZE + settings.BOX_SPACING)/settings.SIZE
                    
                    # Box platzieren
                    self.board[z][y][x] = Box(offset_x, offset_y, offset_z, settings.SIZE, color, pygame.math.Vector3(x,y,z))
                    self.boxes.append(self.board[z][y][x])
        self.init_figures()
    
    def set_selected_box(self, box:pygame.math.Vector3):
        x,y,z = box
        next_box = self.board[int(z)][int(y)][int(x)]
        moved = False
        if self.selected_box != None:
            figure = self.selected_box.figure
            if figure and figure.team == self.current_team: # allow only selecting figures of currently active team
                
                for field in figure.get_target_fields():
                    target_field = field + self.selected_box.orig_vector

                    if target_field == box:
                        # possible move
                        # TODO: check for possible hits
                        print("Possible Move")
                        figure.hide_possible_target_fields()
                        figure.hide_possible_hit_fields()
                        figure.un_highlight_box()
                        
                        if next_box.figure != None: # zielbox hat eine figur
                            if next_box.figure.team != figure.team: # vom Gegner
                                # Check if field is in hit-vector
                                if field in figure.hit_vector: # is needed for PAWN-Movement, because its different from any other
                                    print("Real Hit")
                                    self.selected_box.figure = None
                                    figure.box = next_box
                                    figure.has_moved = True
                                    next_box.figure = figure
                                    moved = True
                                    break
                            else:
                                print("Same Team, select new field")
                        else: # ziel box hat keine figur
                            print("Empty Field")
                            self.selected_box.figure = None
                            figure.box = next_box
                            figure.has_moved = True
                            next_box.figure = figure
                            figure.highlight_box()
                            moved = True
                        
                        break
            else:
                print("selected figure from opponent")

        self.unselect_box()

        self.selected_box:Box = next_box
        if self.selected_box.figure != None and self.selected_box.figure.team == self.current_team:
            if not moved:
                self.selected_box.figure.show_possible_target_fields()
                self.selected_box.figure.show_possible_hit_fields()
        else:
            self.selected_box = None
        
        if moved:
            self.current_team = settings.TEAM_BLACK if self.current_team == settings.TEAM_WHITE else settings.TEAM_WHITE
            
            self.selected_box = None
            self.active_box = None
    
    def unselect_box(self):
        if self.selected_box != None:
            if self.selected_box.figure != None:
                self.selected_box.figure.hide_possible_target_fields()
                self.selected_box.figure.hide_possible_hit_fields()
        
        self.selected_box = None


    def get_box_under_mouse(self, mouse_pos, view_angle):
        """
        Gibt die Box unter den Mauskoordinaten zurück.

        :param mouse_pos: (x, y) Mausposition auf dem Bildschirm
        :param view_angle: Aktueller Blickwinkel (Rotation des Boards)
        :param fov: Field of View (Sichtfeld)
        :param viewer_distance: Abstand des Betrachters zum Board
        :return: Box-Objekt oder None
        """

        
        mouse_x, mouse_y = mouse_pos
        target_fields = []

        if self.selected_box != None:
            figure = self.selected_box.figure
            if figure and figure.team == self.current_team: # allow only selecting figures of currently active team
                for field in figure.get_target_fields():
                    target_fields.append(field + self.selected_box.orig_vector)


         
        for box in self.boxes:

            if box.figure != None or box.orig_vector in target_fields:
                # Projiziere alle 8 Eckpunkte der Box auf 2D
                box_2d_points = []
                for corner in box.get_projected_vertices():
                    # Rotieren und projizieren
                    rotated = rotate_point(corner, view_angle)
                    projected = project_3d_to_2d(rotated, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.FOV, settings.DISTANCE)
                    box_2d_points.append(projected)

                # print(f"Box {box.coordinates} projizierte Punkte: {box_2d_points}")
                # Bestimme den 2D-Bounding-Box der projizierten Box
                min_x = min(p[0] for p in box_2d_points)
                max_x = max(p[0] for p in box_2d_points)
                min_y = min(p[1] for p in box_2d_points)
                max_y = max(p[1] for p in box_2d_points)

                # Prüfe, ob der Mauszeiger innerhalb der Bounding-Box liegt
                if (min_x <= mouse_x <= max_x) and (min_y <= mouse_y <= max_y):
                    box.is_active = True
                    return box
        return None

    def draw(self, screen, angles):
        # Befüllen mit Box-Objekten
        for z in range(self.rows):
            for y in range(self.level):
                for x in range(self.columns):

                    box = self.board[z][y][x]
                    box.is_active = False
                    
                    if self.active_box.x == x and self.active_box.y == y and self.active_box.z == z:
                        box.is_active = True
                    if self.no_visibility != False:  # User schaltet leere Boxen auf Unsichtbar
                        if self.board[z][y][y].figure != None or box.is_active:
                            box.draw(screen, settings.FOV, settings.DISTANCE, angles, self.current_team)
                    else:
                        box.draw(screen, settings.FOV, settings.DISTANCE, angles, self.current_team)

                    
    
    def init_figures(self):

#                             'z''y''x'
        Pawn(self, self.board[1][3][0], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][1], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][2], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][3], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][4], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][5], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][6], settings.TEAM_WHITE)
        Pawn(self, self.board[1][3][7], settings.TEAM_WHITE)
        

        Pawn(self, self.board[6][3][0], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][1], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][2], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][3], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][4], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][5], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][6], settings.TEAM_BLACK)
        Pawn(self, self.board[6][3][7], settings.TEAM_BLACK)

        King(self, self.board[0][3][3], settings.TEAM_WHITE)
        Queen(self, self.board[0][3][4], settings.TEAM_WHITE)
        King(self, self.board[7][3][3], settings.TEAM_BLACK)
        Queen(self, self.board[7][3][4], settings.TEAM_BLACK)

        Bishop(self, self.board[0][3][2], settings.TEAM_WHITE)
        Bishop(self, self.board[0][3][5], settings.TEAM_WHITE)
        Bishop(self, self.board[7][3][2], settings.TEAM_BLACK)
        Bishop(self, self.board[7][3][5], settings.TEAM_BLACK)
        
        Knight(self, self.board[0][3][1], settings.TEAM_WHITE)
        Knight(self, self.board[0][3][6], settings.TEAM_WHITE)
        Knight(self, self.board[7][3][1], settings.TEAM_BLACK)
        Knight(self, self.board[7][3][6], settings.TEAM_BLACK)            

        Rook(self, self.board[0][3][0], settings.TEAM_WHITE)
        Rook(self, self.board[0][3][7], settings.TEAM_WHITE)
        
        Rook(self, self.board[7][3][0], settings.TEAM_BLACK)
        Rook(self, self.board[7][3][7], settings.TEAM_BLACK)
        
        # # Bishop Test
        # b = Bishop(self, self.board[3][3][3], settings.TEAM_WHITE)
        # space = 3
        # for x,y,z in b.movement_vector:
        #     Pawn(self, self.board[3+int(x*space)][3+int(y*space)][3+int(z*space)], settings.TEAM_BLACK)    
        
        # # Pawn Test
        # a = Pawn(self, self.board[1][3][3], settings.TEAM_WHITE)
        # b = Bishop(self, self.board[3][3][4], settings.TEAM_BLACK)
        # c = Bishop(self, self.board[3][3][2], settings.TEAM_BLACK)
        
       