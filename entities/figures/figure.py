import pygame

class Figure:
    def __init__(self, board, box):
        self.board:Board = board
        self.box = box
        self.box.figure = self
        self.movement_vector = []
        self.hit_vector = []
    

    def highlight_box(self):
        self.box.highlight((255,0,0))

    def show_possible_target_fields(self):
        for x,y,z in self.movement_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (z >= 0 and z < self.board.rows):
                if self.board.board[int(z)][int(y)][int(x)] != self.box:
                    self.board.board[int(z)][int(y)][int(x)].highlight((0,255,0))
    
    def hide_possible_target_fields(self):
        for x,y,z in self.movement_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (z >= 0 and z < self.board.rows):
                if self.board.board[int(z)][int(y)][int(x)] != self.box:
                    self.board.board[int(z)][int(y)][int(x)].un_highlight()
        self.highlight_box()
    

    def show_possible_hit_fields(self):
        for x,y,z in self.hit_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (z >= 0 and z < self.board.rows):
                if self.board.board[int(z)][int(y)][int(x)] != self.box:
                    self.board.board[int(z)][int(y)][int(x)].highlight((0,255,255))
            
    
    def hide_possible_hit_fields(self):
        for x,y,z in self.hit_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (z >= 0 and z < self.board.rows):
                if self.board.board[int(z)][int(y)][int(x)] != self.box:
                    self.board.board[int(z)][int(y)][int(x)].un_highlight()
        self.highlight_box()
            