from settings import *
from entities.figures.figure import Figure
import pygame.math

class Pawn(Figure):
    def __init__(self, board, box, team):
        super().__init__(board, box, team)
        self.type = "Pawn"



        self.movement_vector = [
                                pygame.math.Vector3(0, 1, 0),   # Bewegung eins hoch
                                pygame.math.Vector3(0, 2, 0),   # Bewegung zwei hoch
                                pygame.math.Vector3(0, -1, 0),  # Bewegung eins runter
                                pygame.math.Vector3(0, -2, 0),  # Bewegung zwei runter
                            ]
        
        if self.team == TEAM_WHITE:
                                self.movement_vector.append(pygame.math.Vector3(0, 0, 1))   # Bewegung eins vor
                                self.movement_vector.append(pygame.math.Vector3(0, 0, 2))    # Bewegung zwei vor

        if self.team == TEAM_BLACK:
                                self.movement_vector.append(pygame.math.Vector3(0, 0, -1))   # Bewegung eins vor
                                self.movement_vector.append(pygame.math.Vector3(0, 0, -2))    # Bewegung zwei vor
            

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
        if self.team == TEAM_BLACK:
            for v in self.hit_vector:
                v.z *= -1
        

        self.label = "P"
        self.highlight_box()
    
    def get_target_fields(self):
            self.movement_vector = [
                pygame.math.Vector3(0, 1, 0),   # Bewegung eins hoch
                pygame.math.Vector3(0, -1, 0),  # Bewegung eins runter
            ]
            if not self.has_moved:
                self.movement_vector.append(pygame.math.Vector3(0, 2, 0))   # Bewegung zwei hoch
                self.movement_vector.append(pygame.math.Vector3(0, -2, 0))  # Bewegung zwei runter

        
            if self.team == TEAM_WHITE:
                self.movement_vector.append(pygame.math.Vector3(0, 0, 1))   # Bewegung eins vor
                if not self.has_moved:
                    self.movement_vector.append(pygame.math.Vector3(0, 0, 2))    # Bewegung zwei vor

            if self.team == TEAM_BLACK:
                self.movement_vector.append(pygame.math.Vector3(0, 0, -1))   # Bewegung eins vor
                if not self.has_moved:
                    self.movement_vector.append(pygame.math.Vector3(0, 0, -2))    # Bewegung zwei vor




            target_fields = []
            hit_vectors = []

            for v in self.movement_vector:
                new_vector = v
                x, y, z = new_vector + self.box.orig_vector
                # sicherstellen, dass x,y und z innerhalb des Feldes liegen
                if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (
                        z >= 0 and z < self.board.rows):
                    box_to_check = self.board.board[int(z)][int(y)][int(x)]
                    if box_to_check == self.box:
                        break
                    if box_to_check.figure == None:
                        target_fields.append(new_vector)

            for v in self.hit_vector:
                    new_vector = v
                    x, y, z = new_vector + self.box.orig_vector
                    # sicherstellen, dass x,y und z innerhalb des Feldes liegen
                    if (x >= 0 and x < self.board.columns) and (y >= 0 and y < self.board.level) and (
                            z >= 0 and z < self.board.rows):
                        box_to_check = self.board.board[int(z)][int(y)][int(x)]
                        if box_to_check == self.box:
                            break
                        if box_to_check.figure != None:
                            # wenn die figur von dem anderen Team ist kann sie geschlagen werden
                            if self.team != box_to_check.figure.team:
                                hit_vectors.append(
                                    pygame.math.Vector3(int(new_vector.x), int(new_vector.y), int(new_vector.z)))
                            break
            return target_fields + hit_vectors

