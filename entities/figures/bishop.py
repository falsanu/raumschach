from entities.figures.figure import Figure
from entities.box import Box
import pygame.math

class Bishop(Figure):
    def __init__(self, board, box:Box, team):
        super().__init__(board, box, team)
        self.type = "Bishop"
        self.label = "B"

        # Basis movement
        self.movement_vector = [
            # Diagonalen in alle 8 3D-Richtungen (jeweils ±1 in x, y, z)
            pygame.math.Vector3(1, 1, 1),    # rechts-hoch-vorne
            pygame.math.Vector3(1, 1, -1),   # rechts-hoch-hinten
            pygame.math.Vector3(1, -1, 1),   # rechts-runter-vorne
            pygame.math.Vector3(1, -1, -1),  # rechts-runter-hinten

            pygame.math.Vector3(-1, 1, 1),   # links-hoch-vorne
            pygame.math.Vector3(-1, 1, -1),  # links-hoch-hinten
            pygame.math.Vector3(-1, -1, 1),  # links-runter-vorne
            pygame.math.Vector3(-1, -1, -1), # links-runter-hinten

            pygame.math.Vector3(-1, 0, 1),     # in Ebene links vorn
            pygame.math.Vector3(1, 0, 1),      # in Ebene rechts vorn
            pygame.math.Vector3(-1, 0, -1),    # in Ebene links hinten
            pygame.math.Vector3(1, 0, -1),      # in Ebene rechts hinten

            pygame.math.Vector3(-1, 1, 0),     # in Ebene links vorn
            pygame.math.Vector3(1, 1, 0),     # in Ebene links vorn
            pygame.math.Vector3(0, 1, 1),     # in Ebene links vorn
            pygame.math.Vector3(0, 1, -1),     # in Ebene links vorn

            pygame.math.Vector3(-1, -1, 0),     # in Ebene links vorn
            pygame.math.Vector3(1, -1, 0),     # in Ebene links vorn
            pygame.math.Vector3(0, -1, 1),     # in Ebene links vorn
            pygame.math.Vector3(0, -1, -1),     # in Ebene links vorn

        ]

    
        self.hit_vector = []
        
        self.highlight_box()
    
    def get_target_fields(self):
            # calculate the movement_vectors by returning all vectors until end
            # of board or a figure is in line
            
            target_fields = []
            self.hit_vector = []

            for v in self.movement_vector:

                for i in range(1, self.board.columns):  # i nimmt die Werte 1, 2, 3 an
                    new_vector = v*i
                    x,y,z = new_vector + self.box.orig_vector 
                    # sicherstellen, dass x,y und z innerhalb des Feldes liegen
                    if (x>=0 and x < self.board.columns) and (y>=0 and y<self.board.level) and (z>=0 and z<self.board.rows):
                        box_to_check = self.board.board[int(z)][int(y)][int(x)]
                        if box_to_check == self.box:
                                break
                        if box_to_check.figure == None:
                            target_fields.append(new_vector)
                        else:
                            # wenn die figur von dem anderen Team ist kann sie geschlagen werden
                            if self.team != box_to_check.figure.team:
                                    self.hit_vector.append(pygame.math.Vector3(int(new_vector.x),int(new_vector.y),int(new_vector.z)))
                            break
            return target_fields + self.hit_vector
