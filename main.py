import pygame
import sys
import math

# Initialize Pygame and Font Engine
pygame.init()
pygame.font.init()

# Setup True Fullscreen Mode based on monitor native resolution
info_object = pygame.display.get_desktop_sizes()[0]
WIDTH, HEIGHT = info_object[0], info_object[1]
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("The TurTech - Challenge X Presentation Demo")
clock = pygame.time.Clock()

# Color Palette
COLOR_BG_DARK = (30, 34, 42)
COLOR_BG_LIGHT = (255, 255, 255)
COLOR_TEXT_DARK = (40, 45, 55)
COLOR_TEXT_LIGHT = (240, 240, 240)
COLOR_TEXT_MUTED = (140, 150, 165)
COLOR_ACCENT = (76, 175, 80)
COLOR_ACCENT_HOVER = (96, 215, 100)
COLOR_PANEL = (44, 50, 60)
COLOR_ROBOT_BODY = (120, 130, 140)
COLOR_ROBOT_WHEEL = (20, 20, 20)
COLOR_ANTENNA = (200, 150, 40)
COLOR_DIRT = (120, 85, 60)
COLOR_GRASS = (55, 115, 65)
COLOR_TURTLE = (70, 90, 60)

# Global Typography Layouts
FONT_TITLE = pygame.font.SysFont("Arial", 42, bold=True)
FONT_SUBTITLE = pygame.font.SysFont("Arial", 26, bold=True)
FONT_BODY = pygame.font.SysFont("Arial", 18)
FONT_UI = pygame.font.SysFont("Arial", 20, bold=True)

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

        # Cinema Outro variables
        self.outro_timer = 0
        self.outro_alpha = 0
        self.typewriter_chars = 0


    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_ACCENT_HOVER if self.rect.collidepoint(mouse_pos) else COLOR_ACCENT
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        txt_surf = FONT_UI.render(self.text, True, (255, 255, 255))
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Component Structs for Assembly Stage
# Fixed flat array lists allowing smooth linear interpolation movement
COMPONENTS = [
    {"type": "PI", "name": "Raspberry Pi 5 Computer", "desc": "Handles core Fast Fourier Transforms (FFT) and algorithmic tracking logic.", "target_pos_x": WIDTH//2 - 60, "target_pos_y": HEIGHT//2 - 60, "color": (20, 140, 80)},
    {"type": "VCO", "name": "VCO Signal Sweep Generator", "desc": "Drives continuous RF frequency sweeps from 300 MHz to 1 GHz.", "target_pos_x": WIDTH//2 - 70, "target_pos_y": HEIGHT//2 + 30, "color": (30, 100, 200)},
    {"type": "ANTENNA", "name": "Dual Antipodal Vivaldi Antennas", "desc": "Custom copper-foil arrays engineered to skim 1-2 inches above soil surfaces.", "target_pos_x": WIDTH//2 + 40, "target_pos_y": HEIGHT//2 + 60, "color": (210, 140, 20)},
    {"type": "LTE", "name": "SIM7600G-H 4G LTE Module", "desc": "Integrated standalone wireless network interface using Twilio automated APIs.", "target_pos_x": WIDTH//2 + 30, "target_pos_y": HEIGHT//2 - 50, "color": (160, 40, 40)},
    {"type": "BOX", "name": "IP65 Weatherproof Enclosure", "desc": "Sealed outer polycarbonate chassis shield blocking destructive construction dust.", "target_pos_x": WIDTH//2, "target_pos_y": HEIGHT//2, "color": (180, 185, 190)}
]

class ApplicationState:
    def __init__(self):
        self.current_scene = "INTRO"
        self.buttons = []
        
        # Assembly Animation variables
        self.assembly_index = 0
        self.assembly_timer = 0
        self.comp_x, self.comp_y = 260, HEIGHT // 2 + 50
        self.comp_scale = 1.2
        self.assembly_complete = False

        # Simulation Testing variables
        self.sim_step = "APPROACH"  # APPROACH, AVOID, SCANNING_T1, PROFILE_T1, TRACK_T2, SCANNING_T2, PROFILE_T2, COMPLETE
        self.sim_timer = 0
        self.robot_x = -150
        self.robot_y = HEIGHT // 2 - 50
        self.phone_alert_active = False
        self.phone_alert_msg = ""
        self.view_mode = "TOP"
        self.scan_progress = 0
        
        # Cinema Outro variables
        self.outro_timer = 0
        self.outro_alpha = 0

        # Simulation playback state controller switches
        self.outro_timer = 0
        self.outro_alpha = 0
        self.typewriter_chars = 0
        self.is_paused = False

    def start_building(self):
        self.current_scene = "ASSEMBLY"
        self.buttons = []
        self.assembly_index = 0
        self.assembly_timer = 0

    def start_testing(self):
        self.current_scene = "TESTING"
        self.buttons = []
        self.sim_step = "APPROACH"
        self.sim_timer = 0
        self.robot_x = -100
        self.robot_y = HEIGHT // 2 - 50
        self.view_mode = "TOP"
        self.phone_alert_active = False

    def trigger_outro(self):
        self.current_scene = "OUTRO"
        self.outro_timer = 0
        self.buttons = []

    def update(self):
        # 🛑 INSTANT FREEZE EXIT FILTER: If spacebar pause toggle flag is active, skip all math calculations this frame
        if self.is_paused:
            return
        if self.current_scene == "ASSEMBLY":
            if self.assembly_index < len(COMPONENTS):
                self.assembly_timer += 1
                if self.assembly_timer < 390:  # ~6.5 seconds reading window per element
                    self.comp_scale = 1.2 + math.sin(self.assembly_timer * 0.05) * 0.1
                    self.comp_x = 240
                    self.comp_y = 480
                elif self.assembly_timer < 450:  # Animate component into layout frame position
                    t = (self.assembly_timer - 390) / 60.0
                    target_x = COMPONENTS[self.assembly_index]["target_pos_x"]
                    target_y = COMPONENTS[self.assembly_index]["target_pos_y"]
                    self.comp_x = 240 + (target_x - 240) * t
                    self.comp_y = 480 + (target_y - 480) * t

                else:
                    self.assembly_index += 1
                    self.assembly_timer = 0
            elif not self.assembly_complete:
                self.assembly_complete = True
                # Dynamically placed in the center white space above the footer glossary
                self.buttons = [Button(WIDTH // 2 - 120, HEIGHT // 2 + 200, 240, 60, "Start Testing", self.start_testing)]

        elif self.current_scene == "TESTING":
            self.sim_timer += 1
            
            if self.sim_step == "APPROACH":
                self.robot_x += 3.0
                self.robot_y += math.sin(self.sim_timer * 0.05) * 1.5
                if self.robot_x >= WIDTH * 0.25:
                    self.sim_step = "AVOID"
                    self.sim_timer = 0
                    
            elif self.sim_step == "AVOID":
                # Dip down first to clear the side edge of the rock boulder
                if self.sim_timer < 60:
                    self.robot_y += 3.5  
                    self.robot_x += 2.5
                # Having cleared the rock edge, start steering back up toward the higher target plane
                elif self.sim_timer < 120:
                    self.robot_y -= 4.0  # Increased pull up to regain vertical height quickly
                    self.robot_x += 2.5
                else:
                    self.sim_step = "SCANNING_T1"
                    self.sim_timer = 0
                    
            elif self.sim_step == "SCANNING_T1":
                self.robot_x += 2.0
                
                # Active Path Tracking: Guide the robot's Y directly toward Turtle #1's target coordinate
                target_t1_y = HEIGHT // 2 - 25
                if self.robot_y > target_t1_y:
                    self.robot_y -= 1.5  # Steer upward to meet the turtle's line
                elif self.robot_y < target_t1_y:
                    self.robot_y += 1.5
                    
                if self.robot_x >= WIDTH * 0.50 - 40:
                    self.sim_step = "PROFILE_T1"
                    self.view_mode = "SIDE"
                    self.sim_timer = 0
                    self.phone_alert_active = False
                    
            elif self.sim_step == "PROFILE_T1":
                if self.sim_timer < 300:  # ~5 seconds display reading time
                    self.scan_progress = min(100, (self.sim_timer / 150.0) * 100)
                    if self.sim_timer == 60:
                        self.phone_alert_active = True
                        self.phone_alert_msg = "Target #1 Flagged!"
                else:
                    self.view_mode = "TOP"
                    self.sim_step = "TRACK_T2"
                    self.sim_timer = 0
                    self.phone_alert_active = False
                    
            elif self.sim_step == "TRACK_T2":
                self.robot_x += 2.5
                self.robot_y += 1.2 + math.sin(self.sim_timer * 0.05) * 1.5
                if self.robot_x >= WIDTH * 0.75 - 40:
                    self.sim_step = "SCANNING_T2"
                    self.sim_timer = 0
                    
            elif self.sim_step == "SCANNING_T2":
                self.robot_x += 1.5
                if self.robot_x >= WIDTH * 0.78:
                    self.sim_step = "PROFILE_T2"
                    self.view_mode = "SIDE"
                    self.sim_timer = 0
                    
            elif self.sim_step == "PROFILE_T2":
                if self.sim_timer < 300:  # ~5 seconds display reading time
                    self.scan_progress = min(100, (self.sim_timer / 150.0) * 100)
                    if self.sim_timer == 60:
                        self.phone_alert_active = True
                        self.phone_alert_msg = "Target #2 Flagged!"
                else:
                    self.view_mode = "TOP"
                    self.sim_step = "COMPLETE"
                    self.sim_timer = 0
                    self.phone_alert_active = False
                    
            elif self.sim_step == "COMPLETE":
                self.robot_x += 4.0
                if self.robot_x > WIDTH + 150:
                    self.trigger_outro()

        elif self.current_scene == "OUTRO":
            self.outro_timer += 1
            
            if hasattr(self, 'typewriter_chars'):
                self.typewriter_chars += 1
            else:
                self.typewriter_chars = 1
            
            if self.outro_timer < 300:
                self.outro_alpha = min(255, self.outro_timer * 4)
            elif self.outro_timer > 1000:  # ⚠️ We will increase this frame threshold limit
                self.current_scene = "BLACKOUT"

    def draw_detailed_component(self, surface, comp_type, x, y, scale):
        if comp_type == "PI":
            w, h = int(140 * scale), int(100 * scale)
            rect = pygame.Rect(x - w//2, y - h//2, w, h)
            pygame.draw.rect(surface, (23, 112, 65), rect, border_radius=int(6 * scale))
            usb_w, usb_h = int(30 * scale), int(40 * scale)
            pygame.draw.rect(surface, (180, 180, 185), (rect.right - usb_w, rect.top + int(15 * scale), usb_w, usb_h), border_radius=2)
            chip_size = int(34 * scale)
            pygame.draw.rect(surface, (20, 20, 20), (rect.left + int(35 * scale), rect.top + int(30 * scale), chip_size, chip_size), border_radius=3)
            pygame.draw.rect(surface, (200, 200, 200), (rect.left + int(20 * scale), rect.bottom - int(6 * scale), int(15 * scale), int(6 * scale)))
        elif comp_type == "ANTENNA":
            w, h = int(150 * scale), int(90 * scale)
            rect = pygame.Rect(x - w//2, y - h//2, w, h)
            pygame.draw.rect(surface, (50, 40, 30), rect, border_radius=int(4 * scale))
            points_top, points_bot = [], []
            steps = 20
            for i in range(steps + 1):
                px = rect.left + (w * i // steps)
                factor = (i / steps) ** 2.5
                offset = int((h // 2 - 2) * factor)
                points_top.append((px, y - offset))
                points_bot.append((px, y + offset))
            for i in range(steps):
                pygame.draw.line(surface, (215, 145, 30), points_top[i], points_top[i+1], width=int(3*scale))
                pygame.draw.line(surface, (215, 145, 30), points_bot[i], points_bot[i+1], width=int(3*scale))

        elif comp_type == "LTE":
            w, h = int(110 * scale), int(95 * scale)
            rect = pygame.Rect(x - w//2, y - h//2, w, h)
            pygame.draw.rect(surface, (140, 25, 25), rect, border_radius=int(4 * scale))
            sim_w, sim_h = int(35 * scale), int(45 * scale)
            pygame.draw.rect(surface, (30, 30, 35), (x - sim_w//2, y - sim_h//2, sim_w, sim_h), border_radius=2)

        elif comp_type == "BOX":
            w, h = int(280 * scale), int(260 * scale)
            rect = pygame.Rect(x - w//2, y - h//2, w, h)
            pygame.draw.rect(surface, (40, 45, 55), rect, border_radius=int(12 * scale))
            pygame.draw.rect(surface, (160, 170, 180), rect, width=int(4 * scale), border_radius=int(12 * scale))
            pygame.draw.rect(surface, (30, 140, 220), rect.inflate(int(-16*scale), int(-16*scale)), width=int(2 * scale), border_radius=int(8 * scale))

    def draw_3d_rock(self, surface, x, y, radius):
        # Base jagged dark structural backing shadow footprint
        jagged_points = [
            (x - radius, y - int(radius*0.7)), (x - int(radius*0.4), y - radius),
            (x + int(radius*0.6), y - int(radius*0.9)), (x + radius, y - int(radius*0.2)),
            (x + int(radius*0.8), y + int(radius*0.6)), (x + int(radius*0.2), y + radius),
            (x - int(radius*0.7), y + int(radius*0.8)), (x - radius, y + int(radius*0.1))
        ]
        pygame.draw.polygon(surface, (55, 55, 60), jagged_points)
        
        # Faceted structural shaded core layers
        for step, col in [(0.8, (100, 100, 105)), (0.6, (125, 125, 130)), (0.4, (145, 145, 150))]:
            inner_pts = [(x + int((px - x) * step), y + int((py - y) * step)) for px, py in jagged_points]
            pygame.draw.polygon(surface, col, inner_pts)
            
        # Specular light highlight ridge lines on top surfaces
        pygame.draw.line(surface, (180, 180, 185), (x - int(radius*0.4), y - int(radius*0.4)), (x + int(radius*0.2), y - int(radius*0.5)), width=3)

    def draw_turtle_figure(self, surface, x, y):
        pygame.draw.ellipse(surface, COLOR_TURTLE, (x - 25, y - 20, 50, 40))
        pygame.draw.circle(surface, COLOR_TURTLE, (x + 28, y), 9)
        for ox, oy in [(-18, -22), (14, -22), (-18, 22), (14, 22)]:
            pygame.draw.circle(surface, (60, 80, 50), (x + ox, y + oy), 7)

    def draw_topdown_tree(self, surface, x, y, radius):
        # Base canopy shadow
        pygame.draw.circle(surface, (45, 60, 40), (x + 4, y + 4), radius)
        # Layered foliage rings for depth
        for r, color in [(radius, (50, 105, 60)), (int(radius*0.8), (65, 125, 75)), (int(radius*0.5), (85, 150, 95))]:
            pygame.draw.circle(surface, color, (x, y), r)
            # Add small leaf detail segments
            pygame.draw.circle(surface, (color[0]+10, color[1]+10, color[2]+10), (x - int(r*0.2), y - int(r*0.2)), int(r*0.3))

    def draw(self, surface):
        if self.current_scene in ["INTRO", "ASSEMBLY"]:
            surface.fill(COLOR_BG_LIGHT)
        else:
            surface.fill(COLOR_BG_DARK)

        if self.current_scene == "INTRO":
            self.draw_header(surface, "PROJECT DEVELOPMENT INTERFACE", "System Blueprint Architecture", True)
            
            rect_outer = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 160, 500, 320)
            pygame.draw.rect(surface, (220, 225, 230), rect_outer, border_radius=16)
            pygame.draw.rect(surface, (140, 150, 160), rect_outer, width=2, border_radius=16)
            
            for ox, oy in [(-250, -140), (210, -140), (-250, 60), (210, 60)]:
                pygame.draw.rect(surface, COLOR_ROBOT_WHEEL, (WIDTH//2 + ox, HEIGHT//2 + oy, 40, 100), border_radius=8)

            self.draw_spec_label(surface, WIDTH // 2, HEIGHT // 2 - 200, "Total Chassis Width: 14 Inches", center=True, is_light_bg=True)
            self.draw_spec_label(surface, WIDTH // 2, HEIGHT // 2 - 240, "Total Chassis Length: 18 Inches", center=True, is_light_bg=True)
            self.draw_spec_label(surface, WIDTH // 2, HEIGHT // 2 - 280, "Total Vehicle Height: 12 Inches", center=True, is_light_bg=True)
            
            surf_mid = FONT_SUBTITLE.render("The TurTech Rover Exterior", True, COLOR_TEXT_DARK)
            rect_mid = surf_mid.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            surface.blit(surf_mid, rect_mid)

        elif self.current_scene == "ASSEMBLY":
            self.draw_header(surface, "ROBOTIC COMPONENT INTEGRATION STAGE", "Assembling Interior Payload Arrays Automatically", True)
            
            chassis_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 - 160, 320, 320)
            pygame.draw.rect(surface, (220, 225, 230), chassis_rect, border_radius=12)
            pygame.draw.rect(surface, (140, 150, 160), chassis_rect, width=3, border_radius=12)
            for wx, wy in [(WIDTH//2 - 195, HEIGHT//2 - 140), (WIDTH//2 + 160, HEIGHT//2 - 140), (WIDTH//2 - 195, HEIGHT//2 + 60), (WIDTH//2 + 160, HEIGHT//2 + 60)]:
                pygame.draw.rect(surface, COLOR_ROBOT_WHEEL, (wx, wy, 35, 80), border_radius=6)

            # 1. Draw already locked components inside position (Keeping the solid grey enclosure covering everything)
            for idx in range(self.assembly_index):
                comp = COMPONENTS[idx]
                if comp["type"] == "VCO":
                    w = int(380 * 0.5 * 0.7)
                    h = int(120 * 0.5 * 0.7)
                    wave_panel = pygame.Rect(comp["target_pos_x"] - w // 2, comp["target_pos_y"] - h // 2, w, h)
                    pygame.draw.rect(surface, (20, 24, 30), wave_panel, border_radius=int(8 * 0.5))
                    pygame.draw.rect(surface, (100, 110, 120), wave_panel, width=1, border_radius=int(8 * 0.5))
                    line_y = wave_panel.centery + int(15 * 0.5)
                    pygame.draw.line(surface, (0, 210, 255), (wave_panel.left + int(10 * 0.5), line_y), (wave_panel.right - int(10 * 0.5), line_y), width=1)
                elif comp["type"] == "BOX":
                    # Full size 330x330 solid enclosure shield covering all layers completely
                    rect = pygame.Rect(WIDTH // 2 - 165, HEIGHT // 2 - 165, 330, 330)
                    pygame.draw.rect(surface, (120, 125, 130), rect, border_radius=14)
                    pygame.draw.rect(surface, (180, 185, 190), rect, width=4, border_radius=14)
                else:
                    self.draw_detailed_component(surface, comp["type"], comp["target_pos_x"], comp["target_pos_y"], 0.5)

            # Safeguard variable initialization to prevent UnboundLocalError crashes
            active_comp = None 
            
            if self.assembly_index < len(COMPONENTS):
                active_comp = COMPONENTS[self.assembly_index]
                
                panel_rect = pygame.Rect(50, 160, 440, 235)
                pygame.draw.rect(surface, (255, 255, 255), panel_rect, border_radius=12)
                pygame.draw.rect(surface, COLOR_ACCENT, panel_rect, width=2, border_radius=12)
                
                txt_name = FONT_SUBTITLE.render(active_comp["name"], True, COLOR_TEXT_DARK)
                surface.blit(txt_name, (70, 185))
                
                self.draw_multiline_text(surface, active_comp["desc"], 70, 235, 370, True)

                # 2. Draw the traveling physical component LAST so it flies over the top
                if active_comp["type"] == "VCO":
                    w = int(380 * self.comp_scale * 0.7)
                    h = int(120 * self.comp_scale * 0.7)
                    wave_panel = pygame.Rect(int(self.comp_x) - w // 2, int(self.comp_y) - h // 2, w, h)
                    pygame.draw.rect(surface, (20, 24, 30), wave_panel, border_radius=int(8 * self.comp_scale))
                    pygame.draw.rect(surface, (100, 110, 120), wave_panel, width=1, border_radius=int(8 * self.comp_scale))
                    line_y = wave_panel.centery + int(15 * self.comp_scale)
                    pygame.draw.line(surface, (0, 210, 255), (wave_panel.left + int(10 * self.comp_scale), line_y), (wave_panel.right - int(10 * self.comp_scale), line_y), width=max(1, int(2 * self.comp_scale)))
                elif active_comp["type"] == "BOX":
                    # While breathing on the side, it maintains its solid frame presentation
                    if self.assembly_timer < 390:
                        w = int(240 * self.comp_scale * 0.7)
                        h = int(240 * self.comp_scale * 0.7)
                        rect = pygame.Rect(int(self.comp_x) - w // 2, int(self.comp_y) - h // 2, w, h)
                        pygame.draw.rect(surface, (120, 125, 130), rect, border_radius=int(12 * self.comp_scale * 0.7))
                        pygame.draw.rect(surface, (180, 185, 190), rect, width=int(3 * self.comp_scale * 0.7), border_radius=int(12 * self.comp_scale * 0.7))
                    else:
                        # As it moves into the robot, it smoothly expands to fully enclose the whole core frame matrix (330x330)
                        t = (self.assembly_timer - 390) / 60.0
                        w = int((240 * 0.7) + (330 - (240 * 0.7)) * t)
                        h = int((240 * 0.7) + (330 - (240 * 0.7)) * t)
                        rect = pygame.Rect(int(self.comp_x) - w // 2, int(self.comp_y) - h // 2, w, h)
                        pygame.draw.rect(surface, (120, 125, 130), rect, border_radius=14)
                        pygame.draw.rect(surface, (180, 185, 190), rect, width=4, border_radius=14)

                else:
                    self.draw_detailed_component(surface, active_comp["type"], int(self.comp_x), int(self.comp_y), self.comp_scale)
                
            if self.assembly_complete:
                success_txt = FONT_TITLE.render("Assembly Complete! Finding Turtle Adventure Begins.", True, COLOR_ACCENT)
                surface.blit(success_txt, (WIDTH // 2 - success_txt.get_width() // 2, 160))
                
            # Hardware Architectural Abbreviation Glossary Definitions Footer
            glossary_y = HEIGHT - 110
            pygame.draw.line(surface, (210, 215, 220), (50, glossary_y - 15), (WIDTH - 50, glossary_y - 15), width=1)
            
            lbl_glo_title = pygame.font.SysFont("Arial", 14, bold=True).render("SYSTEM BLUEPRINT ARCHITECTURE GLOSSARY:", True, COLOR_TEXT_MUTED)
            surface.blit(lbl_glo_title, (50, glossary_y))
            
            glossary_text = (
                "• VCO: Voltage-Controlled Oscillator (Generates continuous varying frequency radar signals)   "
                "• FMCW: Frequency-Modulated Continuous Wave (Radar processing technique used to map subsurface anomalies)   "
                "• FFT: Fast Fourier Transform (Algorithm processing time-domain signal waves into distance vectors)   "
                "• IP65: Ingress Protection Rating 65 (Dust-tight and fully sealed against directed water jets)"
            )
            self.draw_multiline_text(surface, glossary_text, 50, glossary_y + 25, WIDTH - 100, is_light_bg=True)

        elif self.current_scene == "TESTING":
            if self.view_mode == "TOP":
                surface.fill(COLOR_DIRT)
                pygame.draw.rect(surface, COLOR_GRASS, (0, 0, WIDTH, 160))
                pygame.draw.rect(surface, COLOR_GRASS, (0, HEIGHT-180, WIDTH, 180))
                
                # Denser, comprehensive collection of scattered grass blades across the open test field matrix
                grass_coordinates = [
                    (100, 220), (180, 340), (280, 210), (350, 480), (420, 260), (490, 510),
                    (600, 250), (680, 430), (740, 290), (850, 520), (920, 340), (1020, 490),
                    (1100, 300), (1180, 450), (WIDTH-200, 400), (450, 310), (950, 210),
                    (150, 450), (250, 530), (550, 200), (780, 500), (880, 230), (1050, 220)
                ]
                for gx, gy in grass_coordinates:
                    pygame.draw.line(surface, (80, 130, 75), (gx, gy), (gx - 5, gy - 12), width=2)
                    pygame.draw.line(surface, (80, 130, 75), (gx, gy), (gx + 2, gy - 15), width=2)
                    pygame.draw.line(surface, (80, 130, 75), (gx, gy), (gx + 8, gy - 10), width=2)

                # Draw peripheral environmental background trees
                self.draw_topdown_tree(surface, 150, 90, 45)
                self.draw_topdown_tree(surface, WIDTH - 180, 80, 50)
                self.draw_topdown_tree(surface, 220, HEIGHT - 100, 55)
                self.draw_topdown_tree(surface, WIDTH - 300, HEIGHT - 90, 48)

                # Draw the newly textured realistic boulder obstacle asset
                self.draw_3d_rock(surface, int(WIDTH * 0.32), HEIGHT // 2 - 40, 65)
                lbl_rock = FONT_BODY.render("Obstacle: Compact Rock Anomaly", True, (255, 255, 255))
                surface.blit(lbl_rock, (int(WIDTH * 0.23), HEIGHT // 2 - 130))

                t1_x, t1_y = int(WIDTH * 0.52), HEIGHT // 2 - 25
                self.draw_turtle_figure(surface, t1_x, t1_y)
                
                lbl_t1 = FONT_UI.render("Eastern Box Turtle Target #1", True, (255, 255, 180))
                surface.blit(lbl_t1, (t1_x - 100, t1_y - 65))

                t2_x, t2_y = int(WIDTH * 0.80), HEIGHT // 2 + 120
                self.draw_turtle_figure(surface, t2_x, t2_y)
                lbl_t2 = FONT_UI.render("Eastern Box Turtle Target #2", True, (255, 255, 180))
                surface.blit(lbl_t2, (t2_x - 100, t2_y - 65))

                rx, ry = int(self.robot_x), int(self.robot_y)
                for ox, oy in [(-45, -50), (20, -50), (-45, 35), (20, 35)]:
                    pygame.draw.rect(surface, COLOR_ROBOT_WHEEL, (rx+ox, ry+oy, 25, 55), border_radius=6)
                pygame.draw.rect(surface, COLOR_ROBOT_BODY, (rx-35, ry-35, 70, 70), border_radius=8)
                pygame.draw.line(surface, COLOR_ANTENNA, (rx+35, ry-20), (rx+60, ry-20), width=4)
                pygame.draw.line(surface, COLOR_ANTENNA, (rx+35, ry+20), (rx+60, ry+20), width=4)
                
                if "SCANNING" in self.sim_step:
                    for r_arc in range(15, 55, 15):
                        pygame.draw.arc(surface, COLOR_ACCENT, (rx+35, ry-40, r_arc*2, 80), -0.5, 0.5, width=3)

                pygame.draw.rect(surface, COLOR_PANEL, (0, HEIGHT-90, WIDTH, 90))
                status_str = f"SYSTEM STATUS: VEHICLE ACTIVE EXECUTION  |  SEEK PATH: {self.sim_step}  |  RADAR SENSORS: ONLINE"
                txt_status = FONT_SUBTITLE.render(status_str, True, COLOR_TEXT_LIGHT)
                surface.blit(txt_status, (40, HEIGHT - 55))

            elif self.view_mode == "SIDE":
                surface.fill((40, 30, 25))
                pygame.draw.rect(surface, COLOR_DIRT, (0, 0, WIDTH, HEIGHT // 2 - 40))
                pygame.draw.rect(surface, COLOR_GRASS, (0, 0, WIDTH, 60))
                
                pygame.draw.line(surface, (100, 100, 100), (0, HEIGHT // 2 - 40), (WIDTH, HEIGHT // 2 - 40), width=3)
                lbl_surface = FONT_UI.render("SURFACE DIRT BOUNDARY LEVEL", True, COLOR_TEXT_MUTED)
                surface.blit(lbl_surface, (30, HEIGHT // 2 - 80))

                pygame.draw.rect(surface, COLOR_ROBOT_BODY, (WIDTH//2 - 100, HEIGHT//2 - 160, 200, 90), border_radius=8)
                pygame.draw.circle(surface, COLOR_ROBOT_WHEEL, (WIDTH//2 - 60, HEIGHT//2 - 60), 30)
                pygame.draw.circle(surface, COLOR_ROBOT_WHEEL, (WIDTH//2 + 60, HEIGHT//2 - 60), 30)
                pygame.draw.rect(surface, COLOR_ANTENNA, (WIDTH//2 + 95, HEIGHT//2 - 100, 30, 15))

                # 1. Draw the turtle figure safely above the measurement scale
                self.draw_turtle_figure(surface, WIDTH//2, HEIGHT//2 + 80)
                
                # 2. Draw the vertical measurement line aligned with the text block
                pygame.draw.line(surface, COLOR_ACCENT, (WIDTH//2 - 200, HEIGHT//2 + 135), (WIDTH//2 - 200, HEIGHT//2 + 165), width=3)
                
                # 3. Draw the scale label cleanly grouped underneath the graphic layout
                lbl_depth = FONT_BODY.render("Hiding Depth: 1-6 Inches Below Soil Matrix", True, COLOR_ACCENT)
                surface.blit(lbl_depth, (WIDTH//2 - 180, HEIGHT//2 + 140))

                for wave_d in range(20, 160, 30):
                    wave_y = (HEIGHT // 2 - 40) + (wave_d * (self.scan_progress / 100.0))
                    if wave_y < HEIGHT // 2 + 100:
                        pygame.draw.line(surface, (0, 210, 255), (WIDTH//2 - 80, int(wave_y)), (WIDTH//2 + 80, int(wave_y)), width=3)

                pygame.draw.rect(surface, COLOR_PANEL, (WIDTH - 480, 80, 420, 220), border_radius=12)
                pygame.draw.rect(surface, (0, 210, 255), (WIDTH - 480, 80, 420, 220), width=2, border_radius=12)
                lbl_diff = FONT_SUBTITLE.render("FMCW Anomaly Processing", True, COLOR_TEXT_LIGHT)
                lbl_d1 = FONT_BODY.render("• Rock Anomaly: Uniform Static Dielectric", True, COLOR_TEXT_MUTED)
                lbl_d2 = FONT_BODY.render("• Target: High Tissue Permittivity Variant", True, COLOR_ACCENT)
                lbl_d3 = FONT_BODY.render("Status Flag: High Biasing Probability Confirmed", True, (255, 255, 150))
                surface.blit(lbl_diff, (WIDTH - 450, 110))
                surface.blit(lbl_d1, (WIDTH - 450, 160))
                surface.blit(lbl_d2, (WIDTH - 450, 200))
                surface.blit(lbl_d3, (WIDTH - 450, 240))

            if self.phone_alert_active:
                phone_rect = pygame.Rect(60, HEIGHT // 2 - 250, 280, 440)
                pygame.draw.rect(surface, (10, 15, 20), phone_rect, border_radius=25)
                pygame.draw.rect(surface, (90, 95, 100), phone_rect, width=3, border_radius=25)
                screen_rect = pygame.Rect(74, HEIGHT // 2 - 210, 252, 360)
                pygame.draw.rect(surface, (245, 245, 250), screen_rect, border_radius=6)
                
                msg_rect = pygame.Rect(82, HEIGHT // 2 - 180, 236, 110)
                pygame.draw.rect(surface, (255, 255, 255), msg_rect, border_radius=10)
                pygame.draw.rect(surface, COLOR_ACCENT, msg_rect, width=2, border_radius=10)
                
                lbl_app = pygame.font.SysFont("Arial", 12, bold=True).render("THE TURTECH APP • NOW", True, COLOR_ACCENT)
                lbl_msg1 = pygame.font.SysFont("Arial", 15, bold=True).render(self.phone_alert_msg, True, (10, 10, 10))
                lbl_msg2 = pygame.font.SysFont("Arial", 13).render("Pos: Tracker Zone Grid Array", True, (50, 50, 50))
                lbl_msg3 = pygame.font.SysFont("Arial", 13).render("Halting rover drive path telemetry.", True, (50, 50, 50))
                
                surface.blit(lbl_app, (94, HEIGHT // 2 - 165))
                surface.blit(lbl_msg1, (94, HEIGHT // 2 - 140))
                surface.blit(lbl_msg2, (94, HEIGHT // 2 - 112))
                surface.blit(lbl_msg3, (94, HEIGHT // 2 - 92))

        elif self.current_scene == "OUTRO":
            surface.fill((255, 255, 255))

            if not hasattr(self, 'typewriter_chars'):
                self.typewriter_chars = 0

            # Full raw text segments for evaluation
            str1 = "The TurTech - Precision Protection Model"
            str2 = "Challenge X Case Presentation Solution"
            str3 = "Mitigating site construction fatalities effectively via autonomous subsurface radar monitoring."
            str4 = "Thank you for your time and consideration."
            
            # Calculate typewriter slicing windows across each line sequentially
            rem = self.typewriter_chars
            
            sub1 = str1[:max(0, min(len(str1), rem))]
            rem -= len(str1) + 15  # 15-frame pause before typing next line
            
            sub2 = str2[:max(0, min(len(str2), rem))]
            rem -= len(str2) + 15
            
            sub3 = str3[:max(0, min(len(str3), rem))]
            rem -= len(str3) + 15
            
            sub4 = str4[:max(0, min(len(str4), rem))]

            # Render text surfaces using the dynamically sliced strings
            txt_e1 = FONT_TITLE.render(sub1, True, (20, 20, 20))
            txt_e2 = FONT_SUBTITLE.render(sub2, True, (60, 60, 60))
            txt_e3 = FONT_BODY.render(sub3, True, (100, 100, 100))
            txt_e4 = FONT_UI.render(sub4, True, COLOR_ACCENT)
            
            # Render lines with generous professional double-spacing layout geometry
            start_y = HEIGHT // 2 - 160
            surface.blit(txt_e1, (WIDTH // 2 - txt_e1.get_width() // 2, start_y))
            surface.blit(txt_e2, (WIDTH // 2 - txt_e2.get_width() // 2, start_y + 70))
            surface.blit(txt_e3, (WIDTH // 2 - txt_e3.get_width() // 2, start_y + 145))
            surface.blit(txt_e4, (WIDTH // 2 - txt_e4.get_width() // 2, start_y + 225))
            
            if self.outro_timer > 300:
                black_fade = pygame.Surface((WIDTH, HEIGHT))
                black_fade.fill((0, 0, 0))
                alpha = min(255, (self.outro_timer - 300) * 4)
                black_fade.set_alpha(alpha)
                surface.blit(black_fade, (0, 0))

        elif self.current_scene == "BLACKOUT":
            surface.fill((0, 0, 0))

        for btn in self.buttons:
            btn.draw(surface)

    def draw_header(self, surface, main_title, sub_title, is_light_bg=False):
        txt_color = COLOR_TEXT_DARK if is_light_bg else COLOR_TEXT_LIGHT
        t_surf = FONT_TITLE.render(main_title, True, txt_color)
        s_surf = FONT_SUBTITLE.render(sub_title, True, COLOR_TEXT_MUTED)
        surface.blit(t_surf, (50, 45))
        surface.blit(s_surf, (50, 100))
        pygame.draw.line(surface, (200, 205, 210) if is_light_bg else COLOR_PANEL, (50, 145), (WIDTH - 50, 145), width=2)

    def draw_spec_label(self, surface, x, y, text, center=False, large=False, is_light_bg=False):
        f = FONT_SUBTITLE if large else FONT_BODY
        if is_light_bg:
            c = COLOR_TEXT_DARK if not large else (30, 30, 30)
        else:
            c = COLOR_TEXT_LIGHT if not large else (255, 255, 255)
        surf = f.render(text, True, c)
        rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
        surface.blit(surf, rect)

    def draw_multiline_text(self, surface, text, x, y, max_w, is_light_bg=False):
        words = text.split(' ')
        space_w = FONT_BODY.size(' ')[0]
        cur_x, cur_y = x, y
        txt_color = COLOR_TEXT_DARK if is_light_bg else COLOR_TEXT_LIGHT
        for word in words:
            word_surf = FONT_BODY.render(word, True, txt_color)
            word_w, word_h = word_surf.get_size()
            if cur_x + word_w >= x + max_w:
                cur_x = x
                cur_y += word_h + 4
            surface.blit(word_surf, (cur_x, cur_y))
            cur_x += word_w + space_w

def main():
    state = ApplicationState()
    running = True
    while running:
        if state.current_scene == "INTRO" and not state.buttons:
            state.buttons = [Button(WIDTH // 2 - 120, HEIGHT // 2 + 190, 240, 60, "Start Building", state.start_building)]
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    # Toggles state tracking between True and False on every Space keydown tap
                    state.is_paused = not state.is_paused
            
            # Only let buttons intercept click events if the presentation view is not frozen
            if not state.is_paused:
                for btn in state.buttons:
                    btn.handle_event(event)
        
        state.update()
        state.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
