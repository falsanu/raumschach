import pygame
from entities.box import Box
from entities.figures.pawn import Pawn
from entities.figures.king import King
from settings import *

class Board:
    def __init__(self, rows, level, columns):
        self.rows = rows
        self.level = level
        self.columns = columns

        self.active_box = pygame.math.Vector3(0,0,0)
        self.selected_box:Box = None 
        

        self.board = [[[None for _ in range(self.rows)]
             for _ in range(self.level)]
            for _ in range(self.columns)]
        
        # Mittelpunkt des Boards berechnen
        center_x = (self.columns - 1) / 2  # Mitte der Spalten (X-Achse)
        center_y = (self.level - 1) / 2  # Mitte der Ebenen (Y-Achse)
        center_z = (self.rows - 1) / 2   # Mitte der Reihen (Z-Achse)
        self.center = (center_x, center_y, center_z)

        # Befüllen des Boards mit Box-Objekten
        for z in range(self.rows):
            for y in range(self.level):
                for x in range(self.columns):
                    color = pygame.Color(0)  # Erstelle ein Color-Objekt (Farbe ist zunächst irrelevant)
                    color.hsva = ((y * 360 // self.level) % 360, 100, 40, 50)  # Setze HSV-Werte (Hue, Saturation, Value, Alpha)
                    
                    # Box Offset relativ zum Mittelpunkt (da über die Mitte rotiert wird)
                    offset_x = (x - center_x) * (SIZE + BOX_SPACING)/SIZE
                    offset_y = (y - center_y) * ((SIZE + BOX_SPACING)/SIZE) * (SIZE + Y_SPACING)/SIZE
                    offset_z = (z - center_z) * (SIZE + BOX_SPACING)/SIZE
                    
                    # Box platzieren
                    self.board[z][y][x] = Box(offset_x, offset_y, offset_z, SIZE, color, pygame.math.Vector3(x,y,z))
        
        self.init_figures()
    
    def set_selected_box(self, box:pygame.math.Vector3):
        x,y,z = box

        if self.selected_box != None:
            if self.selected_box.figure != None:
                self.selected_box.figure.hide_possible_target_fields()
                self.selected_box.figure.hide_possible_hit_fields()
            # self.selected_box.un_highlight()


        self.selected_box:Box = self.board[int(z)][int(y)][int(x)]
        if self.selected_box.figure != None:
            # self.selected_box.highlight((0,0,255))
            self.selected_box.figure.show_possible_target_fields()
            self.selected_box.figure.show_possible_hit_fields()
    
    def draw(self, screen, angles):
        # Befüllen mit Box-Objekten
        for z in range(self.rows):
            for y in range(self.level):
                for x in range(self.columns):

                    box = self.board[z][y][x]
                    box.is_active = False

                    if self.active_box.x == x and self.active_box.y == y and self.active_box.z == z:
                        box.is_active = True
                    box.draw(screen, FOV, DISTANCE, angles)
    
    def init_figures(self):
        pawn = Pawn(self.board, self.board[1][4][4])
        
        #pawn.show_possible_hit_fields()

        king = King(self.board, self.board[3][3][3])
        #king.show_possible_target_fields()
        #king.show_possible_hit_fields()
                    
