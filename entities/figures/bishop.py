from entities.figures.figure import Figure
import pygame.math

class Bishop(Figure):
    def __init__(self, board, box, team):
        super().__init__(board, box, team)
        self.type = "Bishop"

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

    
        self.hit_vector = [
        
                            ]
        self.label = "B"
        self.highlight_box()
    
    def get_target_fields(self):
            # calculate the movement_vectors by returning all vectors until end
            # of board or a figure is in line

            
            #

            return self.movement_vector