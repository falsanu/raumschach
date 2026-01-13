
import pygame
import math


# Local imports
import settings

class InputHandler:
    def __init__(self, board, angles, ui):
        self.board = board
        self.angles = angles
        self.ui = ui
        self.mousedown = False
        self.shift_pressed = False
        self.opposite_view = False
        self.dragging = False

        self.shift_pressed = False
        self.last_mouse_pos = None

    def mouse_rotation(self):
        print("mouse rotation")

    def mouse_wheel(self, event):
        if self.shift_pressed:
            settings.FOV += event.y
        else:
            settings.DISTANCE+=event.y*10

    def mouse_motion(self, mouse_pos):
        if self.mousedown and not self.dragging:
            if abs(mouse_pos[0] - self.last_mouse_pos[0]) > 5 or abs(mouse_pos[1] - self.last_mouse_pos[1]) > 5:
                self.dragging = True

    def mouse_button_down(self):
        self.mousedown = True
        self.last_mouse_pos = pygame.mouse.get_pos()  # Startposition speichern
        self.dragging = False  # Flag für Drag-Vorgang

    def mouse_button_up(self):
        self.mousedown = False
        current_mouse_pos = pygame.mouse.get_pos()

        # Prüfe, ob sich die Maus bewegt hat (Drag)
        if self.last_mouse_pos and (
            abs(current_mouse_pos[0] - self.last_mouse_pos[0]) > 5 or  # Schwellenwert für Bewegung
            abs(current_mouse_pos[1] - self.last_mouse_pos[1]) > 5
        ):
            self.dragging = True

        self.last_mouse_pos = None

        # Nur auslösen, wenn kein Drag stattfand
        if not self.dragging:
            self.get_box_under_cursor()


    def key_down(self, event):
        
        if event.key == pygame.K_LSHIFT:
            self.shift_pressed = True

    def key_up(self, event):
        if event.key == pygame.K_LSHIFT:
            self.shift_pressed = False


        if event.key == pygame.K_TAB:
            print("Key down Tab")
            # toggle views    
            self.opposite_view = not self.opposite_view

            if not self.opposite_view:
                self.angles[1]  =    math.radians(45)  # Y-Achse: 45° gedreht
            else:
                self.angles[1]  =    math.radians(225)  # Y-Achse: 225° gedreht
            

        if event.key == pygame.K_1:
            self.angles[1]  =        math.radians(0)  # Y-Achse: 0°° gedreht
        if event.key == pygame.K_2:
            self.angles[1]  =        math.radians(90)  # Y-Achse: 90° gedreht
        if event.key == pygame.K_3:
            self.angles[1]  =        math.radians(180)  # Y-Achse: 180° gedreht
        if event.key == pygame.K_4:
            self.angles[1]  =        math.radians(270)  # Y-Achse: 270° gedreht
        if event.key == pygame.K_ESCAPE:
            self.board.unselect_box()
        

        if event.key == pygame.K_d:
            if self.opposite_view == True:
                x,y,z = self.board.active_box
                x-=1
                if x < 0:
                    x = self.board.columns - 1
                self.board.active_box.x = x
            else:
                x,y,z = self.board.active_box
                x+=1
                if x > self.board.columns -1:
                    x = 0
                
                self.board.active_box.x = x
            
        if event.key == pygame.K_a:
            if self.opposite_view == True:
                x,y,z = self.board.active_box
                x+=1
                if x > self.board.columns -1:
                    x = 0
                
                self.board.active_box.x = x            
            else:
                x,y,z = self.board.active_box
                x-=1
                if x < 0:
                    x = self.board.columns - 1
                self.board.active_box.x = x

        if event.key == pygame.K_s:
            if self.opposite_view == True:
                x,y,z = self.board.active_box
                z+=1
                if z > self.board.rows - 1:
                    z = 0
                self.board.active_box.z = z
            else:

                x,y,z = self.board.active_box
                z-=1
                if z < 0:
                    z = self.board.rows - 1
                self.board.active_box.z = z

        if event.key == pygame.K_w:
            if self.opposite_view == True:
                x,y,z = self.board.active_box
                z-=1
                if z < 0:
                    z = self.board.rows - 1
                self.board.active_box.z = z
            else:
                x,y,z = self.board.active_box
                z+=1
                if z > self.board.rows - 1:
                    z = 0
                self.board.active_box.z = z
        
        if event.key == pygame.K_e:
            x,y,z = self.board.active_box
            y+=1
            if y > self.board.level - 1:
                y = 0
            self.board.active_box.y = y
        
        if event.key == pygame.K_v:
            print("v pressed")
            if self.board.no_visibility == True:
                self.board.no_visibility = False
            else:
                self.board.no_visibility = True

        if event.key == pygame.K_q:
            x,y,z = self.board.active_box
            y-=1
            if y < 0:
                y = self.board.level -1
            self.board.active_box.y = y
        if event.key == pygame.K_SPACE:
            self.board.set_selected_box(self.board.active_box)

    def update(self):
        if self.mousedown and self.last_mouse_pos is not None:
            current_mouse_pos = pygame.mouse.get_pos()
            delta_x = current_mouse_pos[0] - self.last_mouse_pos[0]
            self.angles[1] += math.radians(delta_x * -0.3)  # Flüssige Rotation basierend auf Mausbewegung
            self.last_mouse_pos = current_mouse_pos  # Aktuelle Position speichern
        
        box = self.board.get_box_under_mouse(
            pygame.mouse.get_pos(),
            self.angles
        )
        if box:
            self.board.active_box = box.orig_vector


    def handle_mouse_click(self, mouse_pos):
        box = self.board.get_box_under_mouse(
            mouse_pos,
            self.angles
        )
        print(box)
        if box:
            self.board.set_selected_box(box.orig_vector)
            if box.figure:
                print(f"Box mit Figur ausgewählt: {box.figure.type}")
            else:
                print("Leere Box ausgewählt.")

    def get_box_under_cursor(self):
        # print(pygame.mouse.get_pos())
        self.handle_mouse_click(pygame.mouse.get_pos())

