from entities.figures.figure import Figure
import pygame.math

class King(Figure):
    def __init__(self, board, box, team):
        super().__init__(board, box, team)
        self.type = "King"
        self.movement_vector = []
    
        self.hit_vector = [
                            # Bewegung in den Hauptachsen (x, y, z)
                            pygame.math.Vector3(1, 0, 0),   # rechts
                            pygame.math.Vector3(-1, 0, 0),  # links
                            pygame.math.Vector3(0, 1, 0),   # hoch
                            pygame.math.Vector3(0, -1, 0),  # runter
                            pygame.math.Vector3(0, 0, 1),   # vorwärts
                            pygame.math.Vector3(0, 0, -1),  # rückwärts

                            # Diagonale Bewegungen in der Ebene (x-z, x-y, y-z)
                            pygame.math.Vector3(1, 0, 1),   # rechts-vorne
                            pygame.math.Vector3(1, 0, -1),  # rechts-hinten
                            pygame.math.Vector3(-1, 0, 1),  # links-vorne
                            pygame.math.Vector3(-1, 0, -1), # links-hinten
                            pygame.math.Vector3(0, 1, 1),   # hoch-vorne
                            pygame.math.Vector3(0, 1, -1),  # hoch-hinten
                            pygame.math.Vector3(0, -1, 1),  # runter-vorne
                            pygame.math.Vector3(0, -1, -1), # runter-hinten
                            pygame.math.Vector3(1, 1, 0),   # rechts-hoch
                            pygame.math.Vector3(1, -1, 0),  # rechts-runter
                            pygame.math.Vector3(-1, 1, 0),  # links-hoch
                            pygame.math.Vector3(-1, -1, 0), # links-runter

                            # Volle 3D-Diagonalen (x, y, z)
                            pygame.math.Vector3(1, 1, 1),   # rechts-hoch-vorne
                            pygame.math.Vector3(1, 1, -1),  # rechts-hoch-hinten
                            pygame.math.Vector3(1, -1, 1),  # rechts-runter-vorne
                            pygame.math.Vector3(1, -1, -1), # rechts-runter-hinten
                            pygame.math.Vector3(-1, 1, 1),  # links-hoch-vorne
                            pygame.math.Vector3(-1, 1, -1), # links-hoch-hinten
                            pygame.math.Vector3(-1, -1, 1), # links-runter-vorne
                            pygame.math.Vector3(-1, -1, -1)# links-runter-hinten
                            ]
        
        self.label = "K"
        self.highlight_box()

        
    def get_target_fields(self):
            return self.hit_vector