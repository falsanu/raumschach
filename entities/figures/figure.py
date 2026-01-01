import pygame
 

class Figure:
    def __init__(self, board, box):
        self.board = board
        self.box = box
        self.box.figure = self
        self.movement_vector = []
        self.hit_vector = []
    

    def highlight_box(self):
        self.box.highlight((255,0,0))

    def show_possible_target_fields(self):
        for x,y,z in self.movement_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if self.board[int(z)][int(y)][int(x)] != self.box:
                self.board[int(z)][int(y)][int(x)].highlight((0,255,0))
    
    def hide_possible_target_fields(self):
        for x,y,z in self.movement_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if self.board[int(z)][int(y)][int(x)] != self.box:
                self.board[int(z)][int(y)][int(x)].un_highlight()
        self.highlight_box()
    

    def show_possible_hit_fields(self):
        for x,y,z in self.hit_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if self.board[int(z)][int(y)][int(x)] != self.box:
                self.board[int(z)][int(y)][int(x)].highlight((0,255,255))
            
    
    def hide_possible_hit_fields(self):
        for x,y,z in self.hit_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if self.board[int(z)][int(y)][int(x)] != self.box:
                self.board[int(z)][int(y)][int(x)].un_highlight()
        self.highlight_box()
            