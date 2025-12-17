# bizarro_slayer_game.py
import pygame
import sys
import random
import math
import os
import csv
import time

# Inicializar Pygame
pygame.init()

# Constantes del juego
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (30, 30, 50)
GRASS_GREEN = (76, 153, 0)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
DARK_PURPLE = (75, 0, 130)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)
SILVER = (192, 192, 192)

# Función para reiniciar Pygame completamente
def reiniciar_pygame_completamente():
    """Cierra y re-inicializa Pygame completamente"""
    try:
        # Cerrar todo
        pygame.display.quit()
        pygame.quit()
    except:
        pass
    
    # Pequeña pausa
    time.sleep(0.2)
    
    # Re-inicializar
    pygame.init()

# Función para limpiar Pygame sin cerrarlo
def limpiar_estado_pygame():
    """Limpia el estado de Pygame entre partidas"""
    pygame.event.clear()
    if pygame.display.get_init():
        # Limpiar cualquier superficie de display existente
        screen = pygame.display.get_surface()
        if screen:
            screen.fill(BLACK)
            pygame.display.flip()
    time.sleep(0.1)

# Crear sprites simples usando Pygame
def crear_sprite_jugador():
    """Crea un sprite simple para el jugador"""
    surface = pygame.Surface((40, 60), pygame.SRCALPHA)
    
    # Cuerpo (armadura)
    pygame.draw.rect(surface, LIGHT_BLUE, (5, 15, 30, 35))
    
    # Cabeza
    pygame.draw.circle(surface, (255, 220, 177), (20, 10), 10)
    
    # Ojos
    pygame.draw.circle(surface, BLACK, (15, 8), 2)
    pygame.draw.circle(surface, BLACK, (25, 8), 2)
    
    # Brazos
    pygame.draw.rect(surface, LIGHT_BLUE, (0, 20, 5, 15))
    pygame.draw.rect(surface, LIGHT_BLUE, (35, 20, 5, 15))
    
    # Piernas
    pygame.draw.rect(surface, BLUE, (10, 50, 8, 10))
    pygame.draw.rect(surface, BLUE, (22, 50, 8, 10))
    
    return surface

