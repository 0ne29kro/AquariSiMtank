import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coral Reef Aquarium")

# Colors
OCEAN_BLUE = (20, 105, 140)
OCEAN_DEEP = (15, 80, 110)
SAND_COLOR = (194, 178, 128)
ROCK_DARK = (80, 70, 60)
ROCK_LIGHT = (120, 110, 100)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)

# Fish rendering style: 0=Realistic, 1=Cartoon, 2=Pixel, 3=Tropical, 4=Army, 5=Air Force, 6=Space Force, 7=Navy
fish_style = 0
fish_style_names = ["Realistic", "Cartoon", "Pixel Art", "Tropical", "US Army", "Air Force", "Space Force", "Navy"]

# Background scene: 0=None, 1=Whale, 2=Tank, 3=Fighter Jet, 4=Battleship, 5=Space Shuttle
background_scene = 0
background_scene_names = ["None", "Whale Migration", "Tank Assault", "Air Strike", "Naval Barrage", "Space Launch"]

# Distance scale factor for background (appears 2x farther away)
BG_SCALE = 0.5
# Fixed Y level: halfway between top of screen (0) and top of ship hull (450)
BG_Y = 225

# UI visibility toggle
ui_visible = True


class BackgroundWhale:
    """Majestic whale crossing in the distance"""
    def __init__(self):
        self.x = -300
        self.y = BG_Y
        self.speed = 0.8 * BG_SCALE
        self.length = 400 * BG_SCALE
        self.height = 100 * BG_SCALE
        self.tail_angle = 0
        self.tail_speed = 0.03
        self.body_wave = 0
        
    def update(self):
        self.x += self.speed
        if self.x > WIDTH + 400:
            self.x = -400
        
        self.tail_angle += self.tail_speed
        self.body_wave += 0.02
        
    def draw(self, screen):
        # Whale colors (solid, no transparency)
        whale_color = (60, 80, 100)
        whale_light = (80, 100, 120)
        whale_dark = (40, 55, 70)
        
        # Body undulation
        wave_offset = math.sin(self.body_wave) * 5
        
        cx = self.x
        cy = self.y + wave_offset
        
        # Main body - elongated ellipse
        body_points = []
        for i in range(32):
            angle = (i / 32) * 2 * math.pi
            # Tapered at both ends, fatter in middle
            taper = 1.0 - 0.4 * abs(math.cos(angle))
            px = cx + math.cos(angle) * self.length * 0.5
            py = cy + math.sin(angle) * self.height * 0.5 * taper
            body_points.append((px, py))
        
        pygame.draw.polygon(screen, whale_color, body_points)
        
        # Head (front bulge)
        head_x = cx + self.length * 0.4
        head_y = cy
        pygame.draw.ellipse(screen, whale_color, 
                           (head_x - 30 * BG_SCALE, head_y - 40 * BG_SCALE, 
                            80 * BG_SCALE, 80 * BG_SCALE))
        
        # Tail fluke with animation
        tail_x = cx - self.length * 0.5
        tail_y = cy
        tail_wave = math.sin(self.tail_angle) * 25 * BG_SCALE
        
        # Left fluke
        pygame.draw.polygon(screen, whale_dark, [
            (tail_x, tail_y),
            (tail_x - 60 * BG_SCALE, tail_y - 50 * BG_SCALE + tail_wave),
            (tail_x - 30 * BG_SCALE, tail_y + tail_wave * 0.5)
        ])
        # Right fluke
        pygame.draw.polygon(screen, whale_dark, [
            (tail_x, tail_y),
            (tail_x - 60 * BG_SCALE, tail_y + 50 * BG_SCALE + tail_wave),
            (tail_x - 30 * BG_SCALE, tail_y + tail_wave * 0.5)
        ])
        
        # Dorsal fin
        dorsal_x = cx - self.length * 0.1
        dorsal_y = cy - self.height * 0.4
        pygame.draw.polygon(screen, whale_dark, [
            (dorsal_x - 20 * BG_SCALE, dorsal_y + 20 * BG_SCALE),
            (dorsal_x, dorsal_y - 30 * BG_SCALE),
            (dorsal_x + 30 * BG_SCALE, dorsal_y + 20 * BG_SCALE)
        ])
        
        # Pectoral fin
        pec_x = cx + self.length * 0.15
        pec_y = cy + self.height * 0.3
        pec_wave = math.sin(self.tail_angle * 0.5) * 10 * BG_SCALE
        pygame.draw.ellipse(screen, whale_dark,
                           (pec_x - 40 * BG_SCALE, pec_y + pec_wave, 
                            80 * BG_SCALE, 25 * BG_SCALE))
        
        # Eye
        eye_x = cx + self.length * 0.38
        eye_y = cy - self.height * 0.15
        pygame.draw.circle(screen, (20, 30, 40), (int(eye_x), int(eye_y)), int(8 * BG_SCALE))
        pygame.draw.circle(screen, (150, 160, 170), (int(eye_x - 2), int(eye_y - 2)), int(3 * BG_SCALE))
        
        # Belly lighter area
        belly_points = []
        for i in range(16):
            ratio = i / 15
            bx = cx - self.length * 0.3 + ratio * self.length * 0.6
            by = cy + self.height * 0.35 + math.sin(ratio * math.pi) * 10 * BG_SCALE
            belly_points.append((bx, by))
        for i in range(16):
            ratio = 1 - i / 15
            bx = cx - self.length * 0.3 + ratio * self.length * 0.6
            by = cy + self.height * 0.2
            belly_points.append((bx, by))
        if len(belly_points) > 2:
            pygame.draw.polygon(screen, whale_light, belly_points)
        
        # Spout (occasional)
        if int(self.x) % 400 < 100:
            spout_x = head_x + 10 * BG_SCALE
            spout_y = head_y - 50 * BG_SCALE
            for i in range(5):
                spray_x = spout_x + random.randint(-10, 10) * BG_SCALE
                spray_y = spout_y - i * 15 * BG_SCALE - random.randint(0, 20) * BG_SCALE
                pygame.draw.circle(screen, (200, 220, 240), (int(spray_x), int(spray_y)), int((5 - i) * BG_SCALE))


class BackgroundTank:
    """Tank rolling across with realistic track movement"""
    def __init__(self):
        self.x = -200
        self.y = BG_Y
        self.speed = 1.2 * BG_SCALE
        self.width = 200 * BG_SCALE
        self.height = 80 * BG_SCALE
        self.track_offset = 0
        self.turret_angle = -0.2
        self.muzzle_flash = 0
        self.shell_x = 0
        self.shell_y = 0
        self.shell_active = False
        self.wall_x = WIDTH * 0.7
        self.wall_health = 100
        self.explosion_particles = []
        
    def update(self):
        self.x += self.speed
        self.track_offset += self.speed * 2
        
        # Fire shell periodically
        if int(self.x) % 300 == 150 and not self.shell_active and self.x < self.wall_x - 100:
            self.shell_active = True
            self.shell_x = self.x + self.width * 0.6
            self.shell_y = self.y - self.height * 0.5
            self.muzzle_flash = 10
        
        # Update shell
        if self.shell_active:
            self.shell_x += 8
            if self.shell_x > self.wall_x and self.wall_health > 0:
                self.wall_health -= 34
                self.shell_active = False
                # Create explosion
                for _ in range(15):
                    self.explosion_particles.append({
                        'x': self.wall_x,
                        'y': self.shell_y,
                        'vx': random.uniform(-3, 3),
                        'vy': random.uniform(-4, 2),
                        'life': random.randint(20, 40),
                        'size': random.randint(3, 8)
                    })
        
        # Update explosions
        for p in self.explosion_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15
            p['life'] -= 1
            if p['life'] <= 0:
                self.explosion_particles.remove(p)
        
        if self.muzzle_flash > 0:
            self.muzzle_flash -= 1
        
        # Reset when off screen
        if self.x > WIDTH + 300:
            self.x = -250
            self.wall_health = 100
            self.explosion_particles = []
        
    def draw(self, screen):
        # Tank colors (solid)
        tank_green = (70, 85, 60)
        tank_dark = (45, 55, 40)
        track_color = (40, 40, 35)
        
        cx = self.x
        cy = self.y
        
        # Tracks (bottom)
        track_height = 25 * BG_SCALE
        track_width = self.width * 1.1
        
        # Track body
        pygame.draw.rect(screen, track_color, 
                        (cx - track_width * 0.5, cy, track_width, track_height))
        
        # Track wheels
        num_wheels = 6
        for i in range(num_wheels):
            wheel_x = cx - track_width * 0.4 + i * (track_width * 0.8 / (num_wheels - 1))
            wheel_y = cy + track_height * 0.5
            pygame.draw.circle(screen, tank_dark, (int(wheel_x), int(wheel_y)), int(10 * BG_SCALE))
            # Wheel rotation marks
            rot = self.track_offset * 0.1 + i
            pygame.draw.line(screen, track_color, 
                           (int(wheel_x - 5 * math.cos(rot) * BG_SCALE), int(wheel_y - 5 * math.sin(rot) * BG_SCALE)),
                           (int(wheel_x + 5 * math.cos(rot) * BG_SCALE), int(wheel_y + 5 * math.sin(rot) * BG_SCALE)), 2)
        
        # Track treads (animated)
        tread_spacing = 12 * BG_SCALE
        for i in range(int(track_width / tread_spacing) + 2):
            tread_x = cx - track_width * 0.5 + ((i * tread_spacing + self.track_offset) % track_width)
            pygame.draw.line(screen, (30, 30, 25),
                           (int(tread_x), int(cy)), (int(tread_x), int(cy + track_height)), 2)
        
        # Hull
        hull_points = [
            (cx - self.width * 0.45, cy),
            (cx - self.width * 0.5, cy - self.height * 0.4),
            (cx + self.width * 0.4, cy - self.height * 0.4),
            (cx + self.width * 0.5, cy - self.height * 0.2),
            (cx + self.width * 0.45, cy)
        ]
        pygame.draw.polygon(screen, tank_green, hull_points)
        pygame.draw.polygon(screen, tank_dark, hull_points, 2)
        
        # Turret
        turret_x = cx
        turret_y = cy - self.height * 0.5
        pygame.draw.ellipse(screen, tank_green,
                           (turret_x - 35 * BG_SCALE, turret_y - 20 * BG_SCALE,
                            70 * BG_SCALE, 40 * BG_SCALE))
        
        # Main gun
        gun_length = 80 * BG_SCALE
        gun_end_x = turret_x + math.cos(self.turret_angle) * gun_length
        gun_end_y = turret_y + math.sin(self.turret_angle) * gun_length
        pygame.draw.line(screen, tank_dark, (int(turret_x), int(turret_y)), 
                        (int(gun_end_x), int(gun_end_y)), int(8 * BG_SCALE))
        
        # Muzzle flash
        if self.muzzle_flash > 0:
            pygame.draw.circle(screen, (255, 200, 50), (int(gun_end_x), int(gun_end_y)), int(15 * BG_SCALE))
        
        # Shell in flight
        if self.shell_active:
            pygame.draw.ellipse(screen, (80, 80, 70),
                              (int(self.shell_x - 8), int(self.shell_y - 3), 16, 6))
        
        # Wall
        if self.wall_health > 0:
            wall_color = (100, 90, 80)
            wall_height = 150 * BG_SCALE * (self.wall_health / 100)
            pygame.draw.rect(screen, wall_color,
                           (self.wall_x, cy - wall_height + track_height, 30 * BG_SCALE, wall_height))
            # Wall bricks
            brick_h = 15 * BG_SCALE
            for row in range(int(wall_height / brick_h)):
                by = cy - row * brick_h
                pygame.draw.line(screen, (70, 65, 55),
                               (int(self.wall_x), int(by)), (int(self.wall_x + 30 * BG_SCALE), int(by)), 1)
        
        # Explosions
        for p in self.explosion_particles:
            exp_color = (255, random.randint(100, 200), 50)
            pygame.draw.circle(screen, exp_color, (int(p['x']), int(p['y'])), int(p['size'] * BG_SCALE))
        
        # Dust trail
        for i in range(5):
            dust_x = cx - self.width * 0.5 - i * 20
            dust_y = cy + track_height
            dust_color = (150, 140, 120)
            pygame.draw.circle(screen, dust_color, (int(dust_x), int(dust_y)), int((8 - i) * BG_SCALE))


class BackgroundJet:
    """Fighter jet with missiles and afterburners"""
    def __init__(self):
        self.x = -150
        self.y = BG_Y
        self.speed = 4 * BG_SCALE
        self.length = 120 * BG_SCALE
        self.afterburner = True
        self.afterburner_flicker = 0
        self.missiles = []
        self.wall_x = WIDTH * 0.65
        self.wall_health = 100
        self.explosions = []
        self.fired = False
        
    def update(self):
        self.x += self.speed
        self.afterburner_flicker += 0.3
        
        # Fire missiles at wall
        if self.x > WIDTH * 0.2 and not self.fired and self.wall_health > 0:
            for i in range(2):
                self.missiles.append({
                    'x': self.x + self.length * 0.3,
                    'y': self.y + (i - 0.5) * 20 * BG_SCALE,
                    'speed': 6,
                    'trail': []
                })
            self.fired = True
        
        # Update missiles
        for m in self.missiles[:]:
            m['x'] += m['speed']
            m['trail'].append((m['x'] - 10, m['y']))
            if len(m['trail']) > 20:
                m['trail'].pop(0)
            
            if m['x'] > self.wall_x and self.wall_health > 0:
                self.wall_health -= 50
                self.missiles.remove(m)
                # Big explosion
                for _ in range(25):
                    self.explosions.append({
                        'x': self.wall_x,
                        'y': m['y'],
                        'vx': random.uniform(-5, 5),
                        'vy': random.uniform(-6, 4),
                        'life': random.randint(25, 50),
                        'size': random.randint(4, 12)
                    })
        
        # Update explosions
        for e in self.explosions[:]:
            e['x'] += e['vx']
            e['y'] += e['vy']
            e['vy'] += 0.12
            e['life'] -= 1
            if e['life'] <= 0:
                self.explosions.remove(e)
        
        # Reset
        if self.x > WIDTH + 200:
            self.x = -200
            self.wall_health = 100
            self.fired = False
            self.missiles = []
            self.explosions = []
        
    def draw(self, screen):
        jet_gray = (150, 155, 165)
        jet_dark = (80, 85, 95)
        
        cx = self.x
        cy = self.y
        
        # Fuselage
        fuse_points = [
            (cx + self.length * 0.5, cy),  # Nose
            (cx + self.length * 0.3, cy - 12 * BG_SCALE),
            (cx - self.length * 0.3, cy - 15 * BG_SCALE),
            (cx - self.length * 0.5, cy - 10 * BG_SCALE),
            (cx - self.length * 0.5, cy + 10 * BG_SCALE),
            (cx - self.length * 0.3, cy + 15 * BG_SCALE),
            (cx + self.length * 0.3, cy + 12 * BG_SCALE),
        ]
        pygame.draw.polygon(screen, jet_gray, fuse_points)
        
        # Cockpit
        pygame.draw.ellipse(screen, (100, 150, 200),
                          (cx + self.length * 0.15, cy - 8 * BG_SCALE, 25 * BG_SCALE, 16 * BG_SCALE))
        
        # Wings
        wing_x = cx - self.length * 0.1
        pygame.draw.polygon(screen, jet_dark, [
            (wing_x + 20 * BG_SCALE, cy - 5 * BG_SCALE),
            (wing_x - 30 * BG_SCALE, cy - 50 * BG_SCALE),
            (wing_x - 40 * BG_SCALE, cy - 45 * BG_SCALE),
            (wing_x - 20 * BG_SCALE, cy - 5 * BG_SCALE)
        ])
        pygame.draw.polygon(screen, jet_dark, [
            (wing_x + 20 * BG_SCALE, cy + 5 * BG_SCALE),
            (wing_x - 30 * BG_SCALE, cy + 50 * BG_SCALE),
            (wing_x - 40 * BG_SCALE, cy + 45 * BG_SCALE),
            (wing_x - 20 * BG_SCALE, cy + 5 * BG_SCALE)
        ])
        
        # Tail fins
        tail_x = cx - self.length * 0.45
        pygame.draw.polygon(screen, jet_dark, [
            (tail_x, cy - 10 * BG_SCALE),
            (tail_x - 15 * BG_SCALE, cy - 35 * BG_SCALE),
            (tail_x - 25 * BG_SCALE, cy - 30 * BG_SCALE),
            (tail_x - 10 * BG_SCALE, cy - 10 * BG_SCALE)
        ])
        
        # Afterburners
        if self.afterburner:
            ab_x = cx - self.length * 0.5
            ab_length = 30 + math.sin(self.afterburner_flicker) * 10
            pygame.draw.ellipse(screen, (255, 150, 50),
                              (ab_x - ab_length, cy - 8, ab_length, 16))
            pygame.draw.ellipse(screen, (255, 200, 100),
                              (ab_x - ab_length * 0.7, cy - 5, ab_length * 0.5, 10))
        
        # Missiles in flight
        for m in self.missiles:
            # Trail
            for i, (tx, ty) in enumerate(m['trail']):
                trail_color = (180, 180, 180)
                pygame.draw.circle(screen, trail_color, (int(tx), int(ty)), 2)
            # Missile body
            pygame.draw.ellipse(screen, (200, 200, 190),
                              (int(m['x'] - 12), int(m['y'] - 3), 24, 6))
            # Rocket flame
            pygame.draw.ellipse(screen, (255, 150, 50),
                              (int(m['x'] - 18), int(m['y'] - 2), 8, 4))
        
        # Wall
        if self.wall_health > 0:
            wall_height = 200 * BG_SCALE * (self.wall_health / 100)
            pygame.draw.rect(screen, (90, 85, 75),
                           (self.wall_x, cy - wall_height * 0.5, 25 * BG_SCALE, wall_height))
        
        # Explosions
        for e in self.explosions:
            e_color = (255, random.randint(80, 180), 30)
            pygame.draw.circle(screen, e_color, (int(e['x']), int(e['y'])), int(e['size'] * BG_SCALE))


