from entities.figures.figure import Figure
import pygame.math

class Pawn(Figure):
    def __init__(self, board, box):
        super().__init__(board, box)
        self.movement_vector = [
                                pygame.math.Vector3(0, 1, 0),   # Bewegung eins hoch
                                pygame.math.Vector3(0, 2, 0),   # Bewegung zwei hoch
                                pygame.math.Vector3(0, -1, 0),  # Bewegung eins runter
                                pygame.math.Vector3(0, -2, 0),  # Bewegung zwei runter
                                pygame.math.Vector3(0, 0, 1),   # Bewegung eins vor
                                pygame.math.Vector3(0, 0, 2),   # Bewegung zwei vor
                            ]
    
        self.hit_vector = [
                                pygame.math.Vector3(-1, 0, 1),  # Schlagen eins vor, eins link
                                pygame.math.Vector3(1, 0, 1),   # Schlagen eins vor, eins rechts
                                pygame.math.Vector3(0, 1, 1),   # Schlagen eins hoch, eins vor
                                pygame.math.Vector3(0, -1, 1),  # Schlagen eins runter, eins vor
                                pygame.math.Vector3(-1, 1, 1),  # Schlagen eins hoch, eins links
                                pygame.math.Vector3(1, 1, 1),   # Schlagen eins hoch, eins recht
                                pygame.math.Vector3(-1, -1, 1), # Schlagen eins runter, eins links
                                pygame.math.Vector3(1, -1, 1),  # Schlagen eins runter, eins rechts

                            ]
        

        self.label = "P"
        self.highlight_box()
    
    def highlight_box(self):
        self.box.highlight((255,0,0))

    def show_possible_target_fields(self):
        for x,y,z in self.movement_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if self.board[int(z)][int(y)][int(x)] != self.box:
                self.board[int(z)][int(y)][int(x)].highlight((0,255,0))
    def show_possible_hit_fields(self):
        for x,y,z in self.hit_vector:
            x,y,z = pygame.math.Vector3(x,y,z) + self.box.orig_vector
            if self.board[int(z)][int(y)][int(x)] != self.box:
                self.board[int(z)][int(y)][int(x)].highlight((0,255,255))
            
