from entities.figures.figure import Figure
import pygame.math

class Bishop(Figure):
    def __init__(self, board, box):
        super().__init__(board, box)
        self.type = "Bishop"
        self.movement_vector = [
                                
                            ]
    
        self.hit_vector = [
        
                            ]
        self.label = "B"
        self.highlight_box()
    
   