class BackgroundBattleship:
    """Naval battleship launching torpedoes"""
    def __init__(self):
        self.x = -300
        self.y = BG_Y
        self.speed = 0.6 * BG_SCALE
        self.length = 350 * BG_SCALE
        self.height = 60 * BG_SCALE
        self.torpedoes = []
        self.wall_x = WIDTH * 0.75
        self.wall_health = 100
        self.explosions = []
        self.wake_particles = []
        self.fire_timer = 0
        
    def update(self):
        self.x += self.speed
        self.fire_timer += 1
        
        # Fire torpedoes periodically
        if self.fire_timer % 180 == 90 and self.x > 50 and self.x < self.wall_x - 200:
            self.torpedoes.append({
                'x': self.x + self.length * 0.4,
                'y': self.y + self.height * 0.3,
                'speed': 3,
                'bubble_timer': 0
            })
        
        # Update torpedoes
        for t in self.torpedoes[:]:
            t['x'] += t['speed']
            t['bubble_timer'] += 1
            
            # Bubble trail
            if t['bubble_timer'] % 5 == 0:
                self.wake_particles.append({
                    'x': t['x'] - 15,
                    'y': t['y'] + random.randint(-5, 5),
                    'life': 30,
                    'size': random.randint(2, 5)
                })
            
            if t['x'] > self.wall_x and self.wall_health > 0:
                self.wall_health -= 35
                self.torpedoes.remove(t)
                # Underwater explosion
                for _ in range(30):
                    self.explosions.append({
                        'x': self.wall_x,
                        'y': t['y'] + random.randint(-30, 30),
                        'vx': random.uniform(-4, 2),
                        'vy': random.uniform(-3, 3),
                        'life': random.randint(30, 60),
                        'size': random.randint(5, 15),
                        'type': 'water' if random.random() > 0.5 else 'fire'
                    })
        
        # Update wake particles
        for w in self.wake_particles[:]:
            w['y'] -= 0.3
            w['life'] -= 1
            if w['life'] <= 0:
                self.wake_particles.remove(w)
        
        # Update explosions
        for e in self.explosions[:]:
            e['x'] += e['vx']
            e['y'] += e['vy']
            if e['type'] == 'water':
                e['vy'] -= 0.05
            else:
                e['vy'] += 0.08
            e['life'] -= 1
            if e['life'] <= 0:
                self.explosions.remove(e)
        
        # Reset
        if self.x > WIDTH + 400:
            self.x = -350
            self.wall_health = 100
            self.torpedoes = []
            self.explosions = []
            self.wake_particles = []
        
    def draw(self, screen):
        ship_gray = (100, 105, 115)
        ship_dark = (60, 65, 75)
        
        cx = self.x
        cy = self.y
        
        # Hull
        hull_points = [
            (cx + self.length * 0.5, cy + self.height * 0.3),  # Bow
            (cx + self.length * 0.45, cy),
            (cx - self.length * 0.45, cy),
            (cx - self.length * 0.5, cy + self.height * 0.2),
            (cx - self.length * 0.5, cy + self.height * 0.5),
            (cx + self.length * 0.5, cy + self.height * 0.5),
        ]
        pygame.draw.polygon(screen, ship_gray, hull_points)
        
        # Deck line
        pygame.draw.line(screen, ship_dark,
                        (int(cx - self.length * 0.45), int(cy)),
                        (int(cx + self.length * 0.45), int(cy)), 3)
        
        # Superstructure
        super_x = cx - self.length * 0.1
        super_width = self.length * 0.25
        super_height = self.height * 0.8
        pygame.draw.rect(screen, ship_dark,
                        (super_x - super_width * 0.5, cy - super_height,
                         super_width, super_height))
        
        # Bridge windows
        for i in range(4):
            win_x = super_x - super_width * 0.3 + i * super_width * 0.2
            win_y = cy - super_height * 0.7
            pygame.draw.rect(screen, (150, 180, 200),
                           (int(win_x), int(win_y), int(8 * BG_SCALE), int(6 * BG_SCALE)))
        
        # Gun turrets
        for turret_pos in [-0.3, 0.2, 0.35]:
            turret_x = cx + self.length * turret_pos
            turret_y = cy - 10 * BG_SCALE
            pygame.draw.circle(screen, ship_dark, (int(turret_x), int(turret_y)), int(15 * BG_SCALE))
            # Gun barrels
            barrel_end_x = turret_x + 35 * BG_SCALE
            barrel_end_y = turret_y - 5 * BG_SCALE
            pygame.draw.line(screen, ship_dark, (int(turret_x), int(turret_y)),
                           (int(barrel_end_x), int(barrel_end_y)), int(4 * BG_SCALE))
        
        # Radar mast
        mast_x = super_x
        mast_y = cy - super_height - 30 * BG_SCALE
        pygame.draw.line(screen, ship_dark, (int(mast_x), int(cy - super_height)),
                        (int(mast_x), int(mast_y)), 2)
        pygame.draw.ellipse(screen, (80, 90, 100),
                          (int(mast_x - 12 * BG_SCALE), int(mast_y - 5 * BG_SCALE),
                           int(24 * BG_SCALE), int(10 * BG_SCALE)))
        
        # Wake behind ship
        for i in range(8):
            wake_x = cx - self.length * 0.5 - i * 25
            wake_y = cy + self.height * 0.4
            wake_color = (180, 200, 220)
            wake_width = 20 + i * 8
            pygame.draw.ellipse(screen, wake_color,
                              (int(wake_x - wake_width * 0.5), int(wake_y), int(wake_width), int(15 * BG_SCALE)))
        
        # Torpedoes
        for t in self.torpedoes:
            # Torpedo body
            pygame.draw.ellipse(screen, (60, 70, 60),
                              (int(t['x'] - 20), int(t['y'] - 5), 40, 10))
            # Propeller bubble
            pygame.draw.circle(screen, (200, 220, 240), (int(t['x'] - 22), int(t['y'])), 4)
        
        # Bubble wake
        for w in self.wake_particles:
            pygame.draw.circle(screen, (200, 220, 240), (int(w['x']), int(w['y'])), int(w['size'] * BG_SCALE))
        
        # Wall (underwater barrier)
        if self.wall_health > 0:
            wall_h = 180 * BG_SCALE * (self.wall_health / 100)
            pygame.draw.rect(screen, (70, 80, 90),
                           (self.wall_x, cy - wall_h * 0.3, 35 * BG_SCALE, wall_h))
        
        # Explosions
        for e in self.explosions:
            if e['type'] == 'water':
                e_color = (150, 200, 230)
            else:
                e_color = (255, random.randint(100, 180), 50)
            pygame.draw.circle(screen, e_color, (int(e['x']), int(e['y'])), int(e['size'] * BG_SCALE))


class BackgroundShuttle:
    """Space shuttle launch - right is up"""
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = 50  # Start at left (bottom in launch terms)
        self.y = BG_Y
        self.speed = 0
        self.acceleration = 0.015
        self.max_speed = 5
        self.angle = 0  # Points right
        self.length = 100 * BG_SCALE
        self.main_tank_attached = True
        self.boosters_attached = True
        self.booster_sep_x = WIDTH * 0.3
        self.tank_sep_x = WIDTH * 0.625  # 5/8 across
        self.flame_flicker = 0
        self.boosters = []  # Detached boosters
        self.main_tank = None  # Detached tank
        self.target_x = WIDTH * 0.85
        self.laser_charging = False
        self.laser_charge = 0
        self.laser_firing = False
        self.explosions = []
        self.target_health = 100
        self.mission_complete = False
        
    def update(self):
        if self.mission_complete:
            # Drift off screen
            self.x += 2
            if self.x > WIDTH + 200:
                self.reset()
            return
        
        # Accelerate
        if self.speed < self.max_speed:
            self.speed += self.acceleration
        
        self.x += self.speed
        
        self.flame_flicker += 0.4
        
        # Booster separation
        if self.x > self.booster_sep_x and self.boosters_attached:
            self.boosters_attached = False
            for i in [-1, 1]:
                self.boosters.append({
                    'x': self.x - 40 * BG_SCALE,
                    'y': self.y + i * 25 * BG_SCALE,
                    'vx': -1,
                    'vy': i * 0.8,
                    'angle': 0,
                    'spin': i * 0.02
                })
        
        # Main tank separation at 5/8
        if self.x > self.tank_sep_x and self.main_tank_attached:
            self.main_tank_attached = False
            self.main_tank = {
                'x': self.x - 30 * BG_SCALE,
                'y': self.y,
                'vx': self.speed * 0.5,
                'vy': 0.5,
                'angle': 0,
                'spin': 0.01
            }
        
        # Update detached boosters
        for b in self.boosters:
            b['x'] += b['vx']
            b['y'] += b['vy']
            b['vy'] += 0.03
            b['angle'] += b['spin']
        
        # Update detached tank
        if self.main_tank:
            self.main_tank['x'] += self.main_tank['vx']
            self.main_tank['y'] += self.main_tank['vy']
            self.main_tank['vy'] += 0.02
            self.main_tank['angle'] += self.main_tank['spin']
            self.main_tank['vx'] *= 0.99
        
        # Aim and charge laser after tank separation
        if not self.main_tank_attached and self.x > self.tank_sep_x + 50:
            if not self.laser_firing and self.target_health > 0:
                self.laser_charging = True
                self.laser_charge += 2
                if self.laser_charge >= 100:
                    self.laser_firing = True
                    self.laser_charge = 100
        
        # Fire laser
        if self.laser_firing and self.target_health > 0:
            self.target_health -= 5
            # Explosion particles at target
            if random.random() > 0.5:
                self.explosions.append({
                    'x': self.target_x + random.randint(-20, 20),
                    'y': self.y + random.randint(-40, 40),
                    'vx': random.uniform(-2, 2),
                    'vy': random.uniform(-2, 2),
                    'life': random.randint(15, 30),
                    'size': random.randint(5, 12)
                })
            if self.target_health <= 0:
                self.laser_firing = False
                # Big explosion
                for _ in range(40):
                    self.explosions.append({
                        'x': self.target_x,
                        'y': self.y,
                        'vx': random.uniform(-6, 6),
                        'vy': random.uniform(-6, 6),
                        'life': random.randint(30, 60),
                        'size': random.randint(8, 20)
                    })
                self.mission_complete = True
        
        # Update explosions
        for e in self.explosions[:]:
            e['x'] += e['vx']
            e['y'] += e['vy']
            e['life'] -= 1
            if e['life'] <= 0:
                self.explosions.remove(e)
        
    def draw(self, screen):
        shuttle_white = (230, 230, 235)
        shuttle_dark = (60, 60, 70)
        tank_orange = (210, 120, 50)
        booster_white = (220, 220, 225)
        
        cx = self.x
        cy = self.y
        
        # Draw detached boosters
        for b in self.boosters:
            bx, by = b['x'], b['y']
            pygame.draw.ellipse(screen, booster_white,
                              (int(bx - 25 * BG_SCALE), int(by - 8 * BG_SCALE),
                               int(50 * BG_SCALE), int(16 * BG_SCALE)))
        
        # Draw detached main tank
        if self.main_tank:
            tx, ty = self.main_tank['x'], self.main_tank['y']
            pygame.draw.ellipse(screen, tank_orange,
                              (int(tx - 40 * BG_SCALE), int(ty - 15 * BG_SCALE),
                               int(80 * BG_SCALE), int(30 * BG_SCALE)))
        
        # Main tank (attached)
        if self.main_tank_attached:
            tank_x = cx - 20 * BG_SCALE
            pygame.draw.ellipse(screen, tank_orange,
                              (int(tank_x - 45 * BG_SCALE), int(cy - 18 * BG_SCALE),
                               int(90 * BG_SCALE), int(36 * BG_SCALE)))
        
        # Boosters (attached)
        if self.boosters_attached:
            for i in [-1, 1]:
                bx = cx - 30 * BG_SCALE
                by = cy + i * 30 * BG_SCALE
                pygame.draw.ellipse(screen, booster_white,
                                  (int(bx - 30 * BG_SCALE), int(by - 10 * BG_SCALE),
                                   int(60 * BG_SCALE), int(20 * BG_SCALE)))
                # Booster flames
                flame_len = 25 + math.sin(self.flame_flicker + i) * 8
                pygame.draw.ellipse(screen, (255, 200, 50),
                                  (int(bx - 35 * BG_SCALE - flame_len), int(by - 8 * BG_SCALE),
                                   int(flame_len), int(16 * BG_SCALE)))
        
        # Shuttle orbiter
        shuttle_points = [
            (cx + self.length * 0.5, cy),  # Nose
            (cx + self.length * 0.3, cy - 12 * BG_SCALE),
            (cx - self.length * 0.4, cy - 15 * BG_SCALE),
            (cx - self.length * 0.5, cy - 12 * BG_SCALE),
            (cx - self.length * 0.5, cy + 12 * BG_SCALE),
            (cx - self.length * 0.4, cy + 15 * BG_SCALE),
            (cx + self.length * 0.3, cy + 12 * BG_SCALE),
        ]
        pygame.draw.polygon(screen, shuttle_white, shuttle_points)
        
        # Cockpit windows
        pygame.draw.ellipse(screen, (40, 50, 60),
                          (cx + self.length * 0.2, cy - 8 * BG_SCALE, 20 * BG_SCALE, 16 * BG_SCALE))
        
        # Wings
        pygame.draw.polygon(screen, shuttle_dark, [
            (cx - self.length * 0.2, cy + 10 * BG_SCALE),
            (cx - self.length * 0.45, cy + 40 * BG_SCALE),
            (cx - self.length * 0.5, cy + 35 * BG_SCALE),
            (cx - self.length * 0.35, cy + 10 * BG_SCALE)
        ])
        pygame.draw.polygon(screen, shuttle_dark, [
            (cx - self.length * 0.2, cy - 10 * BG_SCALE),
            (cx - self.length * 0.45, cy - 40 * BG_SCALE),
            (cx - self.length * 0.5, cy - 35 * BG_SCALE),
            (cx - self.length * 0.35, cy - 10 * BG_SCALE)
        ])
        
        # Tail
        pygame.draw.polygon(screen, shuttle_dark, [
            (cx - self.length * 0.35, cy - 12 * BG_SCALE),
            (cx - self.length * 0.5, cy - 35 * BG_SCALE),
            (cx - self.length * 0.55, cy - 30 * BG_SCALE),
            (cx - self.length * 0.45, cy - 12 * BG_SCALE)
        ])
        
        # Main engines flame (when tank attached or just after)
        if self.main_tank_attached or (self.main_tank and self.main_tank['x'] > cx - 100):
            flame_len = 40 + math.sin(self.flame_flicker * 1.3) * 12
            for i in range(3):
                eng_y = cy + (i - 1) * 8 * BG_SCALE
                pygame.draw.ellipse(screen, (255, 180, 80),
                                  (int(cx - self.length * 0.5 - flame_len - i * 5), int(eng_y - 6 * BG_SCALE),
                                   int(flame_len + i * 5), int(12 * BG_SCALE)))
        
        # OMS engines (after tank sep)
        if not self.main_tank_attached:
            for i in [-1, 1]:
                oms_x = cx - self.length * 0.45
                oms_y = cy + i * 10 * BG_SCALE
                pygame.draw.ellipse(screen, (100, 150, 255),
                                  (int(oms_x - 15), int(oms_y - 4), 15, 8))
        
        # Laser charge indicator
        if self.laser_charging and not self.laser_firing:
            charge_x = cx + self.length * 0.4
            charge_size = int(5 + self.laser_charge * 0.1)
            pygame.draw.circle(screen, (100, 200, 255), (int(charge_x), int(cy)), charge_size)
        
        # Laser beam
        if self.laser_firing and self.target_health > 0:
            laser_start_x = cx + self.length * 0.5
            pygame.draw.line(screen, (100, 200, 255),
                           (int(laser_start_x), int(cy)),
                           (int(self.target_x), int(cy)), 4)
            pygame.draw.line(screen, (200, 230, 255),
                           (int(laser_start_x), int(cy)),
                           (int(self.target_x), int(cy)), 2)
        
        # Target
        if self.target_health > 0:
            target_h = 120 * BG_SCALE * (self.target_health / 100)
            pygame.draw.rect(screen, (150, 50, 50),
                           (self.target_x - 15, cy - target_h * 0.5, 30 * BG_SCALE, target_h))
            # Target symbol
            pygame.draw.circle(screen, (255, 100, 100), (int(self.target_x), int(cy)), int(20 * BG_SCALE), 2)
            pygame.draw.line(screen, (255, 100, 100),
                           (int(self.target_x - 25), int(cy)), (int(self.target_x + 25), int(cy)), 2)
            pygame.draw.line(screen, (255, 100, 100),
                           (int(self.target_x), int(cy - 25)), (int(self.target_x), int(cy + 25)), 2)
        
        # Explosions
        for e in self.explosions:
            e_color = (255, random.randint(100, 200), 50)
            pygame.draw.circle(screen, e_color, (int(e['x']), int(e['y'])), int(e['size'] * BG_SCALE))


# Initialize background scenes
bg_whale = BackgroundWhale()
bg_tank = BackgroundTank()
bg_jet = BackgroundJet()
bg_battleship = BackgroundBattleship()
bg_shuttle = BackgroundShuttle()

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Rock structures - each rock is (x, y, width, height)
rocks = [
    pygame.Rect(100, 675, 200, 75),   # Half height
    pygame.Rect(350, 650, 180, 100),  # Half height
    pygame.Rect(600, 685, 150, 65),   # Half height
    pygame.Rect(900, 670, 220, 90),   # Half height
]

# Generate rock details ONCE (so they don't flicker)
rock_details = []
for rock in rocks:
    cracks = []
    for i in range(3):
        start_x = rock.x + random.randint(10, rock.width - 10)
        start_y = rock.y + random.randint(10, rock.height - 10)
        end_x = start_x + random.randint(-30, 30)
        end_y = start_y + random.randint(20, 50)
        cracks.append(((start_x, start_y), (end_x, end_y)))
    rock_details.append(cracks)

# Generate sand grain positions ONCE
sand_grains = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(700, HEIGHT)
    grain_color = (
        SAND_COLOR[0] + random.randint(-20, 20),
        SAND_COLOR[1] + random.randint(-20, 20),
        SAND_COLOR[2] + random.randint(-20, 20)
    )
    sand_grains.append((x, y, grain_color))

# Fish class


