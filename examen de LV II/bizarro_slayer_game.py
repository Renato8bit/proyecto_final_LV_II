# bizarro_slayer_game.py
import pygame
import sys
import random
import math
import os
import csv

# Configuración de Pygame
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
        
    def iniciar_oleada(self, oleada):
        """Inicia una nueva oleada"""
        self.oleada_actual = oleada
        self.oleada_activa = True
        
        # Calcular número de monstruos basado en la oleada
        base_monstruos = 3
        monstruos_extra = min(10, (oleada - 1) * 2)  # Máximo 10 monstruos extra
        self.monstruos_restantes = base_monstruos + monstruos_extra
        
        return self.monstruos_restantes
    
    def monstruo_derrotado(self):
        """Registra un monstruo derrotado"""
        self.monstruos_restantes -= 1
        if self.monstruos_restantes <= 0:
            self.oleada_activa = False
            self.temporizador_oleada = self.tiempo_entre_oleadas
            return True  # Oleada completada
        return False
    
    def update(self):
        """Actualiza el sistema de oleadas"""
        if not self.oleada_activa and self.temporizador_oleada > 0:
            self.temporizador_oleada -= 1
            if self.temporizador_oleada <= 0:
                return self.oleada_actual + 1  # Iniciar siguiente oleada
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
        self.hurt_timer = 0
        self.gold = 0
        self.score = 0
        self.wins = 0
        self.experiencia = 0
        self.nivel = 1
        
    def ganar_experiencia(self, exp):
        """Gana experiencia y sube de nivel"""
        self.experiencia += exp
        nivel_anterior = self.nivel
        self.nivel = max(1, self.experiencia // 100 + 1)
        
        # Mejorar estadísticas al subir de nivel
        if self.nivel > nivel_anterior:
            self.max_hp += 5
            self.atk += 1
            self.hp = self.max_hp  # Curar completamente al subir de nivel
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
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        
        # Efectos pasivos
        self.hp = min(self.max_hp, self.hp + self.regen)
        self.hp -= self.bleed
        self.hp = max(0, self.hp)
    
    def draw(self, screen, camera_x, camera_y):
        """Dibuja al jugador usando sprites"""
        # Usar sprite normal o de daño
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
        
        # Barra de vida
        bar_width = 50
        bar_height = 6
        pygame.draw.rect(screen, RED, 
                        (self.x - camera_x - 5, self.y - camera_y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - camera_x - 5, self.y - camera_y - 15, 
                         bar_width * (self.hp / self.max_hp), bar_height))

class Monster:
    def __init__(self, x, y, monster_type, oleada=1):
        self.x = x
        self.y = y
        self.type = monster_type
        self.width = 50
        self.height = 50
        
        # Estadísticas base según tipo
        if monster_type == "Rana Prisma":
            self.color = (255, 100, 255)
            base_hp = 50
            base_atk = 9
            base_speed = 1.5
        elif monster_type == "Molusco Óseo":
            self.color = (150, 150, 255)
            base_hp = 70
            base_atk = 10
            base_speed = 0.8
        elif monster_type == "Gusano de Reloj":
            self.color = (200, 200, 0)
            base_hp = 60
            base_atk = 8
            base_speed = 1.2
        
        # Aplicar dificultad de oleada
        multiplicador_vida = 1.0 + (oleada - 1) * 0.3
        multiplicador_ataque = 1.0 + (oleada - 1) * 0.2
        multiplicador_velocidad = 1.0 + (oleada - 1) * 0.1
        
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
        self.detection_range = 150
        self.update_counter = 0
        
    def update(self, player, walls):
        """Actualiza el monstruo (CORREGIDO)"""
        # Solo actualizar cada 2 frames para optimizar
        self.update_counter += 1
        if self.update_counter % 2 != 0:
            return
            
        # Seguir al jugador si está cerca
        dx = player.x - self.x
        dy = player.y - self.y
        distance_squared = dx*dx + dy*dy
        
        if distance_squared < self.detection_range * self.detection_range:
            distance = math.sqrt(distance_squared)
            if distance > 0:  # CORRECCIÓN: Verificar que distance no sea 0
                # Perseguir al jugador
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                
                # Verificar colisiones con paredes después de mover
                monster_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                for wall in walls:
                    if monster_rect.colliderect(wall):
                        # Si hay colisión, revertir el movimiento
                        self.x -= (dx / distance) * self.speed
                        self.y -= (dy / distance) * self.speed
                        break
        else:
            # Movimiento aleatorio menos frecuente
            self.move_timer -= 1
            if self.move_timer <= 0:
                self.target_x = self.x + random.randint(-50, 50)
                self.target_y = self.y + random.randint(-50, 50)
                self.move_timer = random.randint(90, 180)
                
            # Moverse hacia el objetivo
            dx_target = self.target_x - self.x
            dy_target = self.target_y - self.y
            dist_target_squared = dx_target*dx_target + dy_target*dy_target
            
            if dist_target_squared > 25:  # CORRECCIÓN: Usar distancia al cuadrado para comparar
                dist_target = math.sqrt(dist_target_squared)
                if dist_target > 0:  # CORRECCIÓN: Verificar que dist_target no sea 0
                    self.x += (dx_target / dist_target) * self.speed * 0.3
                    self.y += (dy_target / dist_target) * self.speed * 0.3
                    
                    # Verificar colisiones con paredes
                    monster_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                    for wall in walls:
                        if monster_rect.colliderect(wall):
                            # Si hay colisión, revertir el movimiento
                            self.x -= (dx_target / dist_target) * self.speed * 0.3
                            self.y -= (dy_target / dist_target) * self.speed * 0.3
                            break
                
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
    def attack(self):
        """El monstruo ataca"""
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 60
            return self.atk
        return 0
        
    def take_damage(self, damage):
        """El monstruo recibe daño"""
        self.hp -= damage
        return self.hp <= 0
        
    def draw(self, screen, camera_x, camera_y):
        """Dibuja el monstruo usando sprites"""
        # Dibujar sprite
        screen.blit(self.sprite, (self.x - camera_x, self.y - camera_y))
        
        # Barra de vida
        bar_width = 50
        bar_height = 6
        pygame.draw.rect(screen, RED, 
                        (self.x - camera_x, self.y - camera_y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, 
                        (self.x - camera_x, self.y - camera_y - 15, 
                         bar_width * (self.hp / self.max_hp), bar_height))
        
        # Indicador de oleada para monstruos difíciles
        if self.oleada >= 3:
            nivel_text = f"Oleada {self.oleada}"
            font = pygame.font.Font(None, 16)
            text_surface = font.render(nivel_text, True, ORANGE)
            screen.blit(text_surface, (self.x - camera_x, self.y - camera_y - 30))

def generar_monstruos_oleada(monstruos, map_width, map_height, oleada, cantidad):
    """Genera monstruos para una oleada específica"""
    monstruos.clear()
    monster_types = ["Rana Prisma", "Molusco Óseo", "Gusano de Reloj"]
    
    # En oleadas altas, mayor probabilidad de monstruos más fuertes
    for _ in range(cantidad):
        x = random.randint(100, map_width - 100)
        y = random.randint(100, map_height - 100)
        
        # En oleadas altas, mayor probabilidad de monstruos fuertes
        if oleada >= 5 and random.random() < 0.6:
            monster_type = "Molusco Óseo"  # Más fuerte
        elif oleada >= 3 and random.random() < 0.4:
            monster_type = "Gusano de Reloj"  # Medio
        else:
            monster_type = random.choice(monster_types)
            
        monstruos.append(Monster(x, y, monster_type, oleada))

def mostrar_pantalla_victoria(pantalla, oleada, puntuacion, oro, nivel):
    """Muestra la pantalla de victoria después de completar una oleada"""
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_texto = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)
    
    # Crear botones
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
        
        # Fondo semitransparente
        fondo = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 200))
        pantalla.blit(fondo, (0, 0))
        
        # Título de victoria
        titulo = fuente_titulo.render(f"¡OLEADA {oleada} COMPLETADA!", True, GOLD)
        pantalla.blit(titulo, (SCREEN_WIDTH//2 - titulo.get_width()//2, 100))
        
        # Estadísticas
        stats_y = 200
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
        
        # Mensaje de recompensa
        recompensa = fuente_pequena.render("¡Has recibido recompensas por completar la oleada!", True, YELLOW)
        pantalla.blit(recompensa, (SCREEN_WIDTH//2 - recompensa.get_width()//2, 350))
        
        # Actualizar y dibujar botones
        boton_continuar.actualizar(pos_mouse)
        boton_salir.actualizar(pos_mouse)
        boton_continuar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    return "salir"

def save_player(name, score, wins, pros_sel, contras_sel):
    """Guarda el progreso del jugador"""
    # Asegurar que el archivo existe
    if not os.path.exists("historial.csv"):
        with open("historial.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Jugador", "Puntos", "Victorias", "Pros", "Contras"])
    
    # Guardar los datos
    with open("historial.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, score, wins, ";".join(pros_sel), ";".join(contras_sel)])

def iniciar_juego_pygame(nombre, pros_sel, contras_sel):
    """Función principal del juego Pygame CON SISTEMA DE OLEADAS Y PANTALLA DE VICTORIA"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Bizarro Slayer - {nombre}")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 20)
    
    # Crear mapa
    map_width, map_height = 1500, 1500
    
    # Paredes
    walls = [
        pygame.Rect(300, 300, 200, 50),
        pygame.Rect(600, 500, 50, 200),
        pygame.Rect(800, 200, 300, 50),
        pygame.Rect(1000, 600, 200, 50),
    ]
    
    # Crear jugador
    player = Player(map_width//2, map_height//2, nombre, pros_sel, contras_sel)
    
    # Sistema de oleadas
    sistema_oleadas = SistemaOleadas()
    oleada_actual = 1
    monstruos = []
    
    # Iniciar primera oleada
    total_monstruos = sistema_oleadas.iniciar_oleada(oleada_actual)
    generar_monstruos_oleada(monstruos, map_width, map_height, oleada_actual, total_monstruos)
    
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
    
    # Bucle principal del juego
    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
        
        # Si debemos mostrar la pantalla de victoria
        if mostrar_pantalla_victoria_flag:
            decision = mostrar_pantalla_victoria(screen, oleada_actual, player.score, player.gold, player.nivel)
            if decision == "continuar":
                oleada_actual += 1
                total_monstruos = sistema_oleadas.iniciar_oleada(oleada_actual)
                generar_monstruos_oleada(monstruos, map_width, map_height, oleada_actual, total_monstruos)
                mostrar_pantalla_victoria_flag = False
                # Curar al jugador completamente para la siguiente oleada
                player.hp = player.max_hp
            else:
                save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                running = False
                continue
        
        # Actualizar cámara
        camera_x = player.x - SCREEN_WIDTH // 2
        camera_y = player.y - SCREEN_HEIGHT // 2
        camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT))
        
        keys = pygame.key.get_pressed()
        
        if game_state == "explore":
            # Movimiento del jugador
            dx, dy = 0, 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy = 1
                
            player.move(dx, dy, walls)
            
            # Verificar combate
            if battle_cooldown <= 0:
                for monster in monstruos[:]:
                    distance = math.sqrt((player.x - monster.x)**2 + (player.y - monster.y)**2)
                    if distance < 80:
                        game_state = "battle"
                        current_monster = monster
                        battle_cooldown = 120
                        break
                        
        elif game_state == "battle":
            # Combate
            if keys[pygame.K_e] and player.attack_cooldown <= 0:
                damage = player.attack()
                if current_monster.take_damage(damage):
                    # Monstruo derrotado
                    experiencia = 20 + (current_monster.oleada * 5)
                    nivel_subido = player.ganar_experiencia(experiencia)
                    
                    player.score += 100 * current_monster.oleada
                    player.wins += 1
                    player.gold += int(random.randint(10, 30) * player.gold_mult * current_monster.oleada)
                    
                    monstruos.remove(current_monster)
                    
                    # Verificar si se completó la oleada
                    if sistema_oleadas.monstruo_derrotado():
                        mensaje_oleada = f"¡Oleada {oleada_actual} completada!"
                        mensaje_timer = 180
                        # Activar pantalla de victoria después de un breve delay
                        pygame.time.set_timer(pygame.USEREVENT, 2000, True)
                    
                    game_state = "explore"
                    current_monster = None
            
            if keys[pygame.K_h]:
                player.hp = min(player.max_hp, player.hp + 10)
                
            # Ataque del monstruo
            if current_monster and current_monster.attack_cooldown <= 0:
                if player.take_damage(current_monster.attack()):
                    if player.hp <= 0:
                        save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
                        running = False
            
            if keys[pygame.K_ESCAPE]:
                game_state = "explore"
                current_monster = None
                battle_cooldown = 60
        
        # Manejar evento de victoria
        for evento in pygame.event.get():
            if evento.type == pygame.USEREVENT:
                mostrar_pantalla_victoria_flag = True
        
        # Actualizar sistema de oleadas (solo si no estamos en pantalla de victoria)
        if not mostrar_pantalla_victoria_flag:
            siguiente_oleada = sistema_oleadas.update()
            if siguiente_oleada:
                oleada_actual = siguiente_oleada
                total_monstruos = sistema_oleadas.iniciar_oleada(oleada_actual)
                generar_monstruos_oleada(monstruos, map_width, map_height, oleada_actual, total_monstruos)
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
            
        # DIBUJADO (solo si no estamos en pantalla de victoria)
        if not mostrar_pantalla_victoria_flag:
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
            # Panel superior
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
            
            # Barra de vida del jugador
            vida_text = f"HP: {player.hp}/{player.max_hp}"
            screen.blit(font.render(vida_text, True, WHITE), (10, 40))
            bar_width = 200
            pygame.draw.rect(screen, RED, (80, 45, bar_width, 20))
            pygame.draw.rect(screen, GREEN, (80, 45, bar_width * (player.hp / player.max_hp), 20))
            pygame.draw.rect(screen, WHITE, (80, 45, bar_width, 20), 2)
            
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
                
                batalla_texts = [
                    f"Combatiendo: {current_monster.type} (Oleada {current_monster.oleada})",
                    f"HP Enemigo: {current_monster.hp}/{current_monster.max_hp}",
                    "E: Atacar | H: Curar (+10 HP) | ESC: Huir"
                ]
                
                for i, text in enumerate(batalla_texts):
                    screen.blit(small_font.render(text, True, WHITE), 
                               (20, SCREEN_HEIGHT - 70 + i * 20))
            
            pygame.display.flip()
        
        clock.tick(FPS)
        
    # Guardar al salir
    if not mostrar_pantalla_victoria_flag:
        save_player(player.nombre, player.score, player.wins, pros_sel, contras_sel)
    pygame.quit()