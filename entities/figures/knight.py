# knight

from entities.figures.figure import Figure
import pygame.math

class Knight(Figure):
    def __init__(self, board, box, team):
        super().__init__(board, box, team)
        self.type = "Knight"
        self.movement_vector = []  # leer, da Bewegungsvektoren = Angriffsvektoren
    
        self.hit_vector = [
                                  #(links(-)/rechts(+),oben(+)/unten(-),vor(+)/zurück(-))
                                #vorwärts zwei
                                pygame.math.Vector3(0, 1, 2),  # Bewegung eins hoch, zwei vor 
                                pygame.math.Vector3(0, -1, 2),  # Bewegung eins runter, zwei vor
                                pygame.math.Vector3(1,0,2),  # Bewegung eins rechts, zwei vor
                                pygame.math.Vector3(-1,0,2),  # Bewegung eins links, zwei vor
                                #rückwärts zwei
                                pygame.math.Vector3(0, 1, -2),  # Bewegung eins hoch, zwei zurück 
                                pygame.math.Vector3(0, -1, -2),  # Bewegung eins runter, zwei zurück
                                pygame.math.Vector3(1,0,-2),  # Bewegung eins rechts, zwei zurück
                                pygame.math.Vector3(-1,0,-2),  # Bewegung eins links, zwei  zurück
                                #hoch zwei
                                pygame.math.Vector3(0,2,1),  # Bewegung zwei hoch, eins vor
                                pygame.math.Vector3(0,2,-1),  # Bewegung zwei hoch, eins zurück
                                pygame.math.Vector3(1,2,0),  # Bewegung zwei hoch, eins rechts
                                pygame.math.Vector3(-1,2,0),  # Bewegung zwei hoch, eins links
                                #runter zwei
                                pygame.math.Vector3(0,-2,1),  # Bewegung zwei runter, eins vor
                                pygame.math.Vector3(0,-2,-1),  # Bewegung zwei runter, eins zurück
                                pygame.math.Vector3(1,-2,0),  # Bewegung zwei runter, eins rechts
                                pygame.math.Vector3(-1,-2,0),  # Bewegung zwei runter, eins links
                                #linke zwei
                                pygame.math.Vector3(-2,0,1),  # Bewegung links zwei, eins vor
                                pygame.math.Vector3(-2,0,-1),  # Bewegung links zwei, eins zurück
                                pygame.math.Vector3(-2,1,0),  # Bewegung links zwei, eins hoch
                                pygame.math.Vector3(-2,-1,0),  # Bewegung links zwei, eins runter
                                #rechts zwei
                                pygame.math.Vector3(2,0,1),  # Bewegung links zwei, eins vor
                                pygame.math.Vector3(2,0,-1),  # Bewegung links zwei, eins zurück
                                pygame.math.Vector3(2,1,0),  # Bewegung links zwei, eins hoch
                                pygame.math.Vector3(2,-1,0),  # Bewegung links zwei, eins runter                                
                            
                            ]
        self.label = "K"
        self.highlight_box()
    
    def get_target_fields(self):
            return self.hit_vector
    