def crear_sprite_monstruo(tipo, color):
    """Crea sprites simples para los monstruos"""
    if "Boss" in tipo:
        surface = pygame.Surface((80, 80), pygame.SRCALPHA)
    else:
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    if tipo == "Rana Prisma":
        # Cuerpo de rana
        pygame.draw.ellipse(surface, color, (5, 10, 40, 30))
        
        # Ojos saltones
        pygame.draw.circle(surface, WHITE, (15, 15), 8)
        pygame.draw.circle(surface, WHITE, (35, 15), 8)
        pygame.draw.circle(surface, BLACK, (15, 15), 4)
        pygame.draw.circle(surface, BLACK, (35, 15), 4)
        
        # Boca
        pygame.draw.arc(surface, BLACK, (15, 25, 20, 10), 0, math.pi, 2)
        
    elif tipo == "Molusco Óseo":
        # Concha espiral
        pygame.draw.circle(surface, color, (25, 25), 20)
        pygame.draw.circle(surface, (color[0]-30, color[1]-30, color[2]-30), (25, 25), 15)
        
        # Ojos en tentáculos
        pygame.draw.line(surface, color, (15, 10), (10, 5), 3)
        pygame.draw.line(surface, color, (35, 10), (40, 5), 3)
        pygame.draw.circle(surface, WHITE, (10, 5), 4)
        pygame.draw.circle(surface, WHITE, (40, 5), 4)
        pygame.draw.circle(surface, BLACK, (10, 5), 2)
        pygame.draw.circle(surface, BLACK, (40, 5), 2)
        
    elif tipo == "Gusano de Reloj":
        # Cuerpo segmentado
        for i in range(4):
            pygame.draw.ellipse(surface, color, (5 + i*10, 15, 15, 20))
        
        # Cara
        pygame.draw.circle(surface, WHITE, (20, 20), 6)
        pygame.draw.circle(surface, WHITE, (35, 20), 6)
        pygame.draw.circle(surface, BLACK, (20, 20), 3)
        pygame.draw.circle(surface, BLACK, (35, 20), 3)
        
        # Reloj en el cuerpo
        pygame.draw.circle(surface, YELLOW, (25, 35), 8)
        pygame.draw.line(surface, BLACK, (25, 35), (25, 30), 2)
        pygame.draw.line(surface, BLACK, (25, 35), (30, 35), 2)
        
    elif tipo == "Esqueleto Eléctrico":
        # Cuerpo de esqueleto
        pygame.draw.ellipse(surface, color, (10, 5, 30, 40))
        
        # Cabeza
        pygame.draw.circle(surface, WHITE, (25, 10), 8)
        
        # Ojos eléctricos
        pygame.draw.circle(surface, CYAN, (20, 8), 3)
        pygame.draw.circle(surface, CYAN, (30, 8), 3)
        
        # Costillas
        for i in range(3):
            pygame.draw.arc(surface, WHITE, (15, 15 + i*8, 20, 8), 0, math.pi, 2)
        
        # Rayos eléctricos
        pygame.draw.line(surface, YELLOW, (10, 25), (5, 20), 2)
        pygame.draw.line(surface, YELLOW, (40, 25), (45, 20), 2)
        
    elif tipo == "Fantasma de Lava":
        # Cuerpo fantasma
        pygame.draw.ellipse(surface, color, (10, 15, 30, 25))
        
        # Ojos de lava
        pygame.draw.circle(surface, RED, (20, 20), 4)
        pygame.draw.circle(surface, RED, (35, 20), 4)
        pygame.draw.circle(surface, YELLOW, (20, 20), 2)
        pygame.draw.circle(surface, YELLOW, (35, 20), 2)
        
        # Llamas
        puntos_llama = [(15, 40), (20, 35), (25, 40), (30, 35), (35, 40)]
        pygame.draw.polygon(surface, ORANGE, puntos_llama)
        
        # Efecto fantasma
        pygame.draw.arc(surface, (255, 100, 0), (15, 10, 20, 15), math.pi, 2*math.pi, 2)
        
    elif tipo == "Slime Cósmico":
        # Cuerpo de slime
        pygame.draw.ellipse(surface, color, (5, 10, 40, 30))
        
        # Ojos cósmicos
        pygame.draw.circle(surface, BLACK, (20, 20), 6)
        pygame.draw.circle(surface, CYAN, (20, 20), 4)
        pygame.draw.circle(surface, BLACK, (35, 20), 6)
        pygame.draw.circle(surface, CYAN, (35, 20), 4)
        pygame.draw.circle(surface, WHITE, (22, 18), 1)
        pygame.draw.circle(surface, WHITE, (37, 18), 1)
        
        # Estrellas en el cuerpo
        for i in range(3):
            x = 15 + i*10
            y = 35
            pygame.draw.polygon(surface, YELLOW, [
                (x, y-3), (x+2, y-1), (x+3, y), (x+2, y+1), (x, y+3),
                (x-2, y+1), (x-3, y), (x-2, y-1)
            ], 1)
    
    elif tipo == "Gárgola de Piedra":
        # Cuerpo de gárgola
        pygame.draw.ellipse(surface, color, (5, 5, 40, 40))
        
        # Alas
        pygame.draw.polygon(surface, (color[0]-20, color[1]-20, color[2]-20), 
                           [(5, 25), (0, 15), (10, 20)])
        pygame.draw.polygon(surface, (color[0]-20, color[1]-20, color[2]-20), 
                           [(45, 25), (50, 15), (40, 20)])
        
        # Cara de piedra
        pygame.draw.circle(surface, DARK_GRAY, (20, 20), 5)
        pygame.draw.circle(surface, DARK_GRAY, (35, 20), 5)
        pygame.draw.arc(surface, DARK_GRAY, (20, 25, 15, 10), 0, math.pi, 3)
        
    elif tipo == "Boss - Rey Esqueleto":
        # Corona
        pygame.draw.polygon(surface, GOLD, [
            (40, 5), (30, 15), (35, 15), (40, 10), (45, 15), (50, 15)
        ])
        # Cabeza
        pygame.draw.circle(surface, WHITE, (40, 20), 15)
        # Ojos rojos
        pygame.draw.circle(surface, RED, (35, 18), 4)
        pygame.draw.circle(surface, RED, (45, 18), 4)
        # Cuerpo
        pygame.draw.ellipse(surface, WHITE, (25, 30, 30, 30))
        # Costillas
        for i in range(4):
            pygame.draw.arc(surface, DARK_GRAY, (28, 35 + i*6, 24, 8), 0, math.pi, 2)
        # Espada
        pygame.draw.rect(surface, SILVER, (55, 35, 15, 3))
        pygame.draw.rect(surface, SILVER, (60, 30, 5, 10))
        # Aura de jefe
        pygame.draw.circle(surface, (255, 0, 0, 100), (40, 40), 35, 3)
        
    elif tipo == "Boss - Dragón Oscuro":
        # Cabeza
        pygame.draw.ellipse(surface, DARK_PURPLE, (20, 10, 40, 25))
        # Cuernos
        pygame.draw.polygon(surface, BLACK, [(25, 10), (20, 0), (30, 5)])
        pygame.draw.polygon(surface, BLACK, [(55, 10), (60, 0), (50, 5)])
        # Ojos
        pygame.draw.circle(surface, RED, (35, 20), 4)
        pygame.draw.circle(surface, RED, (45, 20), 4)
        # Cuerpo
        pygame.draw.ellipse(surface, DARK_PURPLE, (15, 30, 50, 30))
        # Alas
        pygame.draw.polygon(surface, (75, 0, 100), [(10, 40), (0, 20), (20, 30)])
        pygame.draw.polygon(surface, (75, 0, 100), [(70, 40), (80, 20), (60, 30)])
        # Fuego en boca
        pygame.draw.polygon(surface, ORANGE, [(40, 30), (35, 40), (45, 40)])
        pygame.draw.polygon(surface, YELLOW, [(40, 32), (37, 38), (43, 38)])
        
    elif tipo == "Boss - Golem de Titanio":
        # Cuerpo
        pygame.draw.rect(surface, GRAY, (20, 10, 40, 50))
        # Cabeza
        pygame.draw.rect(surface, DARK_GRAY, (25, 5, 30, 15))
        # Ojos azules
        pygame.draw.circle(surface, CYAN, (35, 12), 3)
        pygame.draw.circle(surface, CYAN, (45, 12), 3)
        # Brazos
        pygame.draw.rect(surface, GRAY, (10, 20, 15, 10))
        pygame.draw.rect(surface, GRAY, (55, 20, 15, 10))
        # Piernas
        pygame.draw.rect(surface, GRAY, (25, 60, 10, 15))
        pygame.draw.rect(surface, GRAY, (45, 60, 10, 15))
        # Reflejos metálicos
        pygame.draw.line(surface, LIGHT_GRAY, (25, 15), (35, 15), 2)
        pygame.draw.line(surface, LIGHT_GRAY, (40, 30), (40, 50), 2)
    
    return surface

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal=LIGHT_BLUE, color_hover=BLUE):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.fuente = pygame.font.Font(None, 36)
        self.hover = False
        
    def dibujar(self, pantalla):
        # Dibujar botón
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, WHITE, self.rect, 3, border_radius=10)
        
        # Dibujar texto
        texto_surface = self.fuente.render(self.texto, True, WHITE)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        pantalla.blit(texto_surface, texto_rect)
        
    def actualizar(self, pos_mouse):
        # Verificar hover
        self.hover = self.rect.collidepoint(pos_mouse)
        self.color_actual = self.color_hover if self.hover else self.color_normal
        return self.hover
        
    def clic(self, pos_mouse, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(pos_mouse)
        return False

class SistemaOleadas:
    def __init__(self):
        self.oleada_actual = 1
        self.monstruos_restantes = 0
        self.tiempo_entre_oleadas = 300  # 5 segundos
        self.temporizador_oleada = 0
        self.oleada_activa = False
        self.boss_oleada = False
        
    def iniciar_oleada(self, oleada, nivel_jugador):
        """Inicia una nueva oleada"""
        self.oleada_actual = oleada
        self.oleada_activa = True
        
        # Verificar si es una oleada de jefe (cada 10 niveles del jugador)
        self.boss_oleada = (nivel_jugador % 10 == 0) and oleada > 1
        
        if self.boss_oleada:
            self.monstruos_restantes = 1
        else:
            base_monstruos = 3
            monstruos_extra = min(15, (oleada - 1) * 2)
            self.monstruos_restantes = base_monstruos + monstruos_extra
        
        return self.monstruos_restantes
    
    def monstruo_derrotado(self):
        """Registra un monstruo derrotado"""
        self.monstruos_restantes -= 1
        if self.monstruos_restantes <= 0:
            self.oleada_activa = False
            self.boss_oleada = False
            self.temporizador_oleada = self.tiempo_entre_oleadas
            return True
        return False
    
    def update(self):
        """Actualiza el sistema de oleadas"""
        if not self.oleada_activa and self.temporizador_oleada > 0:
            self.temporizador_oleada -= 1
            if self.temporizador_oleada <= 0:
                return self.oleada_actual + 1
        return None

class Player:
    def __init__(self, x, y, nombre, pros_sel, contras_sel):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.width = 40
        self.height = 60
        
        # Crear sprite del jugador
        self.sprite = crear_sprite_jugador()
        self.sprite_hurt = self.crear_sprite_hurt()
        
        # Aplicar pros y contras
        self.atk = 10 + sum(self.get_pro_value(p, "atk") for p in pros_sel) + sum(self.get_contra_value(c, "atk") for c in contras_sel)
        self.max_hp = 100 + sum(self.get_pro_value(p, "hp") for p in pros_sel) + sum(self.get_contra_value(c, "hp") for c in contras_sel)
        self.hp = self.max_hp
        self.speed = 5 + sum(self.get_pro_value(p, "speed") for p in pros_sel) + sum(self.get_contra_value(c, "speed") for c in contras_sel)
        self.regen = sum(self.get_pro_value(p, "regen") for p in pros_sel)
        self.bleed = sum(self.get_contra_value(c, "bleed") for c in contras_sel)
        self.crit_chance = 0.05 + sum(self.get_pro_value(p, "crit") for p in pros_sel) + sum(self.get_contra_value(c, "crit") for c in contras_sel)
        self.evade = 0.0 + sum(self.get_pro_value(p, "evade") for p in pros_sel) + sum(self.get_contra_value(c, "evade") for c in contras_sel)
        self.gold_mult = 1.0
        
        # Aplicar multiplicadores
        for p in pros_sel:
            if "Oro +25%" in p:
                self.gold_mult *= 1.25
        for c in contras_sel:
            if "Maldición" in c:
                self.gold_mult *= 0.75
        
        # Estado del jugador
        self.direction = "down"
        self.animation_frame = 0
        self.attack_cooldown = 0
        self.heal_cooldown = 0
        self.hurt_timer = 0
        self.gold = 0
        self.score = 0
        self.wins = 0
        self.experiencia = 0
        self.nivel = 1
        self.last_regen_time = 0
        
    def ganar_experiencia(self, exp):
        """Gana experiencia y sube de nivel"""
        self.experiencia += exp
        nivel_anterior = self.nivel
        self.nivel = max(1, self.experiencia // 100 + 1)
        
        if self.nivel > nivel_anterior:
            self.max_hp += 10
            self.atk += 2
            self.hp = self.max_hp
            return True
        return False
        
    def crear_sprite_hurt(self):
        """Crea una versión roja del sprite para cuando recibe daño"""
        sprite = self.sprite.copy()
        pixels = pygame.PixelArray(sprite)
        pixels.replace(LIGHT_BLUE, RED)
        pixels.replace(BLUE, (150, 0, 0))
        del pixels
        return sprite
        
    def get_pro_value(self, pro, stat):
        """Obtiene el valor de un pro"""
        pros_data = {
            "Fuerza +5": {"atk": 5},
            "Vida +20": {"hp": 20},
            "Crítico +10%": {"crit": 0.10},
            "Regeneración +3/turno": {"regen": 3},
            "Velocidad +2": {"speed": 2},
            "Evasión +10%": {"evade": 0.10},
            "Oro +25%": {"gold_mult": 1.25},
        }
        return pros_data.get(pro, {}).get(stat, 0)
    
    def get_contra_value(self, contra, stat):
        """Obtiene el valor de una contra"""
        contras_data = {
            "Fragilidad -15 HP": {"hp": -15},
            "Sangrado constante -2/turno": {"bleed": 2},
            "Pereza -2 velocidad": {"speed": -2},
            "Debilidad -3 fuerza": {"atk": -3},
            "Miedo -10% crítico": {"crit": -0.10},
            "Torpeza -10% esquiva": {"evade": -0.10},
            "Maldición: menos de 25% oro": {"gold_mult": 0.75}
        }
        return contras_data.get(contra, {}).get(stat, 0)
    
    def move(self, dx, dy, walls):
        """Mueve al jugador"""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Actualizar dirección
        if dx > 0: self.direction = "right"
        elif dx < 0: self.direction = "left"
        if dy > 0: self.direction = "down"
        elif dy < 0: self.direction = "up"
        
        # Verificar colisiones
        player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        collision = False
        for wall in walls:
            if player_rect.colliderect(wall):
                collision = True
                break
                
        if not collision:
            self.x = new_x
            self.y = new_y
            
        # Animación
        if dx != 0 or dy != 0:
            self.animation_frame = (self.animation_frame + 1) % 30
    
    def attack(self):
        """Realiza un ataque"""
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 20
            damage = self.atk
            if random.random() < self.crit_chance:
                damage *= 2
            return damage
        return 0
    
    def heal(self):
        """Se cura a sí mismo"""
        if self.heal_cooldown <= 0 and self.hp < self.max_hp:
            self.heal_cooldown = 90
            heal_amount = 25
            self.hp = min(self.max_hp, self.hp + heal_amount)
            return True
        return False
    
    def take_damage(self, damage):
        """Recibe daño"""
        if random.random() > self.evade:
            self.hp -= damage
            self.hurt_timer = 10
            return True
        return False
    
    def update(self):
        """Actualiza el estado del jugador"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_regen_time > 2000:
            self.last_regen_time = current_time
            self.hp = min(self.max_hp, self.hp + self.regen)
            self.hp -= self.bleed
            self.hp = max(0, self.hp)
    
    def draw(self, screen, camera_x, camera_y):
        """Dibuja al jugador usando sprites"""
        current_sprite = self.sprite_hurt if self.hurt_timer > 0 else self.sprite
        
        # Dibujar sprite
        screen.blit(current_sprite, (self.x - camera_x, self.y - camera_y))
        
        # Efecto de ataque
        if self.attack_cooldown > 15:
            attack_color = YELLOW
            if self.direction == "right":
                pygame.draw.line(screen, attack_color,
                                (self.x - camera_x + self.width, self.y - camera_y + self.height//2),
                                (self.x - camera_x + self.width + 30, self.y - camera_y + self.height//2), 4)
            elif self.direction == "left":
                pygame.draw.line(screen, attack_color,
                                (self.x - camera_x, self.y - camera_y + self.height//2),
                                (self.x - camera_x - 30, self.y - camera_y + self.height//2), 4)
            elif self.direction == "up":
                pygame.draw.line(screen, attack_color,
                                (self.x - camera_x + self.width//2, self.y - camera_y),
                                (self.x - camera_x + self.width//2, self.y - camera_y - 30), 4)
            elif self.direction == "down":
                pygame.draw.line(screen, attack_color,
                                (self.x - camera_x + self.width//2, self.y - camera_y + self.height),
                                (self.x - camera_x + self.width//2, self.y - camera_y + self.height + 30), 4)
        
        # Barra de vida
        bar_width = 50
        bar_height = 6
        pygame.draw.rect(screen, RED, 
                        (self.x - camera_x - 5, self.y - camera_y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - camera_x - 5, self.y - camera_y - 15, 
                         bar_width * (self.hp / self.max_hp), bar_height))

class Monster:
    def __init__(self, x, y, monster_type, oleada=1, es_boss=False):
        self.x = x
        self.y = y
        self.type = monster_type
        self.es_boss = es_boss
        
        if es_boss:
            self.width = 80
            self.height = 80
        else:
            self.width = 50
            self.height = 50
        
        monster_colors = {
            "Rana Prisma": (255, 100, 255),
            "Molusco Óseo": (150, 150, 255),
            "Gusano de Reloj": (200, 200, 0),
            "Esqueleto Eléctrico": (200, 200, 200),
            "Fantasma de Lava": (255, 100, 0),
            "Slime Cósmico": (100, 100, 255),
            "Gárgola de Piedra": (100, 100, 100),
            "Boss - Rey Esqueleto": (220, 220, 220),
            "Boss - Dragón Oscuro": (75, 0, 130),
            "Boss - Golem de Titanio": (150, 150, 150)
        }
        
        self.color = monster_colors.get(monster_type, (255, 255, 255))
        
        # Estadísticas base según tipo
        if es_boss:
            # JEFES
            if "Rey Esqueleto" in monster_type:
                base_hp = 500
                base_atk = 30
                base_speed = 2.0
            elif "Dragón Oscuro" in monster_type:
                base_hp = 800
                base_atk = 40
                base_speed = 2.5
            elif "Golem de Titanio" in monster_type:
                base_hp = 1000
                base_atk = 35
                base_speed = 1.5
            else:
                base_hp = 600
                base_atk = 35
                base_speed = 2.0
        else:
            # MONSTRUOS NORMALES
            stats = {
                "Rana Prisma": {"hp": 70, "atk": 12, "speed": 1.8},
                "Molusco Óseo": {"hp": 90, "atk": 14, "speed": 1.0},
                "Gusano de Reloj": {"hp": 80, "atk": 11, "speed": 1.5},
                "Esqueleto Eléctrico": {"hp": 95, "atk": 16, "speed": 1.6},
                "Fantasma de Lava": {"hp": 110, "atk": 18, "speed": 1.4},
                "Slime Cósmico": {"hp": 120, "atk": 13, "speed": 1.2},
                "Gárgola de Piedra": {"hp": 140, "atk": 20, "speed": 1.0}
            }
            base_stats = stats.get(monster_type, {"hp": 80, "atk": 12, "speed": 1.5})
            base_hp = base_stats["hp"]
            base_atk = base_stats["atk"]
            base_speed = base_stats["speed"]
        
        # Aplicar dificultad de oleada
        if es_boss:
            multiplicador_vida = 1.0 + (oleada - 1) * 0.5
            multiplicador_ataque = 1.0 + (oleada - 1) * 0.4
            multiplicador_velocidad = 1.0 + (oleada - 1) * 0.2
        else:
            multiplicador_vida = 1.0 + (oleada - 1) * 0.4
            multiplicador_ataque = 1.0 + (oleada - 1) * 0.3
            multiplicador_velocidad = 1.0 + (oleada - 1) * 0.15
        
        self.max_hp = int(base_hp * multiplicador_vida)
        self.atk = int(base_atk * multiplicador_ataque)
        self.speed = base_speed * multiplicador_velocidad
        self.oleada = oleada
            
        # Crear sprite del monstruo
        self.sprite = crear_sprite_monstruo(monster_type, self.color)
        
        self.hp = self.max_hp
        self.target_x = x
        self.target_y = y
        self.move_timer = 0
        self.attack_cooldown = 0
        self.detection_range = 250 if es_boss else 200
        self.update_counter = 0
        
    def update(self, player, walls):
        """Actualiza el monstruo"""
        self.update_counter += 1
        if self.update_counter % 2 != 0:
            return
            
        dx = player.x - self.x
        dy = player.y - self.y
        distance_squared = dx*dx + dy*dy
        
        if distance_squared < self.detection_range * self.detection_range:
            distance = math.sqrt(distance_squared)
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
                monster_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                for wall in walls:
                    if monster_rect.colliderect(wall):
                        self.x -= (dx / distance) * self.speed
                        self.y -= (dy / distance) * self.speed
                        break
        else:
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.target_x = self.x + random.randint(-50, 50)
                self.target_y = self.y + random.randint(-50, 50)
                self.move_timer = random.randint(90, 180)
                
            dx_target = self.target_x - self.x
            dy_target = self.target_y - self.y
            dist_target_squared = dx_target*dx_target + dy_target*dy_target
            
            if dist_target_squared > 25:
                dist_target = math.sqrt(dist_target_squared)
                if dist_target > 0:
                    self.x += (dx_target / dist_target) * self.speed * 0.3
                    self.y += (dy_target / dist_target) * self.speed * 0.3
                    
                    monster_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    for wall in walls:
                        if monster_rect.colliderect(wall):
                            self.x -= (dx_target / dist_target) * self.speed * 0.3
                            self.y -= (dy_target / dist_target) * self.speed * 0.3
                            break
                
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
    def attack(self):
        """El monstruo ataca"""
        if self.attack_cooldown <= 0:
            if self.es_boss:
                self.attack_cooldown = 40
            else:
                self.attack_cooldown = 50
            return self.atk
        return 0
        
    def take_damage(self, damage):
        """El monstruo recibe daño"""
        self.hp -= damage
        return self.hp <= 0
        
    def draw(self, screen, camera_x, camera_y):
        """Dibuja el monstruo usando sprites"""
        screen.blit(self.sprite, (self.x - camera_x, self.y - camera_y))
        
        if self.es_boss:
            bar_width = 80
            bar_height = 8
            bar_y_offset = -25
        else:
            bar_width = 50
            bar_height = 6
            bar_y_offset = -15
        
        pygame.draw.rect(screen, RED, 
                        (self.x - camera_x, self.y - camera_y + bar_y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - camera_x, self.y - camera_y + bar_y_offset, 
                         bar_width * (self.hp / self.max_hp), bar_height))
        
        if self.es_boss:
            font = pygame.font.Font(None, 24)
            text_surface = font.render("BOSS", True, RED)
            screen.blit(text_surface, (self.x - camera_x + 25, self.y - camera_y - 40))
        
        elif self.oleada >= 3:
            nivel_text = f"Oleada {self.oleada}"
            font = pygame.font.Font(None, 16)
            text_surface = font.render(nivel_text, True, ORANGE)
            screen.blit(text_surface, (self.x - camera_x, self.y - camera_y - 30))

def generar_monstruos_oleada(monstruos, map_width, map_height, oleada, cantidad, nivel_jugador, es_boss_oleada):
    """Genera monstruos para una oleada específica"""
    monstruos.clear()
    
    if es_boss_oleada:
        x = map_width // 2
        y = map_height // 2
        
        if nivel_jugador >= 30:
            boss_type = "Boss - Golem de Titanio"
        elif nivel_jugador >= 20:
            boss_type = "Boss - Dragón Oscuro"
        else:
            boss_type = "Boss - Rey Esqueleto"
        
        monstruos.append(Monster(x, y, boss_type, oleada, es_boss=True))
        
    else:
        monster_types = [
            "Rana Prisma", "Molusco Óseo", "Gusano de Reloj",
            "Esqueleto Eléctrico", "Fantasma de Lava", 
            "Slime Cósmico", "Gárgola de Piedra"
        ]
        
        for _ in range(cantidad):
            x = random.randint(100, map_width - 100)
            y = random.randint(100, map_height - 100)
            
            rand = random.random()
            if oleada >= 8 and rand < 0.3:
                monster_type = "Gárgola de Piedra"
            elif oleada >= 6 and rand < 0.4:
                monster_type = "Fantasma de Lava"
            elif oleada >= 4 and rand < 0.5:
                monster_type = "Esqueleto Eléctrico"
            elif oleada >= 3 and rand < 0.6:
                monster_type = "Slime Cósmico"
            elif oleada >= 5 and rand < 0.5:
                monster_type = "Molusco Óseo"
            elif oleada >= 3 and rand < 0.4:
                monster_type = "Gusano de Reloj"
            else:
                monster_type = random.choice(monster_types)
                
            monstruos.append(Monster(x, y, monster_type, oleada))

def mostrar_pantalla_pausa(pantalla):
    """Muestra la pantalla de pausa"""
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_texto = pygame.font.Font(None, 36)
    
    boton_continuar = Boton(SCREEN_WIDTH//2 - 150, 300, 300, 60, "CONTINUAR", GREEN, (0, 200, 0))
    boton_salir = Boton(SCREEN_WIDTH//2 - 150, 400, 300, 60, "SALIR AL MENÚ", RED, (200, 0, 0))
    
    ejecutando = True
    decision = "continuar"
    
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                decision = "salir"
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    decision = "continuar"
                    ejecutando = False
            
            if boton_continuar.clic(pos_mouse, evento):
                decision = "continuar"
                ejecutando = False
            if boton_salir.clic(pos_mouse, evento):
                decision = "salir_menu"
                ejecutando = False
        
        fondo = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 200))
        pantalla.blit(fondo, (0, 0))
        
        titulo = fuente_titulo.render("PAUSA", True, YELLOW)
        pantalla.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 150))
        
        instrucciones = fuente_texto.render("Juego en pausa", True, WHITE)
        pantalla.blit(instrucciones, (SCREEN_WIDTH//2 - instrucciones.get_width()//2, 230))
        
        boton_continuar.actualizar(pos_mouse)
        boton_salir.actualizar(pos_mouse)
        boton_continuar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    return decision

def mostrar_pantalla_victoria(pantalla, oleada, puntuacion, oro, nivel, es_boss=False):
    """Muestra la pantalla de victoria después de completar una oleada"""
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_texto = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    boton_continuar = Boton(SCREEN_WIDTH//2 - 150, 400, 300, 60, "CONTINUAR SIGUIENTE OLEADA", GREEN, (0, 200, 0))
    boton_salir = Boton(SCREEN_WIDTH//2 - 150, 480, 300, 60, "GUARDAR Y SALIR", RED, (200, 0, 0))
    
    ejecutando = True
    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            
            if boton_continuar.clic(pos_mouse, evento):
                return "continuar"
            if boton_salir.clic(pos_mouse, evento):
                return "salir"
        
        fondo = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 200))
        pantalla.blit(fondo, (0, 0))
        
        if es_boss:
            titulo = fuente_titulo.render(f"¡JEFE DERROTADO!", True, GOLD)
            subtitulo = fuente_texto.render(f"Nivel {nivel} completado", True, YELLOW)
        else:
            titulo = fuente_titulo.render(f"¡OLEADA {oleada} COMPLETADA!", True, GOLD)
            subtitulo = None
        
        pantalla.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 100))
        if subtitulo:
            pantalla.blit(subtitulo, (SCREEN_WIDTH//2 - subtitulo.get_width()//2, 170))
        
        stats_y = 200 if not es_boss else 220
        estadisticas = [
            f"Puntuación Total: {puntuacion}",
            f"Oro Acumulado: {oro}",
            f"Nivel Actual: {nivel}",
            f"Oleada Superada: {oleada}"
        ]
        
        for stat in estadisticas:
            texto = fuente_texto.render(stat, True, WHITE)
            pantalla.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, stats_y))
            stats_y += 50
        
        if es_boss:
            recompensa = fuente_pequena.render("¡Recompensa extra por derrotar al jefe!", True, YELLOW)
        else:
            recompensa = fuente_pequena.render("¡Has recibido recompensas por completar la oleada!", True, YELLOW)
        pantalla.blit(recompensa, (SCREEN_WIDTH//2 - recompensa.get_width()//2, 350))
        
        boton_continuar.actualizar(pos_mouse)
        boton_salir.actualizar(pos_mouse)
        boton_continuar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    return "salir"

def mostrar_pantalla_muerte(pantalla, player, oleada_actual):
    """Muestra la pantalla de muerte del jugador"""
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_texto = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    # Mostrar pantalla inmediatamente
    pantalla.fill((30, 0, 0))
    
    titulo = fuente_titulo.render("¡HAS MUERTO!", True, RED)
    pantalla.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 100))
    
    stats = [
        f"Nombre: {player.nombre}",
        f"Oleada alcanzada: {oleada_actual}",
        f"Nivel alcanzado: {player.nivel}",
        f"Puntuación final: {player.score}",
        f"Oro recolectado: {player.gold}",
        f"Monstruos derrotados: {player.wins}"
    ]
    
    y_pos = 200
    for stat in stats:
        texto = fuente_texto.render(stat, True, WHITE)
        pantalla.blit(texto, (SCREEN_WIDTH//2 - texto.get_width()//2, y_pos))
        y_pos += 50
    
    instruccion1 = fuente_pequena.render("Tu progreso ha sido guardado automáticamente", True, YELLOW)
    instruccion2 = fuente_pequena.render("Presiona cualquier tecla para volver al menú", True, YELLOW)
    
    pantalla.blit(instruccion1, (SCREEN_WIDTH//2 - instruccion1.get_width()//2, 500))
    pantalla.blit(instruccion2, (SCREEN_WIDTH//2 - instruccion2.get_width()//2, 530))
    
    pygame.display.flip()
    
    # Esperar un momento antes de aceptar input
    pygame.time.wait(500)
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                return
            elif evento.type == pygame.KEYDOWN:
                ejecutando = False
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                ejecutando = False
                return
        
        pygame.time.Clock().tick(FPS)
    
    # Limpiar eventos
    pygame.event.clear()

def save_player(name, score, wins, pros_sel, contras_sel):
    """Guarda el progreso del jugador"""
    if not os.path.exists("historial.csv"):
        with open("historial.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Jugador", "Puntos", "Victorias", "Pros", "Contras"])
    
    with open("historial.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, score, wins, ";".join(pros_sel), ";".join(contras_sel)])

def iniciar_juego_pygame(nombre, pros_sel, contras_sel):
    """Función principal del juego Pygame"""
    # Variable para controlar si hubo muerte
    muerte_ocurrida = False
    
    try:
        # Verificar si Pygame está inicializado
        if not pygame.get_init():
            pygame.init()
        
        # Crear la ventana
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"Bizarro Slayer - {nombre}")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 20)
        
        # Crear mapa
        map_width, map_height = 1500, 1500
        
        walls = [
            pygame.Rect(300, 300, 200, 50),
            pygame.Rect(600, 500, 50, 200),
            pygame.Rect(800, 200, 300, 50),
            pygame.Rect(1000, 600, 200, 50),
            pygame.Rect(200, 100, 100, 300),
            pygame.Rect(400, 700, 250, 40),
            pygame.Rect(700, 400, 40, 200),
            pygame.Rect(900, 100, 40, 150),
            pygame.Rect(1200, 300, 200, 40),
            pygame.Rect(100, 500, 150, 40),
            pygame.Rect(500, 200, 40, 100),
            pygame.Rect(1100, 500, 40, 200),
            pygame.Rect(300, 800, 300, 40),
            pygame.Rect(1300, 100, 40, 200),
        ]
        
        # Crear jugador
        player = Player(map_width//2, map_height//2, nombre, pros_sel, contras_sel)
        
        # Sistema de oleadas
        sistema_oleadas = SistemaOleadas()
        oleada_actual = 1
        monstruos = []
        
        # Iniciar primera oleada
        total_monstruos = sistema_oleadas.iniciar_oleada(oleada_actual, player.nivel)
        generar_monstruos_oleada(monstruos, map_width, map_height, oleada_actual, total_monstruos, player.nivel, sistema_oleadas.boss_oleada)
        
        # Cámara
        camera_x, camera_y = 0, 0
        
        # Estado del juego
        game_state = "explore"
        current_monster = None
        battle_cooldown = 0
        mensaje_oleada = ""
        mensaje_timer = 0
        nivel_subido = False
        mostrar_pantalla_victoria_flag = False
        pausado = False
        es_boss_oleada = False
        
        # Bucle principal del juego
        running = True
        while running:
            # Procesar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                    running = False
                    return "menu"
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_p:
                        pausado = not pausado
            
            # Si el juego está pausado, manejar la pantalla de pausa
            if pausado:
                decision = mostrar_pantalla_pausa(screen)
                
                if decision == "continuar":
                    pausado = False
                    pygame.event.clear()
                    continue
                elif decision == "salir_menu":
                    save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                    running = False
                    return "menu"
                elif decision == "salir":
                    save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                    running = False
                    return "salir"
            
            # Si debemos mostrar la pantalla de victoria
            if mostrar_pantalla_victoria_flag:
                decision = mostrar_pantalla_victoria(screen, oleada_actual, player.score, player.gold, player.nivel, es_boss_oleada)
                if decision == "continuar":
                    oleada_actual += 1
                    total_monstruos = sistema_oleadas.iniciar_oleada(oleada_actual, player.nivel)
                    generar_monstruos_oleada(monstruos, map_width, map_height, oleada_actual, total_monstruos, player.nivel, sistema_oleadas.boss_oleada)
                    mostrar_pantalla_victoria_flag = False
                    es_boss_oleada = False
                    player.hp = player.max_hp
                else:
                    save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                    running = False
                    return "menu"
                continue
            
            # Actualizar cámara
            camera_x = player.x - SCREEN_WIDTH // 2
            camera_y = player.y - SCREEN_HEIGHT // 2
            camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH))
            camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT))
            
            keys = pygame.key.get_pressed()
            
            # MOVIMIENTO - SIEMPRE ACTIVO (incluso en combate)
            dx, dy = 0, 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy = 1
            
            # Mover al jugador SIEMPRE
            if dx != 0 or dy != 0:
                player.move(dx, dy, walls)
            
            if game_state == "explore":
                # Verificar combate al explorar
                if battle_cooldown <= 0:
                    for monster in monstruos[:]:
                        distance = math.sqrt((player.x - monster.x)**2 + (player.y - monster.y)**2)
                        if distance < 80:
                            game_state = "battle"
                            current_monster = monster
                            battle_cooldown = 120
                            break
                            
            elif game_state == "battle":
                # COMBATE - se puede atacar y mover al mismo tiempo
                # ATAQUE con tecla E
                if keys[pygame.K_e] and player.attack_cooldown <= 0:
                    damage = player.attack()
                    if current_monster.take_damage(damage):
                        # Monstruo derrotado
                        if current_monster.es_boss:
                            experiencia = 200 + (current_monster.oleada * 20)
                            oro_recompensa = random.randint(100, 200) * player.gold_mult
                            es_boss_oleada = True
                        else:
                            experiencia = 20 + (current_monster.oleada * 5)
                            oro_recompensa = random.randint(10, 30) * player.gold_mult * current_monster.oleada
                        
                        nivel_subido = player.ganar_experiencia(experiencia)
                        
                        if current_monster.es_boss:
                            player.score += 500 * current_monster.oleada
                        else:
                            player.score += 100 * current_monster.oleada
                        
                        player.wins += 1
                        player.gold += int(oro_recompensa)
                        
                        monstruos.remove(current_monster)
                        
                        # Verificar si se completó la oleada
                        if sistema_oleadas.monstruo_derrotado():
                            if current_monster.es_boss:
                                mensaje_oleada = f"¡JEFE DERROTADO!"
                            else:
                                mensaje_oleada = f"¡Oleada {oleada_actual} completada!"
                            mensaje_timer = 180
                            pygame.time.set_timer(pygame.USEREVENT, 2000, True)
                        
                        game_state = "explore"
                        current_monster = None
                
                # CURACIÓN con tecla H
                if keys[pygame.K_h]:
                    if player.heal():
                        pass
                    
                # Ataque del monstruo
                if current_monster and current_monster.attack_cooldown <= 0:
                    if player.take_damage(current_monster.attack()):
                        if player.hp <= 0:
                            # JUGADOR MUERE
                            save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                            
                            # Marcar que hubo muerte
                            muerte_ocurrida = True
                            
                            # Mostrar pantalla de muerte
                            mostrar_pantalla_muerte(screen, player, oleada_actual)
                            
                            # Retornar al menú
                            return "menu"
                
                # Salir del combate con ESC
                if keys[pygame.K_ESCAPE]:
                    game_state = "explore"
                    current_monster = None
                    battle_cooldown = 60
            
            # Manejar evento de victoria
            for evento in pygame.event.get():
                if evento.type == pygame.USEREVENT:
                    mostrar_pantalla_victoria_flag = True
            
            # Actualizar sistema de oleadas
            if not mostrar_pantalla_victoria_flag:
                siguiente_oleada = sistema_oleadas.update()
                if siguiente_oleada:
                    oleada_actual = siguiente_oleada
                    total_monstruos = sistema_oleadas.iniciar_oleada(oleada_actual, player.nivel)
                    generar_monstruos_oleada(monstruos, map_width, map_height, oleada_actual, total_monstruos, player.nivel, sistema_oleadas.boss_oleada)
                    if sistema_oleadas.boss_oleada:
                        mensaje_oleada = f"¡OLEADA DE JEFE! Nivel {player.nivel}"
                    else:
                        mensaje_oleada = f"¡Oleada {oleada_actual} iniciada!"
                    mensaje_timer = 180
            
            # Actualizar entidades
            player.update()
            for monster in monstruos:
                monster.update(player, walls)
                
            if battle_cooldown > 0:
                battle_cooldown -= 1
                
            if mensaje_timer > 0:
                mensaje_timer -= 1
                
            # DIBUJADO
            screen.fill(GRASS_GREEN)
            
            # Solo dibujar paredes visibles
            for wall in walls:
                wall_rect = pygame.Rect(wall.x - camera_x, wall.y - camera_y, wall.width, wall.height)
                if wall_rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
                    pygame.draw.rect(screen, BROWN, wall_rect)
            
            # Dibujar monstruos
            for monster in monstruos:
                monster_rect = pygame.Rect(monster.x - camera_x, monster.y - camera_y, monster.width, monster.height)
                if monster_rect.colliderect(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
                    monster.draw(screen, camera_x, camera_y)
            
            # Dibujar jugador
            player.draw(screen, camera_x, camera_y)
            
            # UI MEJORADA
            panel_superior = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
            panel_superior.fill((0, 0, 0, 150))
            screen.blit(panel_superior, (0, 0))
            
            # Estadísticas del jugador
            stats_texts = [
                f"Oleada: {oleada_actual}",
                f"Monstruos: {sistema_oleadas.monstruos_restantes}",
                f"Nivel: {player.nivel}",
                f"EXP: {player.experiencia % 100}/100",
                f"Victorias: {player.wins}",
                f"Puntos: {player.score}",
                f"Oro: {player.gold}"
            ]
            
            for i, text in enumerate(stats_texts):
                screen.blit(small_font.render(text, True, WHITE), (10 + i * 150, 10))
            
            # Indicador de oleada de jefe
            if sistema_oleadas.boss_oleada:
                boss_text = f"¡OLEADA DE JEFE! - Nivel {player.nivel}"
                boss_surface = font.render(boss_text, True, RED)
                screen.blit(boss_surface, (SCREEN_WIDTH//2 - boss_surface.get_width()//2, 50))
            
            # Barra de vida del jugador
            vida_text = f"HP: {player.hp}/{player.max_hp}"
            screen.blit(font.render(vida_text, True, WHITE), (10, 40))
            bar_width = 200
            pygame.draw.rect(screen, RED, (80, 45, bar_width, 20))
            pygame.draw.rect(screen, GREEN, (80, 45, bar_width * (player.hp / player.max_hp), 20))
            pygame.draw.rect(screen, WHITE, (80, 45, bar_width, 20), 2)
            
            # Indicador de cooldown de curación
            if player.heal_cooldown > 0:
                cooldown_text = f"Cura: {player.heal_cooldown//60 + 1}s"
                screen.blit(small_font.render(cooldown_text, True, YELLOW), (290, 40))
            
            # Mensajes de oleada
            if mensaje_timer > 0:
                mensaje_surface = font.render(mensaje_oleada, True, YELLOW)
                screen.blit(mensaje_surface, (SCREEN_WIDTH//2 - mensaje_surface.get_width()//2, 100))
            
            # Mensaje de subida de nivel
            if nivel_subido:
                nivel_surface = font.render(f"¡Subiste al nivel {player.nivel}!", True, ORANGE)
                screen.blit(nivel_surface, (SCREEN_WIDTH//2 - nivel_surface.get_width()//2, 130))
                nivel_subido = False
            
            # Tiempo entre oleadas
            if not sistema_oleadas.oleada_activa and sistema_oleadas.temporizador_oleada > 0 and not mostrar_pantalla_victoria_flag:
                tiempo_restante = sistema_oleadas.temporizador_oleada // 60 + 1
                tiempo_surface = font.render(f"Siguiente oleada en: {tiempo_restante}s", True, LIGHT_BLUE)
                screen.blit(tiempo_surface, (SCREEN_WIDTH//2 - tiempo_surface.get_width()//2, 160))
            
            # Instrucciones de combate
            if game_state == "battle":
                panel_batalla = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
                panel_batalla.fill((0, 0, 0, 180))
                screen.blit(panel_batalla, (0, SCREEN_HEIGHT - 80))
                
                if current_monster.es_boss:
                    tipo_text = f"JEFE: {current_monster.type}"
                else:
                    tipo_text = f"Combatiendo: {current_monster.type} (Oleada {current_monster.oleada})"
                
                # INSTRUCCIONES MODIFICADAS: Ahora puedes moverte y atacar al mismo tiempo
                batalla_texts = [
                    tipo_text,
                    f"HP Enemigo: {current_monster.hp}/{current_monster.max_hp}",
                    "E: Atacar | H: Curar (+25 HP) | ESC: Huir",
                    "WASD: Moverse (funciona incluso en combate)"
                ]
                
                for i, text in enumerate(batalla_texts):
                    screen.blit(small_font.render(text, True, WHITE), 
                               (20, SCREEN_HEIGHT - 70 + i * 20))
            
            # Instrucciones generales
            instrucciones = small_font.render("P: Pausa", True, WHITE)
            screen.blit(instrucciones, (SCREEN_WIDTH - 120, 10))
            
            pygame.display.flip()
            clock.tick(FPS)
        
        # Si sale normalmente (no por muerte), guardar
        if player.hp > 0:
            save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
            
        return "menu"
            
    except Exception as e:
        print(f"Error durante el juego: {e}")
        import traceback
        traceback.print_exc()
        return "menu"
    finally:
        # Manejar limpieza diferente según si hubo muerte o no
        if muerte_ocurrida:
            # Si hubo muerte, limpiar Pygame
            try:
                pygame.quit()
            except:
                pass
        else:
            # Si no hubo muerte, solo limpiar el estado
            limpiar_estado_pygame()
    
    return "menu"