class Fish:
    def __init__(self, x, y, color, size=15, speed=2):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.base_speed = speed
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.is_herbivore = False
        self.breed_partner = None    # Assigned breeding partner
        self.breed_cooldown = 0    # Time until can breed again

    def find_nearest_food(self, food_list):
        """Find closest food particle"""
        nearest = None
        min_dist = 300  # Look for food from far away!
        for food in food_list:
            if not food.eaten:
                dist = math.sqrt((self.x - food.x)**2 + (self.y - food.y)**2)
                if dist < min_dist:
                    min_dist = dist
                    nearest = food
        return nearest

    def find_nearest_algae(self, algae_list):
        """Find closest algae patch"""
        nearest = None
        min_dist = 300  # Look for algae from far away!
        for algae in algae_list:
            dist = math.sqrt((self.x - algae.x)**2 + (self.y - algae.y)**2)
            if dist < min_dist:
                min_dist = dist
                nearest = algae
        return nearest

    def update(self, food_list, chemistry, algae_list):
        """Update fish position and movement"""
        # Adjust speed based on water quality
        self.speed = self.base_speed * chemistry.affects_fish_health()

        # Herbivores eat algae if in range
        if self.is_herbivore:
            for algae in algae_list:
                dist = math.sqrt((self.x - algae.x)**2 + (self.y - algae.y)**2)
                if dist < 40:
                    algae.shrink(3.0)

        # Non-herbivores eat food pellets if in range
        else:
            for food in food_list:
                if not food.eaten:
                    dist = math.sqrt((self.x - food.x)**2 +
                                     (self.y - food.y)**2)
                    if dist < self.size + 10:
                        food.eaten = True

        # Breeding - check if near partner
        self.breed_cooldown = max(0, self.breed_cooldown - 1)
        if self.breed_partner and self.breed_cooldown == 0:
            dist_to_partner = math.sqrt(
                (self.x - self.breed_partner.x)**2 +
                (self.y - self.breed_partner.y)**2
            )
            if dist_to_partner < 50:    # Close enough to breed
                # Spawn 3 feeder fish!
                baby_x = (self.x + self.breed_partner.x) / 2
                baby_y = (self.y + self.breed_partner.y) / 2

            # Spawn them with slight position variation
                for i in range(3):
                    offset_x = random.randint(-15, 15)
                    offset_y = random.randint(-15, 15)
                    feeder_fish_list.append(FeederFish(
                        baby_x + offset_x, baby_y + offset_y))

                self.breed_cooldown = 600    # 10 second cooldown
                self.breed_partner.breed_cooldown = 600

        # Fish actively seek their preferred food (but not when near edges)
        target = None
        near_boundary = (self.x < 80 or self.x > WIDTH - 80 or
                         self.y < 80 or self.y > 630)

        if not near_boundary:
            if self.is_herbivore:
                # Herbivores seek algae
                target = self.find_nearest_algae(algae_list)
            else:
                # Non-herbivores seek food pellets
                target = self.find_nearest_food(food_list)

        # If target found, swim toward it
        if target:
            dx = target.x - self.x
            dy = target.y - self.y
            dist_to_target = math.sqrt(dx**2 + dy**2)

            # Only turn toward target if not too close (prevents jittering)
            if dist_to_target > 30:
                target_angle = math.atan2(dy, dx)

                # Smoothly turn toward target
                angle_diff = target_angle - self.angle
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                while angle_diff < -math.pi:
                    angle_diff += 2 * math.pi
                self.angle += angle_diff * 0.15
            else:
                # Very close - just wander a bit
                self.angle += random.uniform(-0.02, 0.02)
        else:
            # No food nearby, wander normally
            self.angle += random.uniform(-0.05, 0.05)

        # Move in current direction
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Bounce off boundaries
        if self.x < 50:
            self.angle = random.uniform(-0.5, 0.5)
            self.x = 50
        elif self.x > WIDTH - 50:
            self.angle = random.uniform(2.6, 3.6)
            self.x = WIDTH - 50

        if self.y < 50:
            self.angle = random.uniform(-0.5, 0.5)
            self.y = 50
        elif self.y > 650:
            self.angle = random.uniform(2.6, 3.6)
            self.y = 650

    def draw(self, screen):
        """Draw the fish based on current style"""
        if fish_style == 0:
            self.draw_realistic(screen)
        elif fish_style == 1:
            self.draw_cartoon(screen)
        elif fish_style == 2:
            self.draw_pixel(screen)
        elif fish_style == 3:
            self.draw_tropical(screen)
        elif fish_style == 4:
            self.draw_army(screen)
        elif fish_style == 5:
            self.draw_airforce(screen)
        elif fish_style == 6:
            self.draw_spaceforce(screen)
        else:
            self.draw_navy(screen)

    def draw_realistic(self, screen):
        """Realistic fish with proper body shape and fins"""
        # Body - elongated ellipse
        body_length = self.size * 2
        body_height = self.size * 0.8
        
        # Calculate body center
        cx = self.x
        cy = self.y
        
        # Draw body as rotated ellipse using polygon points
        body_points = []
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            # Ellipse with tapered tail
            taper = 1.0 - 0.3 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            # Rotate by fish angle
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        # Darker shade for depth
        dark_color = (max(0, self.color[0] - 40), max(0, self.color[1] - 40), max(0, self.color[2] - 40))
        light_color = (min(255, self.color[0] + 30), min(255, self.color[1] + 30), min(255, self.color[2] + 30))
        
        pygame.draw.polygon(screen, self.color, body_points)
        
        # Dorsal fin (top)
        dorsal_base_x = cx - math.cos(self.angle) * self.size * 0.2
        dorsal_base_y = cy - math.sin(self.angle) * self.size * 0.2
        dorsal_tip_x = dorsal_base_x - math.sin(self.angle) * self.size * 0.6
        dorsal_tip_y = dorsal_base_y + math.cos(self.angle) * self.size * 0.6
        dorsal_back_x = cx - math.cos(self.angle) * self.size * 0.5
        dorsal_back_y = cy - math.sin(self.angle) * self.size * 0.5
        pygame.draw.polygon(screen, dark_color, [
            (dorsal_base_x, dorsal_base_y),
            (dorsal_tip_x, dorsal_tip_y),
            (dorsal_back_x, dorsal_back_y)
        ])
        
        # Tail fin
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        tail_top_x = tail_x - math.cos(self.angle + 0.5) * self.size * 0.7
        tail_top_y = tail_y - math.sin(self.angle + 0.5) * self.size * 0.7
        tail_bot_x = tail_x - math.cos(self.angle - 0.5) * self.size * 0.7
        tail_bot_y = tail_y - math.sin(self.angle - 0.5) * self.size * 0.7
        pygame.draw.polygon(screen, dark_color, [
            (tail_x, tail_y), (tail_top_x, tail_top_y), (tail_bot_x, tail_bot_y)
        ])
        
        # Pectoral fin (side)
        pec_x = cx + math.cos(self.angle) * self.size * 0.1
        pec_y = cy + math.sin(self.angle) * self.size * 0.1
        pec_tip_x = pec_x + math.sin(self.angle) * self.size * 0.4
        pec_tip_y = pec_y - math.cos(self.angle) * self.size * 0.4
        pygame.draw.polygon(screen, dark_color, [
            (pec_x, pec_y),
            (pec_tip_x, pec_tip_y),
            (pec_x - math.cos(self.angle) * self.size * 0.3, pec_y - math.sin(self.angle) * self.size * 0.3)
        ])
        
        # Eye with highlight
        eye_x = cx + math.cos(self.angle) * self.size * 0.5
        eye_y = cy + math.sin(self.angle) * self.size * 0.5
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), 4)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 2)
        
        # Subtle body highlight
        highlight_x = cx + math.cos(self.angle) * self.size * 0.2 - math.sin(self.angle) * self.size * 0.2
        highlight_y = cy + math.sin(self.angle) * self.size * 0.2 + math.cos(self.angle) * self.size * 0.2
        pygame.draw.circle(screen, light_color, (int(highlight_x), int(highlight_y)), int(self.size * 0.15))

    def draw_cartoon(self, screen):
        """Cute cartoon fish with big eyes and round body"""
        cx, cy = self.x, self.y
        
        # Round body
        body_radius = self.size * 0.8
        pygame.draw.circle(screen, self.color, (int(cx), int(cy)), int(body_radius))
        
        # Lighter belly
        belly_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
        belly_x = cx + math.sin(self.angle) * body_radius * 0.2
        belly_y = cy - math.cos(self.angle) * body_radius * 0.2
        pygame.draw.circle(screen, belly_color, (int(belly_x), int(belly_y)), int(body_radius * 0.5))
        
        # Big cute tail
        tail_x = cx - math.cos(self.angle) * body_radius
        tail_y = cy - math.sin(self.angle) * body_radius
        tail_points = [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.6) * self.size, tail_y - math.sin(self.angle + 0.6) * self.size),
            (tail_x - math.cos(self.angle) * self.size * 0.5, tail_y - math.sin(self.angle) * self.size * 0.5),
            (tail_x - math.cos(self.angle - 0.6) * self.size, tail_y - math.sin(self.angle - 0.6) * self.size),
        ]
        pygame.draw.polygon(screen, self.color, tail_points)
        
        # Cute dorsal fin
        dorsal_x = cx - math.sin(self.angle) * body_radius * 0.7
        dorsal_y = cy + math.cos(self.angle) * body_radius * 0.7
        pygame.draw.circle(screen, self.color, (int(dorsal_x), int(dorsal_y)), int(self.size * 0.4))
        
        # Big expressive eye (white with large pupil)
        eye_x = cx + math.cos(self.angle) * body_radius * 0.4
        eye_y = cy + math.sin(self.angle) * body_radius * 0.4
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), int(self.size * 0.4))
        # Pupil looking in movement direction
        pupil_x = eye_x + math.cos(self.angle) * self.size * 0.1
        pupil_y = eye_y + math.sin(self.angle) * self.size * 0.1
        pygame.draw.circle(screen, (0, 0, 0), (int(pupil_x), int(pupil_y)), int(self.size * 0.2))
        # Eye highlight
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x - 2), int(eye_y - 2)), 2)
        
        # Cute smile
        smile_x = cx + math.cos(self.angle) * body_radius * 0.5
        smile_y = cy + math.sin(self.angle) * body_radius * 0.5 + self.size * 0.2
        pygame.draw.arc(screen, (0, 0, 0), 
                       (int(smile_x - 4), int(smile_y - 4), 8, 8),
                       0.2, math.pi - 0.2, 2)

    def draw_pixel(self, screen):
        """Retro pixel art style fish"""
        cx, cy = int(self.x), int(self.y)
        pixel_size = max(3, int(self.size / 4))
        
        # Snap to pixel grid
        cx = (cx // pixel_size) * pixel_size
        cy = (cy // pixel_size) * pixel_size
        
        # Determine facing direction (simplified to 4 directions)
        if abs(math.cos(self.angle)) > abs(math.sin(self.angle)):
            facing = "right" if math.cos(self.angle) > 0 else "left"
        else:
            facing = "down" if math.sin(self.angle) > 0 else "up"
        
        # Pixel pattern for fish (relative positions)
        if facing == "right":
            pixels = [
                (0, 0), (1, 0), (2, 0),  # Body row 1
                (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1),  # Body row 2 with nose
                (0, 2), (1, 2), (2, 2),  # Body row 3
                (-2, 1),  # Tail
            ]
            eye_pos = (2, 1)
            tail_pixels = [(-2, 0), (-2, 1), (-2, 2), (-3, 1)]
        elif facing == "left":
            pixels = [
                (0, 0), (-1, 0), (-2, 0),
                (1, 1), (0, 1), (-1, 1), (-2, 1), (-3, 1),
                (0, 2), (-1, 2), (-2, 2),
            ]
            eye_pos = (-2, 1)
            tail_pixels = [(2, 0), (2, 1), (2, 2), (3, 1)]
        elif facing == "down":
            pixels = [
                (0, 0), (0, 1), (0, 2),
                (1, -1), (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2),
            ]
            eye_pos = (1, 2)
            tail_pixels = [(0, -2), (1, -2), (2, -2), (1, -3)]
        else:  # up
            pixels = [
                (0, 0), (0, -1), (0, -2),
                (1, 1), (1, 0), (1, -1), (1, -2), (1, -3),
                (2, 0), (2, -1), (2, -2),
            ]
            eye_pos = (1, -2)
            tail_pixels = [(0, 2), (1, 2), (2, 2), (1, 3)]
        
        # Draw tail
        dark_color = (max(0, self.color[0] - 60), max(0, self.color[1] - 60), max(0, self.color[2] - 60))
        for px, py in tail_pixels:
            rect = pygame.Rect(cx + px * pixel_size, cy + py * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(screen, dark_color, rect)
        
        # Draw body pixels
        for px, py in pixels:
            rect = pygame.Rect(cx + px * pixel_size, cy + py * pixel_size, pixel_size, pixel_size)
            pygame.draw.rect(screen, self.color, rect)
        
        # Draw eye
        eye_rect = pygame.Rect(cx + eye_pos[0] * pixel_size, cy + eye_pos[1] * pixel_size, pixel_size, pixel_size)
        pygame.draw.rect(screen, (0, 0, 0), eye_rect)

    def draw_tropical(self, screen):
        """Colorful tropical fish with stripes and patterns"""
        cx, cy = self.x, self.y
        body_length = self.size * 1.8
        body_height = self.size * 1.2
        
        # Generate stripe color (complementary)
        stripe_color = ((self.color[0] + 128) % 256, (self.color[1] + 128) % 256, (self.color[2] + 128) % 256)
        
        # Draw body as rotated ellipse
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            px = math.cos(angle) * body_length * 0.5
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, self.color, body_points)
        
        # Draw stripes
        for i in range(-2, 3):
            stripe_offset = i * self.size * 0.3
            stripe_start_x = cx + math.cos(self.angle) * stripe_offset - math.sin(self.angle) * body_height * 0.4
            stripe_start_y = cy + math.sin(self.angle) * stripe_offset + math.cos(self.angle) * body_height * 0.4
            stripe_end_x = cx + math.cos(self.angle) * stripe_offset + math.sin(self.angle) * body_height * 0.4
            stripe_end_y = cy + math.sin(self.angle) * stripe_offset - math.cos(self.angle) * body_height * 0.4
            pygame.draw.line(screen, stripe_color, 
                           (int(stripe_start_x), int(stripe_start_y)),
                           (int(stripe_end_x), int(stripe_end_y)), 3)
        
        # Fancy flowing tail
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        for t in range(3):
            spread = 0.4 + t * 0.3
            tail_top_x = tail_x - math.cos(self.angle + spread) * self.size * (1.2 - t * 0.2)
            tail_top_y = tail_y - math.sin(self.angle + spread) * self.size * (1.2 - t * 0.2)
            tail_bot_x = tail_x - math.cos(self.angle - spread) * self.size * (1.2 - t * 0.2)
            tail_bot_y = tail_y - math.sin(self.angle - spread) * self.size * (1.2 - t * 0.2)
            tail_color = stripe_color if t % 2 == 0 else self.color
            pygame.draw.polygon(screen, tail_color, [
                (tail_x, tail_y), (tail_top_x, tail_top_y), (tail_bot_x, tail_bot_y)
            ])
        
        # Elaborate dorsal fin
        for d in range(3):
            dorsal_x = cx - math.cos(self.angle) * self.size * (0.1 + d * 0.2)
            dorsal_y = cy - math.sin(self.angle) * self.size * (0.1 + d * 0.2)
            tip_x = dorsal_x - math.sin(self.angle) * self.size * (0.8 - d * 0.15)
            tip_y = dorsal_y + math.cos(self.angle) * self.size * (0.8 - d * 0.15)
            fin_color = stripe_color if d % 2 == 0 else self.color
            pygame.draw.line(screen, fin_color, (int(dorsal_x), int(dorsal_y)), (int(tip_x), int(tip_y)), 3)
        
        # Eye with colorful iris
        eye_x = cx + math.cos(self.angle) * self.size * 0.5
        eye_y = cy + math.sin(self.angle) * self.size * 0.5
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), 5)
        pygame.draw.circle(screen, stripe_color, (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 2)

    def draw_army(self, screen):
        """US Army themed fish with camo pattern"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.0
        body_height = self.size * 1.0
        
        # Army colors
        camo_colors = [(85, 107, 47), (107, 142, 35), (34, 49, 29), (154, 140, 105)]
        base_green = (85, 107, 47)  # Olive drab
        
        # Draw body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            taper = 1.0 - 0.3 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, base_green, body_points)
        
        # Camo pattern spots
        random.seed(int(self.x * 100 + self.y))  # Consistent pattern per fish
        for _ in range(8):
            spot_offset_x = random.uniform(-0.6, 0.4) * body_length
            spot_offset_y = random.uniform(-0.3, 0.3) * body_height
            spot_x = cx + spot_offset_x * math.cos(self.angle) - spot_offset_y * math.sin(self.angle)
            spot_y = cy + spot_offset_x * math.sin(self.angle) + spot_offset_y * math.cos(self.angle)
            spot_color = random.choice(camo_colors)
            spot_size = random.randint(3, 7)
            pygame.draw.circle(screen, spot_color, (int(spot_x), int(spot_y)), spot_size)
        random.seed()  # Reset seed
        
        # Tail fin
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        pygame.draw.polygon(screen, (34, 49, 29), [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.5) * self.size * 0.8, tail_y - math.sin(self.angle + 0.5) * self.size * 0.8),
            (tail_x - math.cos(self.angle - 0.5) * self.size * 0.8, tail_y - math.sin(self.angle - 0.5) * self.size * 0.8)
        ])
        
        # Dorsal fin
        dorsal_x = cx - math.cos(self.angle) * self.size * 0.1
        dorsal_y = cy - math.sin(self.angle) * self.size * 0.1
        dorsal_tip_x = dorsal_x - math.sin(self.angle) * self.size * 0.6
        dorsal_tip_y = dorsal_y + math.cos(self.angle) * self.size * 0.6
        pygame.draw.polygon(screen, (34, 49, 29), [
            (dorsal_x + math.cos(self.angle) * 5, dorsal_y + math.sin(self.angle) * 5),
            (dorsal_tip_x, dorsal_tip_y),
            (dorsal_x - math.cos(self.angle) * 8, dorsal_y - math.sin(self.angle) * 8)
        ])
        
        # Army star insignia
        star_x = cx + math.cos(self.angle) * self.size * 0.1
        star_y = cy + math.sin(self.angle) * self.size * 0.1
        star_size = self.size * 0.25
        self.draw_star(screen, star_x, star_y, star_size, (255, 255, 255))
        
        # Eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.6
        eye_y = cy + math.sin(self.angle) * self.size * 0.6
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 3)

    def draw_star(self, screen, x, y, size, color):
        """Helper to draw a 5-pointed star"""
        points = []
        for i in range(5):
            # Outer point
            angle = -math.pi/2 + (i * 2 * math.pi / 5)
            points.append((x + math.cos(angle) * size, y + math.sin(angle) * size))
            # Inner point
            angle += math.pi / 5
            points.append((x + math.cos(angle) * size * 0.4, y + math.sin(angle) * size * 0.4))
        pygame.draw.polygon(screen, color, points)

    def draw_airforce(self, screen):
        """US Air Force themed fish - sleek jet-inspired"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.2
        body_height = self.size * 0.7
        
        # Air Force colors
        af_blue = (0, 48, 143)
        af_silver = (192, 192, 210)
        af_white = (255, 255, 255)
        
        # Sleek jet-like body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            # More pointed nose
            taper = 1.0 - 0.5 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, af_silver, body_points)
        
        # Blue racing stripe down the middle
        stripe_start_x = cx + math.cos(self.angle) * body_length * 0.4
        stripe_start_y = cy + math.sin(self.angle) * body_length * 0.4
        stripe_end_x = cx - math.cos(self.angle) * body_length * 0.4
        stripe_end_y = cy - math.sin(self.angle) * body_length * 0.4
        pygame.draw.line(screen, af_blue, (int(stripe_start_x), int(stripe_start_y)), 
                        (int(stripe_end_x), int(stripe_end_y)), 4)
        
        # Delta wings
        wing_x = cx - math.cos(self.angle) * self.size * 0.2
        wing_y = cy - math.sin(self.angle) * self.size * 0.2
        # Top wing
        pygame.draw.polygon(screen, af_blue, [
            (wing_x, wing_y),
            (wing_x - math.cos(self.angle) * self.size * 0.6 - math.sin(self.angle) * self.size * 0.8,
             wing_y - math.sin(self.angle) * self.size * 0.6 + math.cos(self.angle) * self.size * 0.8),
            (wing_x - math.cos(self.angle) * self.size * 0.8, wing_y - math.sin(self.angle) * self.size * 0.8)
        ])
        # Bottom wing
        pygame.draw.polygon(screen, af_blue, [
            (wing_x, wing_y),
            (wing_x - math.cos(self.angle) * self.size * 0.6 + math.sin(self.angle) * self.size * 0.8,
             wing_y - math.sin(self.angle) * self.size * 0.6 - math.cos(self.angle) * self.size * 0.8),
            (wing_x - math.cos(self.angle) * self.size * 0.8, wing_y - math.sin(self.angle) * self.size * 0.8)
        ])
        
        # Tail fin (vertical stabilizer style)
        tail_x = cx - math.cos(self.angle) * body_length * 0.45
        tail_y = cy - math.sin(self.angle) * body_length * 0.45
        pygame.draw.polygon(screen, af_blue, [
            (tail_x, tail_y),
            (tail_x - math.sin(self.angle) * self.size * 0.7, tail_y + math.cos(self.angle) * self.size * 0.7),
            (tail_x - math.cos(self.angle) * self.size * 0.5, tail_y - math.sin(self.angle) * self.size * 0.5)
        ])
        
        # USAF roundel (simplified)
        roundel_x = cx + math.cos(self.angle) * self.size * 0.15
        roundel_y = cy + math.sin(self.angle) * self.size * 0.15
        pygame.draw.circle(screen, af_blue, (int(roundel_x), int(roundel_y)), int(self.size * 0.22))
        pygame.draw.circle(screen, af_white, (int(roundel_x), int(roundel_y)), int(self.size * 0.15))
        pygame.draw.circle(screen, (191, 10, 48), (int(roundel_x), int(roundel_y)), int(self.size * 0.08))
        
        # Cockpit
        cockpit_x = cx + math.cos(self.angle) * self.size * 0.55
        cockpit_y = cy + math.sin(self.angle) * self.size * 0.55
        pygame.draw.ellipse(screen, (100, 150, 200), 
                           (int(cockpit_x - 4), int(cockpit_y - 3), 8, 6))

    def draw_spaceforce(self, screen):
        """US Space Force themed - futuristic sci-fi look"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.0
        body_height = self.size * 0.9
        
        # Space Force colors
        sf_dark = (20, 20, 35)
        sf_silver = (180, 185, 200)
        sf_blue = (0, 70, 127)
        sf_glow = (100, 180, 255)
        
        # Futuristic angular body
        nose_x = cx + math.cos(self.angle) * body_length * 0.5
        nose_y = cy + math.sin(self.angle) * body_length * 0.5
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        top_x = cx - math.sin(self.angle) * body_height * 0.5
        top_y = cy + math.cos(self.angle) * body_height * 0.5
        bot_x = cx + math.sin(self.angle) * body_height * 0.5
        bot_y = cy - math.cos(self.angle) * body_height * 0.5
        
        # Main hull
        pygame.draw.polygon(screen, sf_dark, [
            (nose_x, nose_y), (top_x, top_y), (tail_x, tail_y), (bot_x, bot_y)
        ])
        
        # Silver trim lines
        pygame.draw.line(screen, sf_silver, (int(nose_x), int(nose_y)), (int(tail_x), int(tail_y)), 2)
        mid_top_x = (nose_x + top_x) / 2
        mid_top_y = (nose_y + top_y) / 2
        mid_bot_x = (nose_x + bot_x) / 2
        mid_bot_y = (nose_y + bot_y) / 2
        pygame.draw.line(screen, sf_silver, (int(mid_top_x), int(mid_top_y)), (int(mid_bot_x), int(mid_bot_y)), 1)
        
        # Engine glow effect
        glow_x = tail_x - math.cos(self.angle) * 5
        glow_y = tail_y - math.sin(self.angle) * 5
        for i in range(3):
            glow_size = (3 - i) * 3
            glow_alpha = 150 - i * 40
            pygame.draw.circle(screen, sf_glow, (int(glow_x - i * math.cos(self.angle) * 3), 
                                                  int(glow_y - i * math.sin(self.angle) * 3)), glow_size)
        
        # Dorsal fin (antenna style)
        ant_x = cx - math.sin(self.angle) * self.size * 0.8
        ant_y = cy + math.cos(self.angle) * self.size * 0.8
        pygame.draw.line(screen, sf_silver, (int(cx), int(cy)), (int(ant_x), int(ant_y)), 2)
        pygame.draw.circle(screen, sf_glow, (int(ant_x), int(ant_y)), 3)
        
        # Delta symbol / arrow emblem
        emblem_x = cx + math.cos(self.angle) * self.size * 0.1
        emblem_y = cy + math.sin(self.angle) * self.size * 0.1
        delta_size = self.size * 0.2
        pygame.draw.polygon(screen, sf_silver, [
            (emblem_x + math.cos(self.angle) * delta_size, emblem_y + math.sin(self.angle) * delta_size),
            (emblem_x - math.sin(self.angle) * delta_size * 0.6, emblem_y + math.cos(self.angle) * delta_size * 0.6),
            (emblem_x + math.sin(self.angle) * delta_size * 0.6, emblem_y - math.cos(self.angle) * delta_size * 0.6)
        ])
        
        # Cockpit visor
        visor_x = cx + math.cos(self.angle) * self.size * 0.5
        visor_y = cy + math.sin(self.angle) * self.size * 0.5
        pygame.draw.ellipse(screen, sf_blue, (int(visor_x - 5), int(visor_y - 3), 10, 6))
        pygame.draw.ellipse(screen, sf_glow, (int(visor_x - 3), int(visor_y - 2), 4, 3))

    def draw_navy(self, screen):
        """US Navy themed fish - naval ship inspired"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.0
        body_height = self.size * 0.85
        
        # Navy colors
        navy_blue = (0, 0, 80)
        navy_gray = (128, 128, 140)
        navy_white = (255, 255, 255)
        navy_gold = (255, 215, 0)
        
        # Ship hull-like body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            # Flat bottom, curved top like a ship hull
            if math.sin(angle) > 0:
                py_mult = 0.4  # Flatter bottom
            else:
                py_mult = 0.6  # More curved top
            taper = 1.0 - 0.35 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * py_mult
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, navy_gray, body_points)
        
        # Deck line
        deck_start_x = cx + math.cos(self.angle) * body_length * 0.35
        deck_start_y = cy + math.sin(self.angle) * body_length * 0.35
        deck_end_x = cx - math.cos(self.angle) * body_length * 0.35
        deck_end_y = cy - math.sin(self.angle) * body_length * 0.35
        pygame.draw.line(screen, navy_blue, (int(deck_start_x), int(deck_start_y)), 
                        (int(deck_end_x), int(deck_end_y)), 3)
        
        # Conning tower / bridge
        tower_x = cx - math.cos(self.angle) * self.size * 0.1
        tower_y = cy - math.sin(self.angle) * self.size * 0.1
        tower_top_x = tower_x - math.sin(self.angle) * self.size * 0.5
        tower_top_y = tower_y + math.cos(self.angle) * self.size * 0.5
        pygame.draw.polygon(screen, navy_blue, [
            (tower_x - math.cos(self.angle) * 6, tower_y - math.sin(self.angle) * 6),
            (tower_x + math.cos(self.angle) * 6, tower_y + math.sin(self.angle) * 6),
            (tower_top_x + math.cos(self.angle) * 4, tower_top_y + math.sin(self.angle) * 4),
            (tower_top_x - math.cos(self.angle) * 4, tower_top_y - math.sin(self.angle) * 4)
        ])
        
        # Tail (propeller area)
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        pygame.draw.polygon(screen, navy_blue, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.6) * self.size * 0.6, tail_y - math.sin(self.angle + 0.6) * self.size * 0.6),
            (tail_x - math.cos(self.angle - 0.6) * self.size * 0.6, tail_y - math.sin(self.angle - 0.6) * self.size * 0.6)
        ])
        
        # Anchor emblem
        anchor_x = cx + math.cos(self.angle) * self.size * 0.2
        anchor_y = cy + math.sin(self.angle) * self.size * 0.2
        # Anchor shaft
        pygame.draw.line(screen, navy_gold, 
                        (int(anchor_x - math.sin(self.angle) * 6), int(anchor_y + math.cos(self.angle) * 6)),
                        (int(anchor_x + math.sin(self.angle) * 6), int(anchor_y - math.cos(self.angle) * 6)), 2)
        # Anchor crossbar
        pygame.draw.line(screen, navy_gold,
                        (int(anchor_x - math.cos(self.angle) * 4 - math.sin(self.angle) * 3), 
                         int(anchor_y - math.sin(self.angle) * 4 + math.cos(self.angle) * 3)),
                        (int(anchor_x + math.cos(self.angle) * 4 - math.sin(self.angle) * 3),
                         int(anchor_y + math.sin(self.angle) * 4 + math.cos(self.angle) * 3)), 2)
        # Anchor flukes
        pygame.draw.line(screen, navy_gold,
                        (int(anchor_x + math.sin(self.angle) * 6), int(anchor_y - math.cos(self.angle) * 6)),
                        (int(anchor_x - math.cos(self.angle) * 4 + math.sin(self.angle) * 6),
                         int(anchor_y - math.sin(self.angle) * 4 - math.cos(self.angle) * 6)), 2)
        pygame.draw.line(screen, navy_gold,
                        (int(anchor_x + math.sin(self.angle) * 6), int(anchor_y - math.cos(self.angle) * 6)),
                        (int(anchor_x + math.cos(self.angle) * 4 + math.sin(self.angle) * 6),
                         int(anchor_y + math.sin(self.angle) * 4 - math.cos(self.angle) * 6)), 2)
        
        # Porthole eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.55
        eye_y = cy + math.sin(self.angle) * self.size * 0.55
        pygame.draw.circle(screen, navy_white, (int(eye_x), int(eye_y)), 4)
        pygame.draw.circle(screen, navy_blue, (int(eye_x), int(eye_y)), 4, 1)
        pygame.draw.circle(screen, (50, 50, 60), (int(eye_x), int(eye_y)), 2)

