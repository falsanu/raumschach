import pygame
import settings 
from utilities.matrix_helpers import project_3d_to_2d, rotate_point

class Ui():
    def __init__(self, board):
        print("UI Created")
        self.board = board
        self.small_font = pygame.font.SysFont("Arial", 10)
        self.label_font = pygame.font.SysFont("Impact", 20)
        self.points = []
        self.size = (settings.SIZE*1.1+settings.BOX_SPACING) * board.rows
        
        self.points.append(pygame.math.Vector3(-(self.size),-(self.size),-(self.size)))
        self.points.append(pygame.math.Vector3(-(self.size),(self.size),-(self.size)))
        self.points.append(pygame.math.Vector3((self.size),(self.size),-(self.size)))
        self.points.append(pygame.math.Vector3((self.size), -(self.size), -(self.size)))    

        self.points.append(pygame.math.Vector3(-(self.size), (self.size), (self.size)))
        self.points.append(pygame.math.Vector3((self.size), (self.size), (self.size)))
        self.points.append(pygame.math.Vector3((self.size), -(self.size), (self.size)))
        self.points.append(pygame.math.Vector3(-(self.size),-(self.size) ,(self.size)))

        self.edges = [
            (0, 1), (1, 2),  # Vorderseite
            (4, 5), (5, 6), (6, 7), # Rückseite
            (0, 7), (1, 4), (2, 5),    # Verbindungen
        ]
        self.fpsClock = pygame.time.Clock() #1
        
    def position_labels(self, screen, angles):
        active_x, active_y, active_z = self.board.active_box

        # Farbe basierend auf dem aktuellen Team setzen
        active_color = pygame.Color(0)
        if self.board.current_team == settings.TEAM_WHITE:
            active_color.hsla = (49, 100, 80)  # HSLA inkl. Alpha
        else:
            active_color.hsla = (298, 100, 80)  # HSLA inkl. Alpha

        active_color.a = 128
        default_color = pygame.Color(50, 50, 50)

        # Hilfsfunktion, um Beschriftungen zu zeichnen
        def draw_label(i, axis_position_func, axis_active_value, label_func):
            p = axis_position_func(i)
            rotated_point = rotate_point(p, angles)
            projected_point = project_3d_to_2d(rotated_point, screen.get_width(), screen.get_height(), settings.FOV, settings.DISTANCE)
            color = active_color if i == axis_active_value else default_color
            label_text = self.label_font.render(label_func(i), True, color)
            screen.blit(label_text, (projected_point.x, projected_point.y))

        # X-Ebene (A-H)
        def x_position(i):
            x = (i * ((settings.SIZE + settings.BOX_SPACING) * 2)) - self.size + settings.SIZE * 2
            y = self.size - (settings.SIZE * 0.9 + settings.BOX_SPACING)
            z = -self.size - (settings.SIZE * 0.9 + settings.BOX_SPACING)
            return pygame.math.Vector3(x, y, z)

        # Y- und Z-Ebene (1-8)
        def y_position(i):
            x = -self.size - (settings.SIZE * 0.9 + settings.BOX_SPACING)
            y = (self.size - (i * ((settings.SIZE + settings.BOX_SPACING) * 2))) - settings.SIZE * 2
            z = -self.size - (settings.SIZE * 0.9 + settings.BOX_SPACING)
            return pygame.math.Vector3(x, y, z)

        def z_position(i):
            x = -self.size - (settings.SIZE * 0.9 + settings.BOX_SPACING)
            y = self.size - (settings.SIZE * 0.9 + settings.BOX_SPACING)
            z = (i * ((settings.SIZE + settings.BOX_SPACING) * 2)) - self.size + settings.SIZE * 2
            return pygame.math.Vector3(x, y, z)

        # X-Ebene: A-H
        for i in range(self.board.rows):
            draw_label(i, x_position, active_x, lambda i: chr(65 + i))  # 65 = ASCII für 'A'

        # Y- und Z-Ebene: 1-8
        for i in range(self.board.rows):
            draw_label(i, y_position, active_y, lambda i: str(i + 1))
            draw_label(i, z_position, active_z, lambda i: str(i + 1))



    def draw(self, screen, angles):
        rotated_points = [rotate_point(p, angles) for p in self.points]
        projected_points = [
            project_3d_to_2d(p, screen.get_width(), screen.get_height(), settings.FOV, settings.DISTANCE)
            for p in rotated_points
        ]

        # Kanten zeichnen
        for start_idx, end_idx in self.edges:
            start = projected_points[start_idx]
            end = projected_points[end_idx]
            pygame.draw.line(screen, (50,50,50), (start.x, start.y), (end.x, end.y), 1)
                # pygame.gfxdraw.line(screen, int(start.x), int(start.y), int(end.x), int(end.y), self.color)

        self.position_labels(screen, angles)
        fps = int(self.fpsClock.get_fps())
        fps_text = self.small_font.render(f"FPS: {fps}, FOV: {settings.FOV}, DISTANCE: {settings.DISTANCE}, ROT_X:{int(angles[0])}, ROT_Y:{int(angles[1])}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))  # Oben links
        
        mouse_x,mouse_y = pygame.mouse.get_pos()
        mouse_text = self.small_font.render(f"Mouse_X: {mouse_x}, Mouse_Y: {mouse_y}", True, (255, 255, 255))
        screen.blit(mouse_text, (10, 30))  # Oben links
        
        if self.board.active_box != None:
            sel_box_x,sel_box_y,sel_box_z = self.board.active_box
            box_selection_text = self.small_font.render(f"Active Box: x: {int(sel_box_x)}, y: {int(sel_box_y)}, z:{int(sel_box_z)}", True, (255, 255, 255))
            screen.blit(box_selection_text, (10, 50))  # Oben links

        if self.board.selected_box:
            sel_box_x,sel_box_y,sel_box_z = self.board.selected_box.orig_vector
            box_selection_text = self.small_font.render(f"Selected Box: x: {int(sel_box_x)}, y: {int(sel_box_y)}, z:{int(sel_box_z)}", True, (255, 255, 255))
            screen.blit(box_selection_text, (10, 60))  # Oben links

        team_text = "WHITE" if self.board.current_team == settings.TEAM_WHITE else "BLACK"

        game_font = pygame.font.SysFont("Impact", 60)
        game_infos = game_font.render(f"{team_text}", True, (255, 255, 255))
        screen.blit(game_infos, (screen.get_width() - 350, 50))  # Oben rechts
        
        game_info_figure_font = pygame.font.SysFont("Impact", 40)
        game_info_figure = game_info_figure_font.render(f"{self.board.selected_box.figure.type if self.board.selected_box and self.board.selected_box.figure else ''}", True, (255, 255, 255))
        screen.blit(game_info_figure, (screen.get_width() - 350, 105))  # Oben rechts
            
        game_info_figure_font = pygame.font.SysFont("Arial", 12)
        game_credits = game_info_figure_font.render("Raumschach by @falsanu and @jonaspews", True, (255, 255, 255))
        screen.blit(game_credits, (30, screen.get_height() - 20))  # Oben rechts
        
        self.fpsClock.tick(60) 