import pygame
from settings import *
from abc import ABC, abstractmethod

class Figure(ABC):
    def __init__(self, board, box, team):
        self.board = board
        self.box = box
        self.box.figure = self
        self.team = team
        self.movement_vector = []
        self.hit_vector = []
        
    
    def get_color(self):
        if self.team == TEAM_WHITE:
            return (255,255,0)
        else:
            return (255,0,255)

    def highlight_box(self):
        if self.team == TEAM_WHITE:
            self.box.highlight((255,255,0))
        else:
            self.box.highlight((255,0,255))
    
    def un_highlight_box(self):
            self.box.highlight(self.box.initial_color)

    @abstractmethod
    def get_target_fields(self):
        pass

    def show_possible_target_fields(self):
        for x,y,z in self.get_target_fields():
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (z >= 0 and z < self.board.rows):
                if self.board.board[int(z)][int(y)][int(x)] != self.box:
                    self.board.board[int(z)][int(y)][int(x)].highlight((0,255,0))
    
    def hide_possible_target_fields(self):
        for x,y,z in self.get_target_fields():
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
    
    def __str__(self):
        return f"Figure(name={self.name}, type={self.type})"