# Feeder Fish (offspring from breeders)


class FeederFish:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 50, 50)    # Red
        self.size = 10
        self.base_speed = 2    # Faster than predators initially
        self.speed = 2
        self.angle = random.uniform(0, 2 * math.pi)
        self.invulnerable_timer = 300   # 5 seconds at 60 FPS before targetable
        self.being_chased = False
        self.chase_fatigue = 0    # Increases when being chased

    def update(self, predator_list):
        """Update feeder fish movement"""
        # Count down invulnerability
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

        # Check if being chased
        self.being_chased = False
        for predator in predator_list:
            if predator.target == self:
                self.being_chased = True
                break

        # Speed decay when being chased
        if self.being_chased:
            self.chase_fatigue += 0.07
            self.speed = max(2, self.base_speed - self.chase_fatigue)
        else:
            # Recover slowly when not chased
            self.chase_fatigue = max(0, self.chase_fatigue - 0.01)
            self.speed = self.base_speed - self.chase_fatigue

        # Simple wandering
        self.angle += random.uniform(-0.08, 0.08)

        # Move
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Bounce off boundaries
        if self.x < 50:
            self.angle = random.uniform(-0.5, 0.5)
            self.x = 50
        elif self.x > WIDTH - 50:
            self.angle = random.uniform(2.6, 3.6)
            self.x = WIDTH - 50
        if self.y < 50:
            self.angle = random.uniform(-0.5, 0.5)
            self.y = 50
        elif self.y > 650:
            self.angle = random.uniform(2.6, 3.6)
            self.y = 650

    def is_targetable(self):
        """Can only be targeted after invulnerability timer expires"""
        return self.invulnerable_timer <= 0

    def draw(self, screen):
        """Draw feeder fish based on current style"""
        # Handle invulnerability flash
        if self.invulnerable_timer > 0 and self.invulnerable_timer % 20 < 10:
            display_color = (255, 255, 255)
        else:
            display_color = self.color
        
        if fish_style == 0:
            self.draw_realistic(screen, display_color)
        elif fish_style == 1:
            self.draw_cartoon(screen, display_color)
        elif fish_style == 2:
            self.draw_pixel(screen, display_color)
        elif fish_style == 3:
            self.draw_tropical(screen, display_color)
        elif fish_style == 4:
            self.draw_army(screen, display_color)
        elif fish_style == 5:
            self.draw_airforce(screen, display_color)
        elif fish_style == 6:
            self.draw_spaceforce(screen, display_color)
        else:
            self.draw_navy(screen, display_color)

    def draw_realistic(self, screen, color):
        """Realistic small fish"""
        cx, cy = self.x, self.y
        body_length = self.size * 1.8
        body_height = self.size * 0.6
        
        # Body ellipse
        body_points = []
        for i in range(16):
            angle = (i / 16) * 2 * math.pi
            taper = 1.0 - 0.3 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        dark_color = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
        pygame.draw.polygon(screen, color, body_points)
        
        # Small tail
        tail_x = cx - math.cos(self.angle) * body_length * 0.4
        tail_y = cy - math.sin(self.angle) * body_length * 0.4
        pygame.draw.polygon(screen, dark_color, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.5) * self.size * 0.5, tail_y - math.sin(self.angle + 0.5) * self.size * 0.5),
            (tail_x - math.cos(self.angle - 0.5) * self.size * 0.5, tail_y - math.sin(self.angle - 0.5) * self.size * 0.5)
        ])
        
        # Eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.4
        eye_y = cy + math.sin(self.angle) * self.size * 0.4
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 1)

    def draw_cartoon(self, screen, color):
        """Cute small cartoon fish"""
        cx, cy = self.x, self.y
        body_radius = self.size * 0.7
        
        pygame.draw.circle(screen, color, (int(cx), int(cy)), int(body_radius))
        
        # Tail
        tail_x = cx - math.cos(self.angle) * body_radius
        tail_y = cy - math.sin(self.angle) * body_radius
        pygame.draw.circle(screen, color, (int(tail_x), int(tail_y)), int(self.size * 0.4))
        
        # Big eye
        eye_x = cx + math.cos(self.angle) * body_radius * 0.3
        eye_y = cy + math.sin(self.angle) * body_radius * 0.3
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), int(self.size * 0.35))
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), int(self.size * 0.15))
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x - 1), int(eye_y - 1)), 2)

    def draw_pixel(self, screen, color):
        """Pixel art small fish"""
        cx, cy = int(self.x), int(self.y)
        pixel_size = max(2, int(self.size / 3))
        cx = (cx // pixel_size) * pixel_size
        cy = (cy // pixel_size) * pixel_size
        
        facing_right = math.cos(self.angle) > 0
        
        if facing_right:
            pixels = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
            tail = [(-1, 0), (-1, 1)]
            eye = (2, 0)
        else:
            pixels = [(0, 0), (-1, 0), (-2, 0), (0, 1), (-1, 1)]
            tail = [(1, 0), (1, 1)]
            eye = (-2, 0)
        
        dark_color = (max(0, color[0] - 60), max(0, color[1] - 60), max(0, color[2] - 60))
        for px, py in tail:
            pygame.draw.rect(screen, dark_color, (cx + px * pixel_size, cy + py * pixel_size, pixel_size, pixel_size))
        for px, py in pixels:
            pygame.draw.rect(screen, color, (cx + px * pixel_size, cy + py * pixel_size, pixel_size, pixel_size))
        pygame.draw.rect(screen, (0, 0, 0), (cx + eye[0] * pixel_size, cy + eye[1] * pixel_size, pixel_size, pixel_size))

    def draw_tropical(self, screen, color):
        """Small tropical fish with pattern"""
        cx, cy = self.x, self.y
        body_length = self.size * 1.5
        body_height = self.size * 0.8
        
        stripe_color = ((color[0] + 128) % 256, (color[1] + 128) % 256, (color[2] + 128) % 256)
        
        # Body
        body_points = []
        for i in range(16):
            angle = (i / 16) * 2 * math.pi
            px = math.cos(angle) * body_length * 0.5
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, color, body_points)
        
        # Single stripe
        stripe_start_x = cx - math.sin(self.angle) * body_height * 0.3
        stripe_start_y = cy + math.cos(self.angle) * body_height * 0.3
        stripe_end_x = cx + math.sin(self.angle) * body_height * 0.3
        stripe_end_y = cy - math.cos(self.angle) * body_height * 0.3
        pygame.draw.line(screen, stripe_color, (int(stripe_start_x), int(stripe_start_y)), (int(stripe_end_x), int(stripe_end_y)), 2)
        
        # Tail
        tail_x = cx - math.cos(self.angle) * body_length * 0.4
        tail_y = cy - math.sin(self.angle) * body_length * 0.4
        pygame.draw.polygon(screen, stripe_color, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.4) * self.size * 0.6, tail_y - math.sin(self.angle + 0.4) * self.size * 0.6),
            (tail_x - math.cos(self.angle - 0.4) * self.size * 0.6, tail_y - math.sin(self.angle - 0.4) * self.size * 0.6)
        ])
        
        # Eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.4
        eye_y = cy + math.sin(self.angle) * self.size * 0.4
        pygame.draw.circle(screen, (255, 255, 255), (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 1)

    def draw_army(self, screen, color):
        """Army themed feeder fish"""
        cx, cy = self.x, self.y
        camo_colors = [(85, 107, 47), (107, 142, 35), (34, 49, 29), (154, 140, 105)]
        base_green = (85, 107, 47)
        
        # Body
        body_points = []
        for i in range(16):
            angle = (i / 16) * 2 * math.pi
            taper = 1.0 - 0.3 * max(0, math.cos(angle))
            px = math.cos(angle) * self.size * 0.9 * taper
            py = math.sin(angle) * self.size * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, base_green, body_points)
        
        # Small camo spots
        random.seed(int(self.x * 100 + self.y))
        for _ in range(4):
            spot_x = cx + random.uniform(-0.5, 0.3) * self.size
            spot_y = cy + random.uniform(-0.3, 0.3) * self.size
            pygame.draw.circle(screen, random.choice(camo_colors), (int(spot_x), int(spot_y)), 2)
        random.seed()
        
        # Tail
        tail_x = cx - math.cos(self.angle) * self.size * 0.8
        tail_y = cy - math.sin(self.angle) * self.size * 0.8
        pygame.draw.polygon(screen, (34, 49, 29), [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.5) * self.size * 0.4, tail_y - math.sin(self.angle + 0.5) * self.size * 0.4),
            (tail_x - math.cos(self.angle - 0.5) * self.size * 0.4, tail_y - math.sin(self.angle - 0.5) * self.size * 0.4)
        ])
        
        # Eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.4
        eye_y = cy + math.sin(self.angle) * self.size * 0.4
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 2)

    def draw_airforce(self, screen, color):
        """Air Force themed feeder fish"""
        cx, cy = self.x, self.y
        af_silver = (192, 192, 210)
        af_blue = (0, 48, 143)
        
        # Sleek body
        body_points = []
        for i in range(16):
            angle = (i / 16) * 2 * math.pi
            taper = 1.0 - 0.4 * max(0, math.cos(angle))
            px = math.cos(angle) * self.size * 1.0 * taper
            py = math.sin(angle) * self.size * 0.4
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, af_silver, body_points)
        
        # Blue stripe
        pygame.draw.line(screen, af_blue, 
                        (int(cx + math.cos(self.angle) * self.size * 0.5), int(cy + math.sin(self.angle) * self.size * 0.5)),
                        (int(cx - math.cos(self.angle) * self.size * 0.5), int(cy - math.sin(self.angle) * self.size * 0.5)), 2)
        
        # Small wings
        wing_x = cx - math.cos(self.angle) * self.size * 0.2
        wing_y = cy - math.sin(self.angle) * self.size * 0.2
        pygame.draw.polygon(screen, af_blue, [
            (wing_x, wing_y),
            (wing_x - math.sin(self.angle) * self.size * 0.5, wing_y + math.cos(self.angle) * self.size * 0.5),
            (wing_x - math.cos(self.angle) * self.size * 0.3, wing_y - math.sin(self.angle) * self.size * 0.3)
        ])
        
        # Cockpit
        eye_x = cx + math.cos(self.angle) * self.size * 0.4
        eye_y = cy + math.sin(self.angle) * self.size * 0.4
        pygame.draw.circle(screen, (100, 150, 200), (int(eye_x), int(eye_y)), 3)

    def draw_spaceforce(self, screen, color):
        """Space Force themed feeder fish"""
        cx, cy = self.x, self.y
        sf_dark = (20, 20, 35)
        sf_silver = (180, 185, 200)
        sf_glow = (100, 180, 255)
        
        # Angular body
        nose_x = cx + math.cos(self.angle) * self.size * 0.8
        nose_y = cy + math.sin(self.angle) * self.size * 0.8
        tail_x = cx - math.cos(self.angle) * self.size * 0.6
        tail_y = cy - math.sin(self.angle) * self.size * 0.6
        top_x = cx - math.sin(self.angle) * self.size * 0.4
        top_y = cy + math.cos(self.angle) * self.size * 0.4
        bot_x = cx + math.sin(self.angle) * self.size * 0.4
        bot_y = cy - math.cos(self.angle) * self.size * 0.4
        
        pygame.draw.polygon(screen, sf_dark, [(nose_x, nose_y), (top_x, top_y), (tail_x, tail_y), (bot_x, bot_y)])
        pygame.draw.line(screen, sf_silver, (int(nose_x), int(nose_y)), (int(tail_x), int(tail_y)), 1)
        
        # Engine glow
        pygame.draw.circle(screen, sf_glow, (int(tail_x), int(tail_y)), 3)
        
        # Cockpit
        pygame.draw.circle(screen, sf_glow, (int(cx + math.cos(self.angle) * self.size * 0.3), 
                                             int(cy + math.sin(self.angle) * self.size * 0.3)), 2)

    def draw_navy(self, screen, color):
        """Navy themed feeder fish"""
        cx, cy = self.x, self.y
        navy_gray = (128, 128, 140)
        navy_blue = (0, 0, 80)
        navy_white = (255, 255, 255)
        
        # Hull body
        body_points = []
        for i in range(16):
            angle = (i / 16) * 2 * math.pi
            py_mult = 0.35 if math.sin(angle) > 0 else 0.5
            taper = 1.0 - 0.3 * max(0, math.cos(angle))
            px = math.cos(angle) * self.size * 0.9 * taper
            py = math.sin(angle) * self.size * py_mult
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, navy_gray, body_points)
        
        # Deck line
        pygame.draw.line(screen, navy_blue,
                        (int(cx + math.cos(self.angle) * self.size * 0.4), int(cy + math.sin(self.angle) * self.size * 0.4)),
                        (int(cx - math.cos(self.angle) * self.size * 0.4), int(cy - math.sin(self.angle) * self.size * 0.4)), 2)
        
        # Tail
        tail_x = cx - math.cos(self.angle) * self.size * 0.7
        tail_y = cy - math.sin(self.angle) * self.size * 0.7
        pygame.draw.polygon(screen, navy_blue, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.5) * self.size * 0.4, tail_y - math.sin(self.angle + 0.5) * self.size * 0.4),
            (tail_x - math.cos(self.angle - 0.5) * self.size * 0.4, tail_y - math.sin(self.angle - 0.5) * self.size * 0.4)
        ])
        
        # Porthole
        eye_x = cx + math.cos(self.angle) * self.size * 0.35
        eye_y = cy + math.sin(self.angle) * self.size * 0.35
        pygame.draw.circle(screen, navy_white, (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, navy_blue, (int(eye_x), int(eye_y)), 3, 1)

# Predator Fish


class PredatorFish:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (30, 30, 30)    # Dark gray/black
        self.size = 25    # Larger than other fish
        self.speed = 2.5    # Slower than feeder fish initially
        self.angle = random.uniform(0, 2 * math.pi)
        self.target = None    # Current feeder fish target

    def find_target(self, feeder_list, other_predators):
        """Find 3rd closest targetable feeder fish that isn't already being chased"""
        if self.target and self.target in feeder_list:
            # Keep current target if still valid
            return

        # Get list of fish already being chased by other predators
        claimed_targets = [
            pred.target for pred in other_predators if pred != self and pred.target]

        # Find all unclaimed, targetable feeders with their distances
        candidates = []
        for feeder in feeder_list:
            if feeder.is_targetable() and feeder not in claimed_targets:
                dist = math.sqrt((self.x - feeder.x)**2 +
                                 (self.y - feeder.y)**2)
                if dist < 400:  # Within detection range
                    candidates.append((dist, feeder))

        # Sort by distance (closest first)
        candidates.sort(key=lambda x: x[0])

        # Target the 3rd closest (index 2), or farthest if fewer than 3
        if len(candidates) >= 3:
            self.target = candidates[2][1]  # 3rd closest
        elif len(candidates) > 0:
            self.target = candidates[-1][1]  # Farthest available
        else:
            self.target = None

    def update(self, feeder_list, other_predators):
        """Update predator movement"""
        self.find_target(feeder_list, other_predators)

        if self.target:
            # Chase target
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist > 15:
                # Turn toward target
                target_angle = math.atan2(dy, dx)
                angle_diff = target_angle - self.angle
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                while angle_diff < -math.pi:
                    angle_diff += 2 * math.pi
                self.angle += angle_diff * 0.12

            # Check if caught prey
            if dist < self.size:
                return self.target    # Return caught fish to remove it
        else:
            # Wander when no target
            self.angle += random.uniform(-0.05, 0.05)

        # Move
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Bounce off boundaries
        if self.x < 50:
            self.angle = random.uniform(-0.5, 0.5)
            self.x = 50
        elif self.x > WIDTH - 50:
            self.angle = random.uniform(2.6, 3.6)
            self.x = WIDTH - 50
        if self.y < 50:
            self.angle = random.uniform(-0.5, 0.5)
            self.y = 50
        elif self.y > 650:
            self.angle = random.uniform(2.6, 3.6)
            self.y = 650

        return None    # No catch

    def draw(self, screen):
        """Draw predator fish based on current style"""
        if fish_style == 0:
            self.draw_realistic(screen)
        elif fish_style == 1:
            self.draw_cartoon(screen)
        elif fish_style == 2:
            self.draw_pixel(screen)
        elif fish_style == 3:
            self.draw_tropical(screen)
        elif fish_style == 4:
            self.draw_army(screen)
        elif fish_style == 5:
            self.draw_airforce(screen)
        elif fish_style == 6:
            self.draw_spaceforce(screen)
        else:
            self.draw_navy(screen)

    def draw_realistic(self, screen):
        """Realistic menacing predator"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.5
        body_height = self.size * 0.9
        
        # Sleek predator body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            # Sharper nose taper
            taper = 1.0 - 0.5 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        dark_color = (20, 20, 25)
        light_color = (50, 50, 55)
        pygame.draw.polygon(screen, self.color, body_points)
        
        # Shark-like dorsal fin
        dorsal_x = cx - math.cos(self.angle) * self.size * 0.2
        dorsal_y = cy - math.sin(self.angle) * self.size * 0.2
        dorsal_tip_x = dorsal_x - math.sin(self.angle) * self.size * 1.0
        dorsal_tip_y = dorsal_y + math.cos(self.angle) * self.size * 1.0
        dorsal_back_x = cx - math.cos(self.angle) * self.size * 0.8
        dorsal_back_y = cy - math.sin(self.angle) * self.size * 0.8
        pygame.draw.polygon(screen, dark_color, [
            (dorsal_x, dorsal_y), (dorsal_tip_x, dorsal_tip_y), (dorsal_back_x, dorsal_back_y)
        ])
        
        # Powerful tail
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        pygame.draw.polygon(screen, dark_color, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.6) * self.size * 1.0, tail_y - math.sin(self.angle + 0.6) * self.size * 1.0),
            (tail_x - math.cos(self.angle) * self.size * 0.3, tail_y - math.sin(self.angle) * self.size * 0.3),
            (tail_x - math.cos(self.angle - 0.6) * self.size * 1.0, tail_y - math.sin(self.angle - 0.6) * self.size * 1.0)
        ])
        
        # Menacing red eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.7
        eye_y = cy + math.sin(self.angle) * self.size * 0.7
        pygame.draw.circle(screen, (255, 50, 0), (int(eye_x), int(eye_y)), 4)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 2)
        
        # Gill slits
        for i in range(3):
            gill_x = cx + math.cos(self.angle) * self.size * (0.2 - i * 0.15)
            gill_y = cy + math.sin(self.angle) * self.size * (0.2 - i * 0.15)
            gill_end_x = gill_x + math.sin(self.angle) * self.size * 0.2
            gill_end_y = gill_y - math.cos(self.angle) * self.size * 0.2
            pygame.draw.line(screen, dark_color, (int(gill_x), int(gill_y)), (int(gill_end_x), int(gill_end_y)), 2)

    def draw_cartoon(self, screen):
        """Cartoon villain predator"""
        cx, cy = self.x, self.y
        body_radius = self.size * 1.0
        
        # Angry oval body
        body_rect = pygame.Rect(cx - body_radius * 1.3, cy - body_radius * 0.7, body_radius * 2.6, body_radius * 1.4)
        
        # Rotate body points
        body_points = []
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            px = math.cos(angle) * body_radius * 1.3
            py = math.sin(angle) * body_radius * 0.7
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, self.color, body_points)
        
        # Spiky dorsal fin
        for i in range(3):
            spike_x = cx - math.cos(self.angle) * self.size * (0.3 * i)
            spike_y = cy - math.sin(self.angle) * self.size * (0.3 * i)
            spike_tip_x = spike_x - math.sin(self.angle) * self.size * (0.7 - i * 0.15)
            spike_tip_y = spike_y + math.cos(self.angle) * self.size * (0.7 - i * 0.15)
            pygame.draw.polygon(screen, (20, 20, 30), [
                (spike_x - math.cos(self.angle) * 3, spike_y - math.sin(self.angle) * 3),
                (spike_tip_x, spike_tip_y),
                (spike_x + math.cos(self.angle) * 3, spike_y + math.sin(self.angle) * 3)
            ])
        
        # Big tail
        tail_x = cx - math.cos(self.angle) * body_radius * 1.2
        tail_y = cy - math.sin(self.angle) * body_radius * 1.2
        pygame.draw.polygon(screen, self.color, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.7) * self.size * 0.9, tail_y - math.sin(self.angle + 0.7) * self.size * 0.9),
            (tail_x - math.cos(self.angle - 0.7) * self.size * 0.9, tail_y - math.sin(self.angle - 0.7) * self.size * 0.9)
        ])
        
        # Angry eyes
        eye_x = cx + math.cos(self.angle) * body_radius * 0.5
        eye_y = cy + math.sin(self.angle) * body_radius * 0.5
        pygame.draw.circle(screen, (255, 255, 200), (int(eye_x), int(eye_y)), int(self.size * 0.35))
        pygame.draw.circle(screen, (255, 0, 0), (int(eye_x), int(eye_y)), int(self.size * 0.2))
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), int(self.size * 0.1))
        
        # Angry eyebrow
        brow_start_x = eye_x - math.cos(self.angle + 0.5) * self.size * 0.4
        brow_start_y = eye_y - math.sin(self.angle + 0.5) * self.size * 0.4
        brow_end_x = eye_x + math.cos(self.angle - 0.3) * self.size * 0.3
        brow_end_y = eye_y + math.sin(self.angle - 0.3) * self.size * 0.3 - self.size * 0.3
        pygame.draw.line(screen, (0, 0, 0), (int(brow_start_x), int(brow_start_y - 5)), (int(brow_end_x), int(brow_end_y - 5)), 3)
        
        # Mean mouth with teeth
        mouth_x = cx + math.cos(self.angle) * body_radius * 0.8
        mouth_y = cy + math.sin(self.angle) * body_radius * 0.8 + 5
        pygame.draw.line(screen, (0, 0, 0), (int(mouth_x - 8), int(mouth_y)), (int(mouth_x + 5), int(mouth_y + 3)), 2)

    def draw_pixel(self, screen):
        """Pixel art predator"""
        cx, cy = int(self.x), int(self.y)
        pixel_size = max(4, int(self.size / 4))
        cx = (cx // pixel_size) * pixel_size
        cy = (cy // pixel_size) * pixel_size
        
        facing_right = math.cos(self.angle) > 0
        
        if facing_right:
            body = [
                (0, 0), (1, 0), (2, 0), (3, 0),
                (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                (0, 2), (1, 2), (2, 2), (3, 2),
                (0, -1), (1, -1)  # Dorsal fin
            ]
            tail = [(-2, 0), (-2, 1), (-2, 2), (-3, 1)]
            eye = (3, 1)
        else:
            body = [
                (0, 0), (-1, 0), (-2, 0), (-3, 0),
                (1, 1), (0, 1), (-1, 1), (-2, 1), (-3, 1), (-4, 1),
                (0, 2), (-1, 2), (-2, 2), (-3, 2),
                (0, -1), (-1, -1)
            ]
            tail = [(2, 0), (2, 1), (2, 2), (3, 1)]
            eye = (-3, 1)
        
        # Draw tail
        for px, py in tail:
            pygame.draw.rect(screen, (15, 15, 20), (cx + px * pixel_size, cy + py * pixel_size, pixel_size, pixel_size))
        
        # Draw body
        for px, py in body:
            pygame.draw.rect(screen, self.color, (cx + px * pixel_size, cy + py * pixel_size, pixel_size, pixel_size))
        
        # Red eye
        pygame.draw.rect(screen, (255, 0, 0), (cx + eye[0] * pixel_size, cy + eye[1] * pixel_size, pixel_size, pixel_size))

    def draw_tropical(self, screen):
        """Exotic predator with dramatic coloring"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.2
        body_height = self.size * 1.0
        
        # Dramatic color scheme - dark with bright accents
        accent_color = (255, 100, 50)  # Orange-red accent
        
        # Sleek body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            taper = 1.0 - 0.4 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, self.color, body_points)
        
        # Racing stripes
        for i in range(2):
            stripe_offset = (i - 0.5) * self.size * 0.4
            s_start_x = cx + math.cos(self.angle) * body_length * 0.3 + math.sin(self.angle) * stripe_offset
            s_start_y = cy + math.sin(self.angle) * body_length * 0.3 - math.cos(self.angle) * stripe_offset
            s_end_x = cx - math.cos(self.angle) * body_length * 0.4 + math.sin(self.angle) * stripe_offset
            s_end_y = cy - math.sin(self.angle) * body_length * 0.4 - math.cos(self.angle) * stripe_offset
            pygame.draw.line(screen, accent_color, (int(s_start_x), int(s_start_y)), (int(s_end_x), int(s_end_y)), 3)
        
        # Dramatic fins with color
        dorsal_x = cx - math.cos(self.angle) * self.size * 0.1
        dorsal_y = cy - math.sin(self.angle) * self.size * 0.1
        dorsal_tip_x = dorsal_x - math.sin(self.angle) * self.size * 1.2
        dorsal_tip_y = dorsal_y + math.cos(self.angle) * self.size * 1.2
        pygame.draw.polygon(screen, accent_color, [
            (dorsal_x + math.cos(self.angle) * 5, dorsal_y + math.sin(self.angle) * 5),
            (dorsal_tip_x, dorsal_tip_y),
            (dorsal_x - math.cos(self.angle) * self.size * 0.5, dorsal_y - math.sin(self.angle) * self.size * 0.5)
        ])
        
        # Forked tail
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        pygame.draw.polygon(screen, accent_color, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.5) * self.size * 1.2, tail_y - math.sin(self.angle + 0.5) * self.size * 1.2),
            (tail_x - math.cos(self.angle) * self.size * 0.4, tail_y - math.sin(self.angle) * self.size * 0.4),
            (tail_x - math.cos(self.angle - 0.5) * self.size * 1.2, tail_y - math.sin(self.angle - 0.5) * self.size * 1.2)
        ])
        
        # Glowing eye
        eye_x = cx + math.cos(self.angle) * self.size * 0.6
        eye_y = cy + math.sin(self.angle) * self.size * 0.6
        pygame.draw.circle(screen, (255, 200, 100), (int(eye_x), int(eye_y)), 5)
        pygame.draw.circle(screen, (255, 50, 0), (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 1)

    def draw_army(self, screen):
        """Army tank-inspired predator"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.5
        body_height = self.size * 1.0
        
        camo_colors = [(85, 107, 47), (107, 142, 35), (34, 49, 29), (154, 140, 105)]
        base_green = (70, 90, 40)
        dark_green = (34, 49, 29)
        
        # Tank-like angular body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            # More angular, less rounded
            taper = 1.0 - 0.4 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, base_green, body_points)
        
        # Heavy camo pattern
        random.seed(int(self.x * 50 + self.y))
        for _ in range(12):
            spot_offset_x = random.uniform(-0.7, 0.5) * body_length
            spot_offset_y = random.uniform(-0.4, 0.4) * body_height
            spot_x = cx + spot_offset_x * math.cos(self.angle) - spot_offset_y * math.sin(self.angle)
            spot_y = cy + spot_offset_x * math.sin(self.angle) + spot_offset_y * math.cos(self.angle)
            pygame.draw.circle(screen, random.choice(camo_colors), (int(spot_x), int(spot_y)), random.randint(4, 9))
        random.seed()
        
        # Cannon barrel (main gun)
        barrel_start_x = cx + math.cos(self.angle) * self.size * 0.3
        barrel_start_y = cy + math.sin(self.angle) * self.size * 0.3
        barrel_end_x = cx + math.cos(self.angle) * body_length * 0.7
        barrel_end_y = cy + math.sin(self.angle) * body_length * 0.7
        pygame.draw.line(screen, dark_green, (int(barrel_start_x), int(barrel_start_y)), 
                        (int(barrel_end_x), int(barrel_end_y)), 5)
        
        # Turret
        turret_x = cx + math.cos(self.angle) * self.size * 0.1
        turret_y = cy + math.sin(self.angle) * self.size * 0.1
        pygame.draw.circle(screen, dark_green, (int(turret_x), int(turret_y)), int(self.size * 0.35))
        
        # Tank tracks (side detail)
        for i in range(-2, 3):
            track_x = cx + math.cos(self.angle) * self.size * i * 0.25
            track_y = cy + math.sin(self.angle) * self.size * i * 0.25
            track_bot_x = track_x + math.sin(self.angle) * body_height * 0.4
            track_bot_y = track_y - math.cos(self.angle) * body_height * 0.4
            pygame.draw.line(screen, (50, 50, 40), (int(track_x), int(track_y)), (int(track_bot_x), int(track_bot_y)), 2)
        
        # Tail
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        pygame.draw.polygon(screen, dark_green, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.4) * self.size * 0.8, tail_y - math.sin(self.angle + 0.4) * self.size * 0.8),
            (tail_x - math.cos(self.angle - 0.4) * self.size * 0.8, tail_y - math.sin(self.angle - 0.4) * self.size * 0.8)
        ])
        
        # Army star
        star_x = cx - math.cos(self.angle) * self.size * 0.2
        star_y = cy - math.sin(self.angle) * self.size * 0.2
        self.draw_star(screen, star_x, star_y, self.size * 0.2, (255, 255, 255))
        
        # Menacing eye (periscope)
        eye_x = cx + math.cos(self.angle) * self.size * 0.5 - math.sin(self.angle) * self.size * 0.3
        eye_y = cy + math.sin(self.angle) * self.size * 0.5 + math.cos(self.angle) * self.size * 0.3
        pygame.draw.circle(screen, (200, 50, 50), (int(eye_x), int(eye_y)), 4)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), 2)

    def draw_star(self, screen, x, y, size, color):
        """Helper to draw a 5-pointed star"""
        points = []
        for i in range(5):
            angle = -math.pi/2 + (i * 2 * math.pi / 5)
            points.append((x + math.cos(angle) * size, y + math.sin(angle) * size))
            angle += math.pi / 5
            points.append((x + math.cos(angle) * size * 0.4, y + math.sin(angle) * size * 0.4))
        pygame.draw.polygon(screen, color, points)

    def draw_airforce(self, screen):
        """Air Force bomber/fighter predator"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.8
        body_height = self.size * 0.8
        
        af_silver = (180, 180, 195)
        af_blue = (0, 48, 143)
        af_dark = (100, 100, 110)
        
        # Sleek bomber body
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            taper = 1.0 - 0.55 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * 0.5
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, af_silver, body_points)
        
        # Blue stripe
        pygame.draw.line(screen, af_blue,
                        (int(cx + math.cos(self.angle) * body_length * 0.4), int(cy + math.sin(self.angle) * body_length * 0.4)),
                        (int(cx - math.cos(self.angle) * body_length * 0.4), int(cy - math.sin(self.angle) * body_length * 0.4)), 5)
        
        # Large swept wings
        wing_x = cx - math.cos(self.angle) * self.size * 0.3
        wing_y = cy - math.sin(self.angle) * self.size * 0.3
        # Top wing
        pygame.draw.polygon(screen, af_blue, [
            (wing_x + math.cos(self.angle) * self.size * 0.3, wing_y + math.sin(self.angle) * self.size * 0.3),
            (wing_x - math.cos(self.angle) * self.size * 0.8 - math.sin(self.angle) * self.size * 1.2,
             wing_y - math.sin(self.angle) * self.size * 0.8 + math.cos(self.angle) * self.size * 1.2),
            (wing_x - math.cos(self.angle) * self.size * 1.0, wing_y - math.sin(self.angle) * self.size * 1.0)
        ])
        # Bottom wing
        pygame.draw.polygon(screen, af_blue, [
            (wing_x + math.cos(self.angle) * self.size * 0.3, wing_y + math.sin(self.angle) * self.size * 0.3),
            (wing_x - math.cos(self.angle) * self.size * 0.8 + math.sin(self.angle) * self.size * 1.2,
             wing_y - math.sin(self.angle) * self.size * 0.8 - math.cos(self.angle) * self.size * 1.2),
            (wing_x - math.cos(self.angle) * self.size * 1.0, wing_y - math.sin(self.angle) * self.size * 1.0)
        ])
        
        # Twin tail fins
        tail_x = cx - math.cos(self.angle) * body_length * 0.45
        tail_y = cy - math.sin(self.angle) * body_length * 0.45
        for side in [-1, 1]:
            fin_base_x = tail_x + math.sin(self.angle) * self.size * 0.2 * side
            fin_base_y = tail_y - math.cos(self.angle) * self.size * 0.2 * side
            fin_tip_x = fin_base_x - math.sin(self.angle) * self.size * 0.8 * side
            fin_tip_y = fin_base_y + math.cos(self.angle) * self.size * 0.8 * side
            pygame.draw.polygon(screen, af_blue, [
                (fin_base_x, fin_base_y),
                (fin_tip_x, fin_tip_y),
                (tail_x - math.cos(self.angle) * self.size * 0.3, tail_y - math.sin(self.angle) * self.size * 0.3)
            ])
        
        # USAF roundel
        roundel_x = cx
        roundel_y = cy
        pygame.draw.circle(screen, af_blue, (int(roundel_x), int(roundel_y)), int(self.size * 0.28))
        pygame.draw.circle(screen, (255, 255, 255), (int(roundel_x), int(roundel_y)), int(self.size * 0.2))
        pygame.draw.circle(screen, (191, 10, 48), (int(roundel_x), int(roundel_y)), int(self.size * 0.1))
        
        # Cockpit
        cockpit_x = cx + math.cos(self.angle) * self.size * 0.7
        cockpit_y = cy + math.sin(self.angle) * self.size * 0.7
        pygame.draw.ellipse(screen, (80, 130, 180), (int(cockpit_x - 6), int(cockpit_y - 4), 12, 8))
        pygame.draw.ellipse(screen, (150, 200, 255), (int(cockpit_x - 3), int(cockpit_y - 2), 5, 3))

    def draw_spaceforce(self, screen):
        """Space Force capital ship predator"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.6
        body_height = self.size * 1.0
        
        sf_dark = (15, 15, 30)
        sf_silver = (160, 165, 180)
        sf_blue = (0, 50, 100)
        sf_glow = (80, 160, 255)
        sf_engine = (255, 150, 50)
        
        # Angular capital ship body
        nose_x = cx + math.cos(self.angle) * body_length * 0.5
        nose_y = cy + math.sin(self.angle) * body_length * 0.5
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        top_x = cx - math.sin(self.angle) * body_height * 0.5
        top_y = cy + math.cos(self.angle) * body_height * 0.5
        bot_x = cx + math.sin(self.angle) * body_height * 0.5
        bot_y = cy - math.cos(self.angle) * body_height * 0.5
        
        # Main hull
        pygame.draw.polygon(screen, sf_dark, [
            (nose_x, nose_y), (top_x, top_y), (tail_x, tail_y), (bot_x, bot_y)
        ])
        
        # Hull plating lines
        for i in range(4):
            ratio = 0.2 + i * 0.2
            line_x = nose_x + (tail_x - nose_x) * ratio
            line_y = nose_y + (tail_y - nose_y) * ratio
            line_top_x = line_x - math.sin(self.angle) * body_height * 0.4
            line_top_y = line_y + math.cos(self.angle) * body_height * 0.4
            line_bot_x = line_x + math.sin(self.angle) * body_height * 0.4
            line_bot_y = line_y - math.cos(self.angle) * body_height * 0.4
            pygame.draw.line(screen, sf_silver, (int(line_top_x), int(line_top_y)), (int(line_bot_x), int(line_bot_y)), 1)
        
        # Engine array (multiple glows)
        for i in range(-1, 2):
            eng_x = tail_x + math.sin(self.angle) * self.size * 0.25 * i
            eng_y = tail_y - math.cos(self.angle) * self.size * 0.25 * i
            pygame.draw.circle(screen, sf_engine, (int(eng_x - math.cos(self.angle) * 5), int(eng_y - math.sin(self.angle) * 5)), 5)
            pygame.draw.circle(screen, (255, 255, 200), (int(eng_x - math.cos(self.angle) * 3), int(eng_y - math.sin(self.angle) * 3)), 2)
        
        # Command bridge (top structure)
        bridge_x = cx - math.cos(self.angle) * self.size * 0.2
        bridge_y = cy - math.sin(self.angle) * self.size * 0.2
        bridge_top_x = bridge_x - math.sin(self.angle) * self.size * 0.7
        bridge_top_y = bridge_y + math.cos(self.angle) * self.size * 0.7
        pygame.draw.polygon(screen, sf_blue, [
            (bridge_x - math.cos(self.angle) * 8, bridge_y - math.sin(self.angle) * 8),
            (bridge_x + math.cos(self.angle) * 8, bridge_y + math.sin(self.angle) * 8),
            (bridge_top_x, bridge_top_y)
        ])
        
        # Weapon arrays (side fins)
        for side in [-1, 1]:
            fin_x = cx + math.cos(self.angle) * self.size * 0.3
            fin_y = cy + math.sin(self.angle) * self.size * 0.3
            fin_tip_x = fin_x + math.sin(self.angle) * self.size * 0.6 * side
            fin_tip_y = fin_y - math.cos(self.angle) * self.size * 0.6 * side
            pygame.draw.polygon(screen, sf_silver, [
                (fin_x, fin_y),
                (fin_tip_x, fin_tip_y),
                (fin_x - math.cos(self.angle) * self.size * 0.4, fin_y - math.sin(self.angle) * self.size * 0.4)
            ])
        
        # Forward sensor/weapon glow
        weapon_x = nose_x
        weapon_y = nose_y
        pygame.draw.circle(screen, sf_glow, (int(weapon_x), int(weapon_y)), 4)
        pygame.draw.circle(screen, (255, 255, 255), (int(weapon_x), int(weapon_y)), 2)
        
        # Bridge windows
        for i in range(3):
            win_x = bridge_x + (bridge_top_x - bridge_x) * (0.3 + i * 0.2) + math.cos(self.angle) * (i - 1) * 3
            win_y = bridge_y + (bridge_top_y - bridge_y) * (0.3 + i * 0.2) + math.sin(self.angle) * (i - 1) * 3
            pygame.draw.circle(screen, sf_glow, (int(win_x), int(win_y)), 2)

    def draw_navy(self, screen):
        """Navy destroyer/battleship predator"""
        cx, cy = self.x, self.y
        body_length = self.size * 2.6
        body_height = self.size * 0.9
        
        navy_gray = (110, 115, 125)
        navy_dark = (70, 75, 85)
        navy_blue = (0, 0, 70)
        navy_white = (240, 240, 245)
        navy_gold = (255, 200, 50)
        
        # Battleship hull
        body_points = []
        for i in range(24):
            angle = (i / 24) * 2 * math.pi
            py_mult = 0.35 if math.sin(angle) > 0 else 0.65
            taper = 1.0 - 0.4 * max(0, math.cos(angle))
            px = math.cos(angle) * body_length * 0.5 * taper
            py = math.sin(angle) * body_height * py_mult
            rx = px * math.cos(self.angle) - py * math.sin(self.angle)
            ry = px * math.sin(self.angle) + py * math.cos(self.angle)
            body_points.append((cx + rx, cy + ry))
        
        pygame.draw.polygon(screen, navy_gray, body_points)
        
        # Deck
        deck_start_x = cx + math.cos(self.angle) * body_length * 0.35
        deck_start_y = cy + math.sin(self.angle) * body_length * 0.35
        deck_end_x = cx - math.cos(self.angle) * body_length * 0.4
        deck_end_y = cy - math.sin(self.angle) * body_length * 0.4
        pygame.draw.line(screen, navy_dark, (int(deck_start_x), int(deck_start_y)), (int(deck_end_x), int(deck_end_y)), 4)
        
        # Main gun turrets
        for turret_pos in [0.15, -0.15]:
            turret_x = cx + math.cos(self.angle) * self.size * turret_pos
            turret_y = cy + math.sin(self.angle) * self.size * turret_pos
            turret_top_x = turret_x - math.sin(self.angle) * self.size * 0.25
            turret_top_y = turret_y + math.cos(self.angle) * self.size * 0.25
            pygame.draw.circle(screen, navy_dark, (int(turret_top_x), int(turret_top_y)), int(self.size * 0.2))
            # Gun barrels
            barrel_end_x = turret_top_x + math.cos(self.angle) * self.size * 0.5
            barrel_end_y = turret_top_y + math.sin(self.angle) * self.size * 0.5
            pygame.draw.line(screen, navy_blue, (int(turret_top_x), int(turret_top_y)), (int(barrel_end_x), int(barrel_end_y)), 3)
        
        # Bridge/superstructure
        bridge_x = cx - math.cos(self.angle) * self.size * 0.1
        bridge_y = cy - math.sin(self.angle) * self.size * 0.1
        bridge_top_x = bridge_x - math.sin(self.angle) * self.size * 0.6
        bridge_top_y = bridge_y + math.cos(self.angle) * self.size * 0.6
        pygame.draw.polygon(screen, navy_dark, [
            (bridge_x - math.cos(self.angle) * 10, bridge_y - math.sin(self.angle) * 10),
            (bridge_x + math.cos(self.angle) * 10, bridge_y + math.sin(self.angle) * 10),
            (bridge_top_x + math.cos(self.angle) * 5, bridge_top_y + math.sin(self.angle) * 5),
            (bridge_top_x - math.cos(self.angle) * 5, bridge_top_y - math.sin(self.angle) * 5)
        ])
        
        # Radar/antenna
        ant_x = bridge_top_x - math.sin(self.angle) * self.size * 0.2
        ant_y = bridge_top_y + math.cos(self.angle) * self.size * 0.2
        pygame.draw.line(screen, navy_gray, (int(bridge_top_x), int(bridge_top_y)), (int(ant_x), int(ant_y)), 2)
        pygame.draw.circle(screen, navy_white, (int(ant_x), int(ant_y)), 3)
        
        # Tail/stern
        tail_x = cx - math.cos(self.angle) * body_length * 0.5
        tail_y = cy - math.sin(self.angle) * body_length * 0.5
        pygame.draw.polygon(screen, navy_dark, [
            (tail_x, tail_y),
            (tail_x - math.cos(self.angle + 0.5) * self.size * 0.7, tail_y - math.sin(self.angle + 0.5) * self.size * 0.7),
            (tail_x - math.cos(self.angle) * self.size * 0.3, tail_y - math.sin(self.angle) * self.size * 0.3),
            (tail_x - math.cos(self.angle - 0.5) * self.size * 0.7, tail_y - math.sin(self.angle - 0.5) * self.size * 0.7)
        ])
        
        # Anchor emblem
        anchor_x = cx + math.cos(self.angle) * self.size * 0.4
        anchor_y = cy + math.sin(self.angle) * self.size * 0.4
        pygame.draw.line(screen, navy_gold, 
                        (int(anchor_x - math.sin(self.angle) * 8), int(anchor_y + math.cos(self.angle) * 8)),
                        (int(anchor_x + math.sin(self.angle) * 8), int(anchor_y - math.cos(self.angle) * 8)), 2)
        pygame.draw.line(screen, navy_gold,
                        (int(anchor_x - math.cos(self.angle) * 5 - math.sin(self.angle) * 4), 
                         int(anchor_y - math.sin(self.angle) * 5 + math.cos(self.angle) * 4)),
                        (int(anchor_x + math.cos(self.angle) * 5 - math.sin(self.angle) * 4),
                         int(anchor_y + math.sin(self.angle) * 5 + math.cos(self.angle) * 4)), 2)
        
        # Bridge windows (eyes)
        for i in range(3):
            win_ratio = 0.3 + i * 0.2
            win_x = bridge_x + (bridge_top_x - bridge_x) * win_ratio
            win_y = bridge_y + (bridge_top_y - bridge_y) * win_ratio
            pygame.draw.circle(screen, navy_white, (int(win_x), int(win_y)), 2)


# Create breeder fish - 6 of each color in breeding pairs
fish_list = []

# Blue breeders (3 pairs)
blue_fish = [
    Fish(200, 150, (50, 200, 255), size=15, speed=2),
    Fish(250, 180, (50, 200, 255), size=15, speed=2),
    Fish(400, 200, (50, 200, 255), size=15, speed=2),
    Fish(450, 230, (50, 200, 255), size=15, speed=2),
    Fish(600, 250, (50, 200, 255), size=15, speed=2),
    Fish(650, 280, (50, 200, 255), size=15, speed=2),
]
# Pair them: 0-1, 2-3, 4-5
blue_fish[0].breed_partner = blue_fish[1]
blue_fish[1].breed_partner = blue_fish[0]
blue_fish[2].breed_partner = blue_fish[3]
blue_fish[3].breed_partner = blue_fish[2]
blue_fish[4].breed_partner = blue_fish[5]
blue_fish[5].breed_partner = blue_fish[4]
fish_list.extend(blue_fish)

# Yellow herbivore breeders (3 pairs)
yellow_fish = [
    Fish(200, 350, (255, 255, 100), size=18, speed=3),
    Fish(250, 380, (255, 255, 100), size=18, speed=3),
    Fish(400, 400, (255, 255, 100), size=18, speed=3),
    Fish(450, 430, (255, 255, 100), size=18, speed=3),
    Fish(600, 450, (255, 255, 100), size=18, speed=3),
    Fish(650, 480, (255, 255, 100), size=18, speed=3),
]
for fish in yellow_fish:
    fish.is_herbivore = True
yellow_fish[0].breed_partner = yellow_fish[1]
yellow_fish[1].breed_partner = yellow_fish[0]
yellow_fish[2].breed_partner = yellow_fish[3]
yellow_fish[3].breed_partner = yellow_fish[2]
yellow_fish[4].breed_partner = yellow_fish[5]
yellow_fish[5].breed_partner = yellow_fish[4]
fish_list.extend(yellow_fish)

# Orange breeders (3 pairs)
orange_fish = [
    Fish(200, 550, (255, 150, 50), size=20, speed=2.5),
    Fish(250, 580, (255, 150, 50), size=20, speed=2.5),
    Fish(400, 600, (255, 150, 50), size=20, speed=2.5),
    Fish(450, 550, (255, 150, 50), size=20, speed=2.5),
    Fish(600, 580, (255, 150, 50), size=20, speed=2.5),
    Fish(650, 600, (255, 150, 50), size=20, speed=2.5),
]
orange_fish[0].breed_partner = orange_fish[1]
orange_fish[1].breed_partner = orange_fish[0]
orange_fish[2].breed_partner = orange_fish[3]
orange_fish[3].breed_partner = orange_fish[2]
orange_fish[4].breed_partner = orange_fish[5]
orange_fish[5].breed_partner = orange_fish[4]
fish_list.extend(orange_fish)

# Initialize feeder and predator lists
feeder_fish_list = []
predator_fish_list = []

# Start with 2 predator fish
predator_fish_list.append(PredatorFish(600, 300))
predator_fish_list.append(PredatorFish(400, 400))
predator_fish_list.append(PredatorFish(800, 500))
predator_fish_list.append(PredatorFish(300, 550))

# Algae System


class AlgaePatch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5    # Start small
        self.max_size = 25
        self.color = (34, 139, 34)    # Forest green

    def grow(self, nitrate_level):
        """Algae grows faster with high nitrates"""
        if nitrate_level > 30 and self.size < self.max_size:
            # Faster growth with more nitrates
            growth = 0.05 + (nitrate_level / 1000)
            self.size += growth

    def shrink(self, amount):
        """Algae shrinks when eaten"""
        self.size -= amount

    def is_dead(self):
        return self.size <= 0

    def draw(self, screen):
        """Draw algae patch"""
        pygame.draw.circle(screen, self.color, (int(
            self.x), int(self.y)), int(self.size))
        # Add some texture
        for i in range(3):
            offset_x = random.randint(-int(self.size//2), int(self.size//2))
            offset_y = random.randint(-int(self.size//2), int(self.size//2))
            pygame.draw.circle(screen, (44, 19, 44),
                               (int(self.x + offset_x), int(self.y + offset_y)),
                               max(1, int(self.size//4)))

# Coral class


class Coral:
    def __init__(self, x, y, coral_type, color):
        self.x = x
        self.y = y
        self.coral_type = coral_type  # "branch", "brain", "plate", "tube", "fan"
        self.base_color = color
        self.color = color
        self.size = 10  # Start small
        self.max_size = random.randint(35, 65)
        self.growth_rate = 0.01  # Slow growth
        self.pulse_offset = random.uniform(0, 2 * math.pi)  # For animation
        self.sway_offset = random.uniform(0, 2 * math.pi)
        self.age = 0
        
        # Generate random branch structure for branch coral
        self.branches = []
        if coral_type == "branch":
            num_branches = random.randint(4, 7)
            for i in range(num_branches):
                angle = random.uniform(-0.8, 0.8)  # Spread angle
                length = random.uniform(0.6, 1.0)  # Relative length
                thickness = random.uniform(0.3, 0.6)
                sub_branches = random.randint(1, 3)
                self.branches.append({
                    'angle': angle,
                    'length': length,
                    'thickness': thickness,
                    'sub_branches': sub_branches,
                    'sub_angles': [random.uniform(-0.5, 0.5) for _ in range(sub_branches)]
                })
        
        # Generate tube positions for tube coral
        self.tubes = []
        if coral_type == "tube":
            num_tubes = random.randint(5, 10)
            for i in range(num_tubes):
                offset_x = random.uniform(-0.8, 0.8)
                offset_y = random.uniform(-0.3, 0.3)
                height = random.uniform(0.5, 1.0)
                self.tubes.append({'x': offset_x, 'y': offset_y, 'height': height})
        
        # Generate polyp positions
        self.polyps = []
        num_polyps = random.randint(8, 15)
        for i in range(num_polyps):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0.3, 0.9)
            self.polyps.append({'angle': angle, 'dist': dist, 'phase': random.uniform(0, 2 * math.pi)})

    def update(self):
        """Grow coral slowly over time"""
        self.age += 1
        if self.size < self.max_size:
            self.size += self.growth_rate
        
        # Gentle color pulsing for bioluminescence effect
        pulse = math.sin(self.age * 0.03 + self.pulse_offset) * 0.15
        self.color = (
            min(255, max(0, int(self.base_color[0] * (1 + pulse)))),
            min(255, max(0, int(self.base_color[1] * (1 + pulse)))),
            min(255, max(0, int(self.base_color[2] * (1 + pulse))))
        )

    def draw(self, screen):
        """Draw coral based on type"""
        if self.coral_type == "branch":
            self.draw_branch(screen)
        elif self.coral_type == "brain":
            self.draw_brain(screen)
        elif self.coral_type == "plate":
            self.draw_plate(screen)
        elif self.coral_type == "tube":
            self.draw_tube(screen)
        elif self.coral_type == "fan":
            self.draw_fan(screen)

    def draw_branch(self, screen):
        """Draw realistic branching coral"""
        sway = math.sin(self.age * 0.02 + self.sway_offset) * 3
        
        # Darker base color
        dark_color = (max(0, self.color[0] - 50), max(0, self.color[1] - 50), max(0, self.color[2] - 50))
        light_color = (min(255, self.color[0] + 40), min(255, self.color[1] + 40), min(255, self.color[2] + 40))
        
        # Draw base/trunk
        base_width = self.size * 0.3
        pygame.draw.polygon(screen, dark_color, [
            (self.x - base_width * 0.5, self.y),
            (self.x + base_width * 0.5, self.y),
            (self.x + base_width * 0.3, self.y - self.size * 0.3),
            (self.x - base_width * 0.3, self.y - self.size * 0.3)
        ])
        
        # Draw each branch
        for branch in self.branches:
            branch_sway = sway * branch['length']
            
            # Main branch
            start_x = self.x
            start_y = self.y - self.size * 0.2
            end_x = self.x + math.sin(branch['angle']) * self.size * branch['length'] + branch_sway
            end_y = self.y - self.size * branch['length']
            
            thickness = max(2, int(self.size * branch['thickness'] * 0.15))
            pygame.draw.line(screen, self.color, (start_x, start_y), (end_x, end_y), thickness)
            
            # Sub-branches
            for i, sub_angle in enumerate(branch['sub_angles']):
                sub_start_x = start_x + (end_x - start_x) * (0.4 + i * 0.25)
                sub_start_y = start_y + (end_y - start_y) * (0.4 + i * 0.25)
                sub_end_x = sub_start_x + math.sin(branch['angle'] + sub_angle) * self.size * 0.4 + branch_sway * 0.5
                sub_end_y = sub_start_y - self.size * 0.35
                
                pygame.draw.line(screen, self.color, (sub_start_x, sub_start_y), (sub_end_x, sub_end_y), max(1, thickness - 1))
                
                # Polyp tip
                pygame.draw.circle(screen, light_color, (int(sub_end_x), int(sub_end_y)), max(2, thickness))
            
            # Main branch tip polyp
            pygame.draw.circle(screen, light_color, (int(end_x), int(end_y)), max(3, thickness + 1))

    def draw_brain(self, screen):
        """Draw realistic brain coral with maze pattern"""
        pulse = math.sin(self.age * 0.05 + self.pulse_offset) * 2
        current_size = self.size + pulse
        
        dark_color = (max(0, self.color[0] - 60), max(0, self.color[1] - 60), max(0, self.color[2] - 60))
        light_color = (min(255, self.color[0] + 50), min(255, self.color[1] + 50), min(255, self.color[2] + 50))
        
        # Main dome shape
        dome_points = []
        num_points = 32
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            # Slightly irregular edge
            wave = math.sin(angle * 5 + self.pulse_offset) * current_size * 0.08
            radius = current_size + wave
            # Flatten the bottom
            y_squash = 0.6 if math.sin(angle) > 0 else 1.0
            px = self.x + math.cos(angle) * radius
            py = self.y + math.sin(angle) * radius * y_squash
            dome_points.append((px, py))
        
        pygame.draw.polygon(screen, self.color, dome_points)
        pygame.draw.polygon(screen, dark_color, dome_points, 2)
        
        # Draw maze/groove pattern
        num_grooves = 5
        for g in range(num_grooves):
            groove_points = []
            groove_radius = current_size * (0.3 + g * 0.15)
            num_groove_points = 16
            for i in range(num_groove_points):
                angle = (i / num_groove_points) * 2 * math.pi
                wave = math.sin(angle * 3 + g + self.age * 0.02) * groove_radius * 0.2
                r = groove_radius + wave
                px = self.x + math.cos(angle) * r * 0.9
                py = self.y + math.sin(angle) * r * 0.5
                groove_points.append((int(px), int(py)))
            
            if len(groove_points) > 2:
                pygame.draw.lines(screen, dark_color, True, groove_points, 2)
        
        # Highlight on top
        highlight_y = self.y - current_size * 0.3
        pygame.draw.ellipse(screen, light_color, 
                           (self.x - current_size * 0.3, highlight_y - current_size * 0.15,
                            current_size * 0.6, current_size * 0.3))

    def draw_plate(self, screen):
        """Draw layered plate/table coral"""
        pulse = math.sin(self.age * 0.04 + self.pulse_offset) * 1.5
        sway = math.sin(self.age * 0.015 + self.sway_offset) * 2
        
        dark_color = (max(0, self.color[0] - 50), max(0, self.color[1] - 50), max(0, self.color[2] - 50))
        light_color = (min(255, self.color[0] + 40), min(255, self.color[1] + 40), min(255, self.color[2] + 40))
        
        # Draw stalk
        stalk_width = self.size * 0.15
        pygame.draw.polygon(screen, dark_color, [
            (self.x - stalk_width, self.y),
            (self.x + stalk_width, self.y),
            (self.x + stalk_width * 0.7, self.y - self.size * 0.5),
            (self.x - stalk_width * 0.7, self.y - self.size * 0.5)
        ])
        
        # Draw multiple plate layers
        num_layers = 3
        for layer in range(num_layers):
            layer_y = self.y - self.size * 0.4 - layer * self.size * 0.15
            layer_width = self.size * (1.3 - layer * 0.2) + pulse
            layer_height = self.size * (0.25 - layer * 0.03)
            layer_sway = sway * (1 + layer * 0.3)
            
            # Each layer is an ellipse
            layer_color = (
                min(255, self.color[0] + layer * 15),
                min(255, self.color[1] + layer * 15),
                min(255, self.color[2] + layer * 15)
            )
            
            # Draw plate as polygon for 3D effect
            plate_points = []
            for i in range(24):
                angle = (i / 24) * 2 * math.pi
                px = self.x + math.cos(angle) * layer_width + layer_sway
                py = layer_y + math.sin(angle) * layer_height
                plate_points.append((px, py))
            
            pygame.draw.polygon(screen, layer_color, plate_points)
            pygame.draw.polygon(screen, dark_color, plate_points, 1)
            
            # Add radial lines for texture
            if layer == num_layers - 1:
                for i in range(8):
                    angle = (i / 8) * 2 * math.pi
                    line_end_x = self.x + math.cos(angle) * layer_width * 0.9 + layer_sway
                    line_end_y = layer_y + math.sin(angle) * layer_height * 0.9
                    pygame.draw.line(screen, dark_color, 
                                   (self.x + layer_sway, layer_y), 
                                   (int(line_end_x), int(line_end_y)), 1)

    def draw_tube(self, screen):
        """Draw tube coral colony"""
        sway = math.sin(self.age * 0.025 + self.sway_offset) * 2
        
        dark_color = (max(0, self.color[0] - 40), max(0, self.color[1] - 40), max(0, self.color[2] - 40))
        light_color = (min(255, self.color[0] + 60), min(255, self.color[1] + 60), min(255, self.color[2] + 60))
        inner_color = (max(0, self.color[0] - 80), max(0, self.color[1] - 80), max(0, self.color[2] - 80))
        
        # Sort tubes by y position for proper layering
        sorted_tubes = sorted(self.tubes, key=lambda t: t['y'], reverse=True)
        
        for tube in sorted_tubes:
            tube_x = self.x + tube['x'] * self.size * 0.5
            tube_base_y = self.y + tube['y'] * self.size * 0.3
            tube_height = self.size * tube['height']
            tube_width = self.size * 0.18
            
            # Individual tube sway
            tube_sway = sway * tube['height']
            tube_top_x = tube_x + tube_sway
            tube_top_y = tube_base_y - tube_height
            
            # Tube body (trapezoid)
            pygame.draw.polygon(screen, self.color, [
                (tube_x - tube_width, tube_base_y),
                (tube_x + tube_width, tube_base_y),
                (tube_top_x + tube_width * 0.8, tube_top_y),
                (tube_top_x - tube_width * 0.8, tube_top_y)
            ])
            
            # Tube opening (ellipse at top)
            opening_width = tube_width * 1.6
            opening_height = tube_width * 0.5
            pygame.draw.ellipse(screen, light_color,
                              (tube_top_x - opening_width, tube_top_y - opening_height,
                               opening_width * 2, opening_height * 2))
            # Inner dark part
            pygame.draw.ellipse(screen, inner_color,
                              (tube_top_x - opening_width * 0.6, tube_top_y - opening_height * 0.6,
                               opening_width * 1.2, opening_height * 1.2))
            
            # Polyp tentacles waving from opening
            num_tentacles = 6
            for t in range(num_tentacles):
                tentacle_angle = (t / num_tentacles) * 2 * math.pi
                wave = math.sin(self.age * 0.08 + tube['x'] * 5 + t) * 3
                tentacle_end_x = tube_top_x + math.cos(tentacle_angle) * opening_width * 0.8 + wave
                tentacle_end_y = tube_top_y - opening_height - 3 + math.sin(tentacle_angle) * 2
                pygame.draw.line(screen, light_color,
                               (int(tube_top_x + math.cos(tentacle_angle) * opening_width * 0.3), 
                                int(tube_top_y)),
                               (int(tentacle_end_x), int(tentacle_end_y)), 1)

    def draw_fan(self, screen):
        """Draw sea fan coral"""
        sway = math.sin(self.age * 0.02 + self.sway_offset) * 4
        pulse = math.sin(self.age * 0.04 + self.pulse_offset)
        
        dark_color = (max(0, self.color[0] - 50), max(0, self.color[1] - 50), max(0, self.color[2] - 50))
        light_color = (min(255, self.color[0] + 40), min(255, self.color[1] + 40), min(255, self.color[2] + 40))
        
        # Draw central stem
        stem_top_x = self.x + sway
        stem_top_y = self.y - self.size * 0.9
        pygame.draw.line(screen, dark_color, (self.x, self.y), (stem_top_x, stem_top_y), 3)
        
        # Draw fan structure with multiple branches
        fan_width = self.size * 1.2
        fan_height = self.size * 0.8
        
        # Main fan outline
        num_ribs = 9
        for i in range(num_ribs):
            # Spread ribs in a fan pattern
            rib_angle = -0.7 + (i / (num_ribs - 1)) * 1.4
            rib_sway = sway * (1 + abs(rib_angle) * 0.5)
            
            rib_length = fan_height * (1.0 - abs(rib_angle) * 0.3)
            rib_end_x = stem_top_x + math.sin(rib_angle) * fan_width * 0.5 + rib_sway * 0.5
            rib_end_y = stem_top_y - rib_length
            
            # Draw rib
            pygame.draw.line(screen, self.color, (stem_top_x, stem_top_y), 
                           (int(rib_end_x), int(rib_end_y)), 2)
            
            # Draw cross-connections between ribs
            if i > 0:
                prev_angle = -0.7 + ((i-1) / (num_ribs - 1)) * 1.4
                prev_length = fan_height * (1.0 - abs(prev_angle) * 0.3)
                
                # Multiple horizontal connections
                for h in range(3):
                    height_ratio = 0.3 + h * 0.25
                    
                    curr_x = stem_top_x + math.sin(rib_angle) * fan_width * 0.5 * height_ratio + rib_sway * 0.3 * height_ratio
                    curr_y = stem_top_y - rib_length * height_ratio
                    prev_x = stem_top_x + math.sin(prev_angle) * fan_width * 0.5 * height_ratio + rib_sway * 0.3 * height_ratio
                    prev_y = stem_top_y - prev_length * height_ratio
                    
                    pygame.draw.line(screen, light_color if h % 2 == 0 else self.color,
                                   (int(prev_x), int(prev_y)), (int(curr_x), int(curr_y)), 1)
            
            # Polyp dots along ribs
            for p in range(3):
                polyp_ratio = 0.3 + p * 0.25
                polyp_x = stem_top_x + (rib_end_x - stem_top_x) * polyp_ratio
                polyp_y = stem_top_y + (rib_end_y - stem_top_y) * polyp_ratio
                if (i + p) % 2 == 0:
                    pygame.draw.circle(screen, light_color, (int(polyp_x), int(polyp_y)), 2)

# Kelp class


class Kelp:
    def __init__(self, x):
        self.x = x
        self.base_y = 700  # Grows from sand
        self.height = random.randint(375, 750)  # Varying heights
        self.color = (20, 80, 40)  # Dark green
        self.segments = 12  # Number of segments for smooth curve
        self.sway_offset = random.uniform(0, 2 * math.pi)  # Random phase
        self.sway_speed = random.uniform(0.02, 0.04)  # How fast it sways
        self.age = 0

    def update(self):
        """Update swaying animation"""
        self.age += 1

    def draw(self, screen):
        """Draw kelp as a wavy vertical line"""
        points = []
        for i in range(self.segments + 1):
            # Calculate position along kelp
            ratio = i / self.segments
            y = self.base_y - (self.height * ratio)

            # Add sway (more sway at the top)
            sway_amount = ratio * 15  # More sway at top
            sway = math.sin(self.age * self.sway_speed +
                            self.sway_offset + ratio * 2) * sway_amount
            x = self.x + sway

            points.append((x, y))

        # Draw the kelp as a thick line
        if len(points) > 1:
            pygame.draw.lines(screen, self.color, False, points, 5)

            # Add lighter highlights on one side
            highlight_color = (30, 100, 50)
            for i in range(len(points) - 1):
                if i % 2 == 0:  # Every other segment
                    start = points[i]
                    end = points[i + 1]
                    offset_start = (start[0] - 2, start[1])
                    offset_end = (end[0] - 2, end[1])
                    pygame.draw.line(screen, highlight_color,
                                     offset_start, offset_end, 2)


class Bubble:
    def __init__(self, x, y, size=None):
        self.x = x
        self.y = y
        self.size = size if size else random.randint(2, 5)
        self.speed = random.uniform(0.5, 1.5)
        self.wobble = random.uniform(-0.3, 0.3)    # Horizontal wobble
        self.wobble_offset = random.uniform(0, 2 * math.pi)
        self.age = 0

    def update(self):
        """Bubbles rise and wobble"""
        self.age += 1
        self.y -= self.speed  # Rise up
        # Wobble side to side
        self.x += math.sin(self.age * 0.1 + self.wobble_offset) * self.wobble

    def is_expired(self):
        """Remove when reaching surface"""
        return self.y < 50

    def draw(self, screen):
        """Draw bubble with highlight"""
        # Main bubble
        pygame.draw.circle(screen, (150, 200, 255),
                           (int(self.x), int(self.y)), self.size)
        # Highlight (smaller, offset)
        highlight_x = int(self.x - self.size // 3)
        highlight_y = int(self.y - self.size // 3)
        pygame.draw.circle(screen, (200, 230, 255),
                           (highlight_x, highlight_y), max(1, self.size // 3))


# Treasure Chest - FIXED (single definition)
class TreasureChest:
    def __init__(self, x, y, delay=0):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.lid_open_amount = 0    # 0 = closed, 1 = fully open
        self.bubble_timer = 0
        
        # Cycle timer system
        self.cycle_timer = delay  # Starts at different offsets for staggered opening
        self.cycle_length = 900   # Full cycle: 15 seconds at 60 FPS
        
        # Colors
        self.chest_color = (101, 67, 33)    # Brown
        self.gold_color = (255, 215, 0)
        self.dark_brown = (70, 47, 23)

    def update(self, bubble_list):
        """Animate lid based on cycle timer"""
        # Increment cycle timer
        self.cycle_timer += 1
        if self.cycle_timer >= self.cycle_length:
            self.cycle_timer = 0

        # Calculate lid position based on where we are in cycle
        # Open for first 5 seconds (300 frames), closed for rest
        if self.cycle_timer < 300:
            # Opening/open phase - open over ~1.5 sec
            target_open = min(1.0, self.cycle_timer / 100.0)
        else:
            # Closing/closed phase - close over ~1.5 sec
            frames_since_open = self.cycle_timer - 300
            target_open = max(0, 1.0 - (frames_since_open / 100.0))

        # Smoothly move toward target
        self.lid_open_amount = target_open

        # Spawn bubbles when open
        if self.lid_open_amount > 0.3:
            self.bubble_timer += 1
            if self.bubble_timer > 15:
                self.bubble_timer = 0
                bubble_x = self.x + self.width // 2 + random.randint(-5, 5)
                bubble_y = self.y - 5
                bubble_list.append(Bubble(bubble_x, bubble_y))

    def draw(self, screen):
        """Draw treasure chest with animated lid"""
        # Base of chest
        base_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.chest_color, base_rect)
        pygame.draw.rect(screen, self.dark_brown, base_rect, 2)

        # Draw gold inside when open
        if self.lid_open_amount > 0.2:
            gold_height = int(self.height * 0.4)
            gold_rect = pygame.Rect(
                self.x + 5,
                self.y + self.height - gold_height,
                self.width - 10,
                gold_height
            )
            pygame.draw.rect(screen, self.gold_color, gold_rect)
            # Gold coins
            for i in range(3):
                coin_x = self.x + random.randint(8, self.width - 8)
                coin_y = self.y + self.height - random.randint(5, gold_height)
                pygame.draw.circle(screen, (255, 223, 0), (coin_x, coin_y), 3)

        # Lid
        lid_height = 8
        hinge_x = self.x + self.width
        hinge_y = self.y

        if self.lid_open_amount < 0.1:
            # Closed lid - draw flat on top
            lid_rect = pygame.Rect(
                self.x, self.y - lid_height, self.width, lid_height)
            pygame.draw.rect(screen, self.dark_brown, lid_rect)
            pygame.draw.rect(screen, (50, 30, 10), lid_rect, 2)
        else:
            # Open lid - draw angled
            front_y = self.y - (self.lid_open_amount * 25)
            points = [
                (self.x, front_y),                    # Front top
                (self.x, front_y + lid_height),       # Front bottom
                (hinge_x, hinge_y + lid_height),      # Back bottom
                (hinge_x, hinge_y)                    # Back top (hinge)
            ]
            pygame.draw.polygon(screen, self.dark_brown, points)
            pygame.draw.polygon(screen, (50, 30, 10), points, 2)


class PirateShip:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 450  # Back to near bottom
        self.age = 0
        # Dark silhouette colors
        self.ship_color = (30, 40, 50)
        self.sail_color = (40, 50, 60)

    def update(self):
        self.age += 1

    def draw(self, screen):
        """Draw pirate ship silhouette - 5x original size"""
        # Hull - 5x bigger
        hull_points = [
            (self.x - 400, self.y + 250),    # Bottom left
            (self.x - 500, self.y),          # Top left
            (self.x + 500, self.y),          # Top right
            (self.x + 400, self.y + 250)     # Bottom right
        ]
        pygame.draw.polygon(screen, self.ship_color, hull_points)

        # Deck
        deck_rect = pygame.Rect(self.x - 450, self.y, 900, 50)
        pygame.draw.rect(screen, (25, 35, 45), deck_rect)

        # Mast (broken, tilted)
        mast_sway = math.sin(self.age * 0.02) * 15
        pygame.draw.line(screen, (20, 25, 30),
                         (self.x, self.y),
                         (self.x + 50 + mast_sway, self.y - 400), 25)

        # Torn sail (swaying)
        sail_sway = math.sin(self.age * 0.03) * 25
        sail_points = [
            (self.x + 50, self.y - 350),
            (self.x + 200 + sail_sway, self.y - 250),
            (self.x + 175 + sail_sway, self.y - 150),
            (self.x + 50, self.y - 200)
        ]
        pygame.draw.polygon(screen, self.sail_color, sail_points)

        # Portholes - 5 of them
        for i in range(5):
            porthole_x = self.x - 300 + (i * 150)
            porthole_y = self.y + 100
            pygame.draw.circle(screen, (10, 15, 20),
                               (porthole_x, porthole_y), 20)


# Light rays from surface
class LightRay:
    def __init__(self, x):
        self.x = x
        self.width = random.randint(40, 80)
        self.intensity_offset = random.uniform(0, 2 * math.pi)
        self.sway_offset = random.uniform(0, 2 * math.pi)
        self.age = 0

    def update(self):
        self.age += 1

    def draw(self, screen):
        """Draw volumetric light ray"""
        # Calculate sway
        sway = math.sin(self.age * 0.01 + self.sway_offset) * 20

        # Calculate pulsing intensity - much brighter now
        intensity = 45 + int(math.sin(self.age * 0.02 +
                             self.intensity_offset) * 20)

        # Draw ray as polygon with transparency - brighter, more golden color
        ray_color = (180, 220, 255, intensity)    # Bright cyan-white with alpha

        top_left = (self.x + sway - self.width // 2, 0)
        top_right = (self.x + sway + self.width // 2, 0)
        bottom_left = (self.x - self.width // 3, HEIGHT - 100)
        bottom_right = (self.x + self.width // 3, HEIGHT - 100)

        points = [top_left, top_right, bottom_right, bottom_left]

        # Create surface with alpha
        ray_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(ray_surface, ray_color, points)
        screen.blit(ray_surface, (0, 0))


# Create corals on rocks
coral_list = []
coral_types = ["branch", "brain", "plate", "tube", "fan"]
coral_colors = [
    (255, 100, 150),  # Pink
    (150, 100, 255),  # Purple
    (100, 255, 150),  # Green
    (255, 200, 100),  # Orange
    (100, 200, 255),  # Light blue
    (255, 150, 200),  # Light pink
    (200, 100, 200),  # Magenta
    (100, 255, 200),  # Cyan-green
    (255, 255, 150),  # Yellow
]

# Place corals on top of each rock
for rock in rocks:
    num_corals = random.randint(3, 5)
    for _ in range(num_corals):
        x = rock.x + random.randint(20, rock.width - 20)
        y = rock.y - random.randint(5, 15)  # Slightly above rock surface
        coral_type = random.choice(coral_types)
        color = random.choice(coral_colors)
        coral_list.append(Coral(x, y, coral_type, color))

# Create kelp in background
kelp_list = []
kelp_positions = [150, 300, 500, 750, 950, 1100]  # Spread across tank
for x_pos in kelp_positions:
    kelp_list.append(Kelp(x_pos))

# Create treasure chests (on pirate ship deck) with staggered opening
treasure_chests = []
ship_deck_y = 450  # Top of ship hull
chest_data = [
    (WIDTH // 2 - 300, ship_deck_y - 30, 0),      # Left: opens immediately
    (WIDTH // 2, ship_deck_y - 30, 300),          # Center: opens after 5 sec
    (WIDTH // 2 + 300, ship_deck_y - 30, 600)     # Right: opens after 10 sec
]
for x, y, delay in chest_data:
    treasure_chests.append(TreasureChest(x, y, delay))

# Create pirate ship
pirate_ship = PirateShip()

# Create light rays
light_rays = []
ray_positions = [200, 500, 800, 1000]
for x_pos in ray_positions:
    light_rays.append(LightRay(x_pos))

# Bubble list
bubble_list = []

# Water Chemistry System


class WaterChemistry:
    def __init__(self):
        self.nitrates = 0  # Start with clean water
        self.max_nitrates = 100

    def add_waste(self, amount):
        """Add nitrates from fish waste or decaying food"""
        self.nitrates = min(self.nitrates + amount, self.max_nitrates)

    def water_change(self, percentage):
        """Reduce nitrates through water change"""
        self.nitrates *= (1 - percentage)

    def get_health_status(self):
        """Return tank health based on nitrates"""
        if self.nitrates < 20:
            return "Excellent", GREEN
        elif self.nitrates < 50:
            return "Good", YELLOW
        else:
            return "Poor", RED

    def affects_fish_health(self):
        """High nitrates slow fish down and stress them"""
        if self.nitrates > 60:
            return 0.5  # Fish move at half speed
        elif self.nitrates > 40:
            return 0.8  # Fish move at 80% speed
        return 1.0  # Normal speed

# Food Particle System


class FoodParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 4
        self.age = 0
        self.max_age = 600  # 10 seconds at 60 FPS
        self.eaten = False
        self.sinking_speed = 0.5

    def update(self):
        """Food sinks slowly and ages"""
        self.age += 1
        self.y += self.sinking_speed

    def is_expired(self):
        """Food decays after max_age or reaches bottom"""
        return self.age > self.max_age or self.y > 690

    def draw(self, screen):
        """Draw food as a flashing pellet"""
        # Strobe flash effect - alternate between bright and normal
        if self.age % 10 < 5:  # Flash every 10 frames
            color = (255, 200, 100)  # Bright orange/yellow
        else:
            color = (139, 90, 43)  # Normal brown

        pygame.draw.circle(
            screen, color, (int(self.x), int(self.y)), self.size)


# Initialize systems
water_chemistry = WaterChemistry()
food_particles = []
algae_patches = []
algae_spawn_timer = 0

# Font for UI
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)
small_font = pygame.font.SysFont('Arial', 16)


def draw_ui():
    """Draw water chemistry and instructions"""
    # Background panel for UI
    ui_panel = pygame.Rect(10, 10, 320, 210)
    pygame.draw.rect(screen, (0, 0, 0, 128), ui_panel)
    pygame.draw.rect(screen, WHITE, ui_panel, 2)

    # Water chemistry status
    status, color = water_chemistry.get_health_status()
    nitrate_text = font.render(
        f"Nitrates: {int(water_chemistry.nitrates)}/100", True, WHITE)
    status_text = font.render(f"Status: {status}", True, color)
    screen.blit(nitrate_text, (20, 20))
    screen.blit(status_text, (20, 45))
    
    # Fish style display
    style_text = font.render(f"Fish Style: {fish_style_names[fish_style]}", True, (100, 200, 255))
    screen.blit(style_text, (20, 75))
    
    # Background scene display
    scene_color = (255, 200, 100) if background_scene > 0 else (150, 150, 150)
    scene_text = font.render(f"Scene: {background_scene_names[background_scene]}", True, scene_color)
    screen.blit(scene_text, (20, 100))

    # Instructions
    instruction1 = small_font.render("Click: Food | W: Water | F: Fish Style", True, WHITE)
    instruction2 = small_font.render("1-4: Nature | 5-8: Military", True, WHITE)
    instruction3 = small_font.render("B: Cycle Scene | 0: Scene Off | H: Hide UI", True, (255, 200, 100))
    screen.blit(instruction1, (20, 130))
    screen.blit(instruction2, (20, 150))
    screen.blit(instruction3, (20, 170))


def draw_gradient_background():
    """Draw ocean with depth gradient (lighter at top, darker at bottom)"""
    for y in range(HEIGHT):
        # Interpolate between light and dark blue based on depth
        ratio = y / HEIGHT
        r = int(OCEAN_BLUE[0] + (OCEAN_DEEP[0] - OCEAN_BLUE[0]) * ratio)
        g = int(OCEAN_BLUE[1] + (OCEAN_DEEP[1] - OCEAN_BLUE[1]) * ratio)
        b = int(OCEAN_BLUE[2] + (OCEAN_DEEP[2] - OCEAN_BLUE[2]) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


def draw_sand():
    """Draw sandy bottom with some texture"""
    sand_rect = pygame.Rect(0, 700, WIDTH, 100)
    pygame.draw.rect(screen, SAND_COLOR, sand_rect)

    # Draw pre-generated sand grains (no flickering!)
    for grain in sand_grains:
        x, y, color = grain
        pygame.draw.circle(screen, color, (x, y), 1)


def draw_rocks():
    """Draw rock formations with simple shading"""
    for i, rock in enumerate(rocks):
        # Draw main rock body
        pygame.draw.rect(screen, ROCK_DARK, rock)

        # Add highlight on top-left for 3D effect
        highlight = pygame.Rect(
            rock.x, rock.y, rock.width // 2, rock.height // 3)
        pygame.draw.rect(screen, ROCK_LIGHT, highlight)

        # Draw pre-generated cracks (no flickering!)
        for crack in rock_details[i]:
            start, end = crack
            pygame.draw.line(screen, (60, 50, 40), start, end, 2)


# Main game loop
running = True
frame_count = 0
while running:
    frame_count += 1

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                # Water change
                water_chemistry.water_change(0.25)
            if event.key == pygame.K_f:
                # Cycle fish style
                fish_style = (fish_style + 1) % 8
            if event.key == pygame.K_1:
                fish_style = 0  # Realistic
            if event.key == pygame.K_2:
                fish_style = 1  # Cartoon
            if event.key == pygame.K_3:
                fish_style = 2  # Pixel
            if event.key == pygame.K_4:
                fish_style = 3  # Tropical
            if event.key == pygame.K_5:
                fish_style = 4  # Army
            if event.key == pygame.K_6:
                fish_style = 5  # Air Force
            if event.key == pygame.K_7:
                fish_style = 6  # Space Force
            if event.key == pygame.K_8:
                fish_style = 7  # Navy
            if event.key == pygame.K_b:
                # Cycle background scene
                background_scene = (background_scene + 1) % 6
            if event.key == pygame.K_0:
                background_scene = 0  # None
            if event.key == pygame.K_h:
                # Toggle UI visibility
                ui_visible = not ui_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Drop food where clicked
            mx, my = pygame.mouse.get_pos()
            food_particles.append(FoodParticle(mx, my))

    # Update food particles
    for food in food_particles[:]:
        food.update()
        if food.is_expired():
            # Uneaten food decays and adds nitrates
            if not food.eaten:
                water_chemistry.add_waste(2)
            food_particles.remove(food)

    # Fish naturally produce waste over time
    if frame_count % 120 == 0:  # Every 2 seconds
        water_chemistry.add_waste(0.5)

    # Auto-feed pellets every 3 seconds
    if frame_count % 180 == 0:  # Every 3 seconds
        # Random position in center area of tank
        auto_feed_x = random.randint(150, WIDTH - 150)
        auto_feed_y = random.randint(100, 400)
        food_particles.append(FoodParticle(auto_feed_x, auto_feed_y))

    # Spawn algae when nitrates are high
    algae_spawn_timer += 1
    if algae_spawn_timer > 180 and water_chemistry.nitrates > 25:    # Every 3 seconds
        algae_spawn_timer = 0

        # Spawn multiple algae patches (more when nitrates are higher)
        num_spawns = 2 if water_chemistry.nitrates > 50 else 1
        num_spawns = 3 if water_chemistry.nitrates > 75 else num_spawns

        for _ in range(num_spawns):
            # Spawn on rocks or sand (but not near edges!)
            if random.random() < 0.5 and len(rocks) > 0:
                # Spawn on a random rock
                rock = random.choice(rocks)
                x = rock.x + random.randint(0, rock.width)
                y = rock.y + random.randint(0, rock.height)
            else:
                # Spawn on sand
                x = random.randint(100, WIDTH - 100)  # Keep away from edges
                y = random.randint(700, 780)

            # Only spawn if not too close to edges
            if 100 < x < WIDTH - 100 and 100 < y < 680:
                algae_patches.append(AlgaePatch(x, y))

    # Update algae growth
    for algae in algae_patches[:]:
        algae.grow(water_chemistry.nitrates)
        if algae.is_dead():
            algae_patches.remove(algae)

    # Draw everything (back to front layering)
    draw_gradient_background()

    # Light rays (very back, behind everything)
    for ray in light_rays:
        ray.update()
        ray.draw(screen)

    draw_sand()

    # Pirate ship (deep background)
    pirate_ship.update()
    pirate_ship.draw(screen)

    # Update and draw kelp (behind rocks)
    for kelp in kelp_list:
        kelp.update()
        kelp.draw(screen)

    draw_rocks()

    # Treasure chests on sand
    for chest in treasure_chests:
        chest.update(bubble_list)
        chest.draw(screen)

    # Update and draw corals
    for coral in coral_list:
        coral.update()
        coral.draw(screen)

    # Draw food particles
    for food in food_particles:
        if not food.eaten:
            food.draw(screen)

    # Draw algae
    for algae in algae_patches:
        algae.draw(screen)

    # Update and draw bubbles (in front of most things)
    for bubble in bubble_list[:]:
        bubble.update()
        if bubble.is_expired():
            bubble_list.remove(bubble)
        else:
            bubble.draw(screen)

    # Update and draw breeder fish
    for fish in fish_list:
        fish.update(food_particles, water_chemistry, algae_patches)
        fish.draw(screen)

    # Update and draw feeder fish
    for feeder in feeder_fish_list[:]:
        feeder.update(predator_fish_list)
        feeder.draw(screen)

    # Update and draw predator fish
    for predator in predator_fish_list:
        caught_fish = predator.update(feeder_fish_list, predator_fish_list)
        if caught_fish:
            feeder_fish_list.remove(caught_fish)
        predator.draw(screen)

    # Theatre layer - draws ABOVE all aquarium elements at BG_Y line
    if background_scene == 1:
        bg_whale.update()
        bg_whale.draw(screen)
    elif background_scene == 2:
        bg_tank.update()
        bg_tank.draw(screen)
    elif background_scene == 3:
        bg_jet.update()
        bg_jet.draw(screen)
    elif background_scene == 4:
        bg_battleship.update()
        bg_battleship.draw(screen)
    elif background_scene == 5:
        bg_shuttle.update()
        bg_shuttle.draw(screen)

    # Draw UI (toggleable with H key)
    if ui_visible:
        draw_ui()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
