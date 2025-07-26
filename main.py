import pygame
import random
import time
import math
import os
from pygame import mixer

# Inicialización de pygame y mixer para sonidos
pygame.init()
mixer.init()

# Configuración de pantalla
ANCHO, ALTO = 1364, 698  # Pantalla más grande
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)  # Permitir redimensionamiento
pygame.display.set_caption("Galactic Treasure Hunter")  # Título de la ventana
FPS = 60 #FPS

# Cargar el icono (asegúrate de que la ruta sea correcta)
try:
    icono = pygame.image.load("imgs/icono.png")  # o .ico
    pygame.display.set_icon(icono)  # Establecer el icono
except:
    print("No se pudo cargar el icono. Se usará el predeterminado.")
   
# Crear directorio de imágenes si no existe
if not os.path.exists('imgs'):
    os.makedirs('imgs')
    
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
DORADO = (255, 215, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
CIAN = (0, 255, 255)
MORADO = (128, 0, 128)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
ROSA = (255, 105, 180)

# Cargar imágenes (asumiendo que existen estos archivos en imgs/)
try:
    fondos = []  # Lista para almacenar los fondos de cada nivel
    for i in range(1, 6):  
        fondo_img = pygame.image.load(f"imgs/fondo_{i}.png")
        fondos.append(pygame.transform.scale(fondo_img, (ANCHO, ALTO)))
    
    # Si no hay suficientes fondos, usamos el primero para todos los niveles
    if len(fondos) < 5:
        for i in range(len(fondos), 5):
            fondos.append(fondos[0].copy())
    
    meteoro_img = pygame.image.load("imgs/obstaculo.png")
    meteoro_img = pygame.transform.scale(meteoro_img, (40, 40))
    nave_img = pygame.image.load("imgs/nave.png")
    nave_img = pygame.transform.scale(nave_img, (70, 70))
    enemigo_img = pygame.image.load("imgs/enemigo.png")
    enemigo_img = pygame.transform.scale(enemigo_img, (60, 60))
    enemigo_2_img = pygame.image.load("imgs/enemigo_2.png")  # Corregir si hay typo en el nombre del archivo
    enemigo_2_img = pygame.transform.scale(enemigo_2_img, (60, 60))
    enemigo_3_img = pygame.image.load("imgs/enemigo_3.png")  # Asegurarse que el archivo existe con este nombre
    enemigo_3_img = pygame.transform.scale(enemigo_3_img, (60, 60))
    jefe_img = pygame.image.load("imgs/jefe.png")
    jefe_img = pygame.transform.scale(jefe_img, (80, 80))
    tesoro_img = pygame.image.load("imgs/tesoro.png")
    tesoro_img = pygame.transform.scale(tesoro_img, (55, 55))
    powerup_img = pygame.image.load("imgs/powerup.png")
    powerup_img = pygame.transform.scale(powerup_img, (45, 45))
    vida_img = pygame.image.load("imgs/vida.png") 
    vida_img = pygame.transform.scale(vida_img, (65, 65)) 
except:
    # Si no hay imágenes, usaremos formas geométricas
    fondos = [None] * 5
    meteoro_img = None
    nave_img = None
    enemigo_img = None
    enemigo_2_img = None  # Añadir esta línea
    enemigo_3_img = None  # Añadir esta línea
    jefe_img = None
    tesoro_img = None
    powerup_img = None
    vida_img = None

# Cargar sonidos
try:
    sonido_laser = mixer.Sound("sounds/laser.mp3")
    sonido_explosion = mixer.Sound("sounds/explosion.mp3")
    sonido_tesoro = mixer.Sound("sounds/tesoro.mp3")
    sonido_powerup = mixer.Sound("sounds/powerup.mp3")
    sonido_dano = mixer.Sound("sounds/dano.mp3")
except:
    # Si no hay sonidos, los desactivamos
    sonido_laser = None
    sonido_explosion = None
    sonido_tesoro = None
    sonido_powerup = None
    sonido_dano = None

# Clases para organizar mejor el código
class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(ANCHO//2, ALTO//2, 40, 40)
        self.velocidad = 5
        self.puntos = 0
        self.vidas = 50         
        self.vidas_max = 50
        self.energia = 100     
        self.energia_max = 100
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.poderes = {
            "disparo_rapido": False,
            "mega_laser": False,
            "escudo": False
        }
        self.escudo_activo = False
        self.escudo_duracion = 0
        self.disparo_cooldown = 0
        self.sprite = nave_img
        self.ultima_direccion = (0, -1)  # Por defecto hacia arriba
        
    def mover(self, dx, dy):
        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad
        # Limitar a pantalla
        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(ALTO - self.rect.height, self.rect.y))
        
        if dx != 0 or dy != 0:
            self.ultima_direccion = (dx, dy)
            
    def dibujar(self, pantalla):
        if self.sprite:
            pantalla.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            color = CIAN if self.invulnerable else AZUL
            pygame.draw.rect(pantalla, color, self.rect)
            
        if self.escudo_activo:
            pygame.draw.circle(pantalla, CIAN, self.rect.center, 30, 2)
            
    def recibir_dano(self, cantidad):
        if not self.invulnerable and not self.escudo_activo:
            self.vidas -= cantidad
            self.invulnerable = True
            self.tiempo_invulnerable = time.time()
            if sonido_dano:
                sonido_dano.play()
            return True
        return False
        
    def actualizar(self):
        # Cooldown de disparo
        if self.disparo_cooldown > 0:
            self.disparo_cooldown -= 1
            
        # Invulnerabilidad después de daño
        if self.invulnerable and time.time() - self.tiempo_invulnerable > 1:
            self.invulnerable = False
            
        # Regeneración de energía
        if self.energia < self.energia_max:
            self.energia += 0.23
            
        # Escudo temporal
        if self.escudo_activo and time.time() - self.escudo_duracion > 5:
            self.escudo_activo = False
            
    def disparar_superlaser(self):
        if self.energia >= 30:  # Coste alto de energía
            self.energia -= 30
            lasers = []
            # Disparar un láser más grande y poderoso
            for i in range(-1, 9):  # cantidad de laseres en un pequeño abanico
                angulo = math.radians(i * 20)  # Menor dispersión que el disparo normal
                dx = math.cos(angulo) * self.ultima_direccion[0] - math.sin(angulo) * self.ultima_direccion[1]
                dy = math.sin(angulo) * self.ultima_direccion[0] + math.cos(angulo) * self.ultima_direccion[1]
                
                laser = {
                    "rect": pygame.Rect(self.rect.centerx-4, self.rect.centery-4, 8, 15),  # Más grande
                    "direccion": (dx, dy),
                    "velocidad": 12,  # Más rápido
                    "color": CIAN,  # Color diferente
                    "daño": 3  # Más daño
                }
                lasers.append(laser)
            
            if sonido_laser:
                sonido_laser.play()  # O usa un sonido diferente para el superláser
            return lasers
        return []
    
class Enemigo:
    def __init__(self, x, y, tipo="normal", nivel=1):
        self.tipo = tipo
        self.tiempo_aparicion = time.time()  # Nuevo: registrar tiempo de aparición
        self.efecto_aparicion = None  # Nuevo: efecto especial de aparición
            
        if tipo == "normal":
            self.rect = pygame.Rect(x, y, 50, 50)
            self.velocidad = 2 + nivel * 0.1  # Aumenta velocidad por nivel
            self.vida = 2
            self.color = MORADO
            self.sprite = enemigo_img
        elif tipo == "rapido":
            self.rect = pygame.Rect(x, y, 50, 50)
            self.velocidad = 3 + nivel * 0.15
            self.vida = 3
            self.color = ROSA
            self.sprite = enemigo_2_img
        elif tipo == "resistente":
            self.rect = pygame.Rect(x, y, 50, 50)
            self.velocidad = 1.5 + nivel * 0.1
            self.vida = 5 + nivel // 2  # Más vida en niveles altos
            self.color = NARANJA
            self.sprite = enemigo_3_img
        elif tipo == "jefe":
            self.rect = pygame.Rect(x, y, 90, 90)
            self.velocidad = 1
            self.vida = 10 + nivel * 5 #Vida del jefe aumenta en cada nivel
            self.color = ROJO
            self.sprite = jefe_img
            self.patron_movimiento = 0
            self.tiempo_ultimo_disparo = 0
            
    def mover_hacia(self, objetivo_rect):
        if self.tipo == "jefe":
            # Movimiento especial para el jefe
            self.patron_movimiento += 0.02
            self.rect.x = ANCHO//2 + math.sin(self.patron_movimiento) * 300
            self.rect.y = 100 + math.cos(self.patron_movimiento * 0.5) * 50
        else:
            # Movimiento normal hacia el jugador
            dx = objetivo_rect.centerx - self.rect.centerx
            dy = objetivo_rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)
            if distancia > 0:
                dx_norm = dx / distancia
                dy_norm = dy / distancia
                self.rect.x += int(dx_norm * self.velocidad)
                self.rect.y += int(dy_norm * self.velocidad)
                
    def disparar(self, objetivo_rect):
        if self.tipo == "jefe" and time.time() - self.tiempo_ultimo_disparo > 2:
            self.tiempo_ultimo_disparo = time.time()
            lasers = []
            # Disparo en patrón del jefe
            for angulo in range(0, 360, 45):
                rad = math.radians(angulo)
                laser = {
                    "rect": pygame.Rect(self.rect.centerx-3, self.rect.centery-3, 6, 6),
                    "direccion": (math.sin(rad), math.cos(rad)),
                    "velocidad": 5,
                    "color": ROJO
                }
                lasers.append(laser)
            return lasers
        elif random.randint(1, 100) == 1:
            laser = {
                "rect": pygame.Rect(self.rect.centerx-2, self.rect.bottom, 4, 10),
                "direccion": (0, 1),
                "velocidad": 5,
                "color": self.color
            }
            return [laser]
        return []
        
    def dibujar(self, pantalla):
            # Mostrar efecto de aparición si existe
            if self.efecto_aparicion and time.time() - self.tiempo_aparicion < 2:  # Mostrar por 2 segundos
                self.efecto_aparicion.dibujar(pantalla)
            
            if self.sprite:
                # Si es un jefe y está apareciendo, hacerlo parpadear
                if self.tipo == "jefe" and time.time() - self.tiempo_aparicion < 2:
                    if int((time.time() - self.tiempo_aparicion) * 5) % 2 == 0:  # Parpadeo rápido
                        pantalla.blit(self.sprite, (self.rect.x, self.rect.y))
                else:
                    pantalla.blit(self.sprite, (self.rect.x, self.rect.y))
            else:
                pygame.draw.rect(pantalla, self.color, self.rect)
                
            # Barra de vida mejorada para jefes
            if self.tipo == "jefe":
                # Fondo de la barra
                pygame.draw.rect(pantalla, (50, 50, 50), (self.rect.x - 10, self.rect.y - 20, self.rect.width + 20, 10))
                # Barra de vida principal
                vida_porcentaje = self.vida / (15 + self.nivel * 10)
                pygame.draw.rect(pantalla, ROJO, (self.rect.x - 10, self.rect.y - 20, (self.rect.width + 20) * vida_porcentaje, 8))
                # Borde resaltado
                pygame.draw.rect(pantalla, BLANCO, (self.rect.x - 10, self.rect.y - 20, self.rect.width + 20, 10), 2)
                
                # Texto con el nombre del jefe
                texto_jefe = fuente_pequena.render(f"JEFE NIVEL {self.nivel}", True, BLANCO)
                pantalla.blit(texto_jefe, (self.rect.centerx - texto_jefe.get_width()//2, self.rect.y - 40))

class ObjetoEspecial:
    def __init__(self, tipo, x=None, y=None):
        self.tipo = tipo  # "tesoro", "powerup", "vida"
        self.rect = pygame.Rect(x or random.randint(0, ANCHO-30), 
                               y or random.randint(0, ALTO-30), 
                               30, 30)
        self.tiempo_vida = 10  # Segundos antes de desaparecer
        self.tiempo_creacion = time.time()
        
        if tipo == "tesoro":
            self.color = DORADO
            self.sprite = tesoro_img
            self.valor = 1
        elif tipo == "powerup":
            self.color = VERDE
            self.sprite = powerup_img
            self.tipo_powerup = random.choice(["disparo_rapido", "mega_laser", "escudo"])
        elif tipo == "vida":
            self.color = ROJO
            self.sprite = vida_img  # Usar la imagen de vida (o None si no existe)
            self.valor = 20
            
    def dibujar(self, pantalla):
        if self.sprite:
            pantalla.blit(self.sprite, (self.rect.topleft))
        else:
            pygame.draw.rect(pantalla, self.color, self.rect)
        
        # Mostrar tiempo restante
        tiempo_restante = self.tiempo_vida - (time.time() - self.tiempo_creacion)
        if tiempo_restante < 3:  # Parpadea los últimos 3 segundos
            if int(tiempo_restante * 2) % 2 == 0:  # Parpadeo
                if self.sprite:
                    pantalla.blit(self.sprite, (self.rect.topleft))
                else:
                    pygame.draw.rect(pantalla, self.color, self.rect)
                    
    def esta_vivo(self):
        return time.time() - self.tiempo_creacion < self.tiempo_vida

class EfectoParticula:
    def __init__(self, x, y, color, cantidad=20, tamaño=3):
        self.particulas = []
        for _ in range(cantidad):
            velocidad = random.uniform(1, 5)
            angulo = random.uniform(0, math.pi*2)
            vida = random.uniform(0.5, 1.5)
            self.particulas.append({
                "x": x,
                "y": y,
                "dx": math.cos(angulo) * velocidad,
                "dy": math.sin(angulo) * velocidad,
                "vida": vida,
                "tamaño": tamaño,
                "color": color,
                "tiempo": 0
            })
            
    def actualizar(self):
        for p in self.particulas[:]:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["tiempo"] += (1/FPS)  
            if p["tiempo"] >= p["vida"]:
                self.particulas.remove(p)
                
    def dibujar(self, pantalla):
        for p in self.particulas:
            alpha = 255 * (1 - p["tiempo"]/p["vida"])
            color = list(p["color"])
            if len(color) == 3:
                color.append(alpha)
            superficie = pygame.Surface((p["tamaño"]*2, p["tamaño"]*2), pygame.SRCALPHA)
            pygame.draw.circle(superficie, color, (p["tamaño"], p["tamaño"]), p["tamaño"])
            pantalla.blit(superficie, (p["x"] - p["tamaño"], p["y"] - p["tamaño"]))

# Inicialización de objetos del juego
jugador = Jugador()
enemigos = []
objetos_especiales = []
lasers_jugador = []
lasers_enemigos = []
meteoritos = []
efectos_particulas = []
explosiones = []

# Variables de juego
nivel = 1
puntos_objetivo = 50 + (nivel * 50)  # Más puntos por nivel
tiempo_inicio_nivel = None
enemigos_restantes = 0
spawn_timer = 0
jefe_aparecido = False
jefe_derrotado = False
tiempo_ultimo_tesoro = 0
pausado = False
game_over = False
victoria = False

# Fuentes
fuente_pequena = pygame.font.SysFont("Arial", 18)
fuente_mediana = pygame.font.SysFont("Arial", 24)
fuente_grande = pygame.font.SysFont("Arial", 36)
fuente_titulo = pygame.font.SysFont("Arial", 72, bold=True)

# Música
try:
    mixer.music.load("imgs/musica_fondo.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)  # Repetir indefinidamente
except:
    pass

def spawn_enemigos(cantidad, nivel_actual):
    global enemigos_restantes
    
    # Disminuir la cantidad de enemigos normales
    cantidad = max(3, 5 + nivel_actual - 2)  # Menos enemigos que antes
    
     # Aumenta la probabilidad de enemigos resistentes en niveles altos
    if nivel_actual >= 3:
        tipos = ["normal"] * 30 + ["resistente"] * 15 + ["rapido"] * 5 + ["jefe"] * 25
    else:
        tipos = ["normal"] * 50 + ["resistente"] * 20  + ["rapido"] * 10
    
    if nivel_actual >= 2 and jugador.puntos >= puntos_objetivo * 0.7 and not any(e.tipo == "jefe" for e in enemigos):
        # Añadir jefes según el nivel (máximo 3)
        jefes_a_spawnear = min(nivel_actual - 1, 3)
        for _ in range(jefes_a_spawnear):
            x = random.choice([-50, ANCHO+50, random.randint(0, ANCHO)])
            y = random.choice([-50, ALTO+50, random.randint(0, ALTO)])
            # Asegurarse de que no aparezca demasiado cerca del jugador
            while math.hypot(x - jugador.rect.centerx, y - jugador.rect.centery) < 200:
                x = random.choice([-50, ANCHO+50, random.randint(0, ANCHO)])
                y = random.choice([-50, ALTO+50, random.randint(0, ALTO)])
            enemigos.append(Enemigo(x, y, "jefe", nivel_actual))
            enemigos_restantes += 1
        
        mostrar_mensaje(f"¡VIENEN {jefes_a_spawnear} JEFES!", ROJO, 48, 2)
        return  # Salir de la función después de spawnear jefes
    
    # Spawn normal de otros enemigos
    for _ in range(cantidad):
        tipo = random.choice(tipos)
        x = random.choice([-50, ANCHO+50, random.randint(0, ANCHO)])
        y = random.choice([-50, ALTO+50, random.randint(0, ALTO)])
        
        # Asegurarse de que no aparezca demasiado cerca del jugador
        while math.hypot(x - jugador.rect.centerx, y - jugador.rect.centery) < 200:
            x = random.choice([-50, ANCHO+50, random.randint(0, ANCHO)])
            y = random.choice([-50, ALTO+50, random.randint(0, ALTO)])
            
        enemigos.append(Enemigo(x, y, tipo, nivel_actual))
          
    # Actualizar enemigos_restantes SOLO al inicio del nivel
    if tiempo_inicio_nivel is None:
        enemigos_restantes = cantidad
        
def spawn_objeto_especial(tipo=None):
    if not tipo:
        tipos = ["tesoro"] * 70 + ["powerup"] * 20 + ["vida"] * 10
        tipo = random.choice(tipos)
        
    objetos_especiales.append(ObjetoEspecial(tipo))

def mostrar_hud():
    # Barra de vida
    vida_porcentaje = jugador.vidas / jugador.vidas_max
    pygame.draw.rect(pantalla, ROJO, (10, 10, 200, 20))
    pygame.draw.rect(pantalla, VERDE, (10, 10, 200 * vida_porcentaje, 20))
    texto_vida = fuente_pequena.render(f"Vida: {jugador.vidas}/{jugador.vidas_max}", True, BLANCO)
    pantalla.blit(texto_vida, (15, 10))
    
    # Barra de energía
    energia_porcentaje = jugador.energia / jugador.energia_max
    pygame.draw.rect(pantalla, MORADO, (10, 35, 200, 15))
    pygame.draw.rect(pantalla, AZUL, (10, 35, 200 * energia_porcentaje, 15))
    texto_energia = fuente_pequena.render(f"Energía: {int(jugador.energia)}/{jugador.energia_max}", True, BLANCO)
    pantalla.blit(texto_energia, (15, 35))
    
    # Puntos y nivel
    texto_puntos = fuente_mediana.render(f"Puntos: {jugador.puntos}", True, BLANCO)
    texto_nivel = fuente_mediana.render(f"Nivel: {nivel}", True, BLANCO)
    texto_objetivo = fuente_mediana.render(f"Objetivo: {puntos_objetivo}", True, BLANCO)
    pantalla.blit(texto_puntos, (ANCHO - 150, 10))
    pantalla.blit(texto_nivel, (ANCHO - 150, 40))
    pantalla.blit(texto_objetivo, (ANCHO - 150, 70))
    
    # Poderes activos
    y_poder = 70
    for poder, activo in jugador.poderes.items():
        if activo:
            texto = fuente_pequena.render(poder.replace("_", " ").title(), True, AMARILLO)
            pantalla.blit(texto, (15, y_poder))
            y_poder += 20
    
    if jugador.escudo_activo:
        texto = fuente_pequena.render("Escudo activo", True, CIAN)
        pantalla.blit(texto, (15, y_poder))

def mostrar_mensaje(texto, color=BLANCO, tamaño=36, duracion=2, y_offset=0):
    fuente_temp = pygame.font.SysFont("Arial", tamaño)
    superficie = fuente_temp.render(texto, True, color)
    rect = superficie.get_rect(center=(ANCHO//2, ALTO//2 + y_offset))
    pantalla.blit(superficie, rect)
    pygame.display.update()
    pygame.time.delay(int(duracion * 1000))

def pantalla_inicio():
    pantalla.fill(NEGRO)
    
    if fondos[nivel-1]:
        pantalla.blit(fondos[nivel-1], (0, 0))
    
    titulo = fuente_titulo.render("TREASURE HUNTER", True, DORADO)
    subtitulo = fuente_grande.render("Presiona cualquier tecla para comenzar", True, BLANCO)
    controles = fuente_mediana.render("Controles: Flechas para mover, F para disparar, R para mega , P para pausar", True, BLANCO)
    objetivo = fuente_mediana.render("Objetivo: Recolecta tesoros y derrota enemigos", True, BLANCO)
    
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//4))
    pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, ALTO//2))
    pantalla.blit(controles, (ANCHO//2 - controles.get_width()//2, ALTO//2 + 50))
    pantalla.blit(objetivo, (ANCHO//2 - objetivo.get_width()//2, ALTO//2 + 90))
    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False
    return True

def pantalla_pausa():
    pantalla.fill((0, 0, 0, 128))  # Semi-transparente
    texto = fuente_grande.render("PAUSA", True, BLANCO)
    continuar = fuente_mediana.render("Presiona P para continuar", True, BLANCO)
    
    pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 50))
    pantalla.blit(continuar, (ANCHO//2 - continuar.get_width()//2, ALTO//2 + 20))
    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                esperando = False
    return True

def pantalla_final(victoria=False):
    pantalla.fill(NEGRO)
    
    if victoria:
        titulo = fuente_titulo.render("¡VICTORIA!", True, DORADO)
        mensaje = fuente_grande.render(f"Completaste todos los niveles con {jugador.puntos} puntos", True, BLANCO)
    else:
        titulo = fuente_titulo.render("GAME OVER", True, ROJO)
        mensaje = fuente_grande.render(f"Alcanzaste el nivel {nivel} con {jugador.puntos} puntos", True, BLANCO)
        nivel_perdido = fuente_mediana.render(f"Perdiste en el nivel {nivel}", True, BLANCO)
    
    reiniciar = fuente_mediana.render("Presiona R para reiniciar desde el nivel 1", True, BLANCO)
    salir = fuente_mediana.render("Presiona ESC para salir", True, BLANCO)
    
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//3))
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2))
    if not victoria:
        pantalla.blit(nivel_perdido, (ANCHO//2 - nivel_perdido.get_width()//2, ALTO//2 + 40))
    pantalla.blit(reiniciar, (ANCHO//2 - reiniciar.get_width()//2, ALTO//2 + 100))
    pantalla.blit(salir, (ANCHO//2 - salir.get_width()//2, ALTO//2 + 140))
    
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True  # Reiniciar
                elif evento.key == pygame.K_ESCAPE:
                    return False  # Salir
    return False

def reiniciar_juego():
    global jugador, enemigos, objetos_especiales, lasers_jugador, lasers_enemigos
    global meteoritos, efectos_particulas, explosiones, nivel, puntos_objetivo
    global tiempo_inicio_nivel, enemigos_restantes, spawn_timer, jefe_aparecido, jefe_derrotado
    global tiempo_ultimo_tesoro, pausado, game_over, victoria
    
    jugador = Jugador()
    enemigos = []
    objetos_especiales = []
    lasers_jugador = []
    lasers_enemigos = []
    meteoritos = []
    efectos_particulas = []
    explosiones = []
    
    nivel = 1
    puntos_objetivo = 50 + (nivel * 50)
    tiempo_inicio_nivel = None
    enemigos_restantes = 0
    spawn_timer = 0
    jefe_aparecido = False
    jefe_derrotado = False
    tiempo_ultimo_tesoro = 0
    pausado = False
    game_over = False
    victoria = False

# Bucle principal del juego
if pantalla_inicio():
    ejecutando = True
    reloj = pygame.time.Clock()
    
    while ejecutando:
        reloj.tick(FPS) 
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                
                if evento.key == pygame.K_p and not game_over and not victoria:
                    if not pantalla_pausa():
                        ejecutando = False
                        
                elif evento.key == pygame.K_r:  # Tecla R para superláser
                    nuevos_lasers = jugador.disparar_superlaser()
                    lasers_jugador.extend(nuevos_lasers)
                    
                elif evento.key == pygame.K_f and jugador.energia >= 10:
                    # Disparar 3 láseres en un pequeño abanico
                    for i in range(-1, 3):  # Esto creará la cantidad de disparos 
                        angulo = math.radians(i * 30)  # Pequeña desviación para cada láser
                        dx = math.cos(angulo) * jugador.ultima_direccion[0] - math.sin(angulo) * jugador.ultima_direccion[1]
                        dy = math.sin(angulo) * jugador.ultima_direccion[0] + math.cos(angulo) * jugador.ultima_direccion[1]
                        
                        laser = {
                            "rect": pygame.Rect(jugador.rect.centerx-2, jugador.rect.centery-2, 4, 10),
                            "direccion": (dx, dy),
                            "velocidad": 10,
                            "color": AZUL,
                            "daño": 1
                        }
                        
                        lasers_jugador.append(laser)
                    
                    jugador.energia -= 2  # Coste de energía por el conjunto de disparos
                    jugador.disparo_cooldown = 0
                    if sonido_laser:
                        sonido_laser.play()
        if pausado or game_over or victoria:
            continue
        
        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        dx = dy = 0
        if teclas[pygame.K_LEFT]:
            dx = -1
        if teclas[pygame.K_RIGHT]:
            dx = 1
        if teclas[pygame.K_UP]:
            dy = -1
        if teclas[pygame.K_DOWN]:
            dy = 1
        
        jugador.mover(dx, dy)
        jugador.actualizar()
        
        # Iniciar nivel si no se ha hecho
        if tiempo_inicio_nivel is None:
            tiempo_inicio_nivel = time.time()
            spawn_enemigos(5 + nivel * 2, nivel)
        
        # Spawn de enemigos periódico
        spawn_timer += 1/FPS
        if spawn_timer >= 3:  
            spawn_timer = 0
            
        # Spawnear siempre un mínimo de enemigos, independientemente de enemigos_restantes
            spawn_cantidad = min(nivel, 6)  # Rango de enemigos según nivel
            spawn_enemigos(spawn_cantidad, nivel)
            
            if enemigos_restantes > 0:
                spawn_enemigos(min(1, nivel), nivel)
        
        # Spawn de tesoros y power-ups
        if time.time() - tiempo_ultimo_tesoro > 5:  # Cada 5 segundos
            tiempo_ultimo_tesoro = time.time()
            if random.random() < 0.7:  # 70% de probabilidad
                spawn_objeto_especial()
        
        # Actualizar enemigos
        for enemigo in enemigos[:]:
            enemigo.mover_hacia(jugador.rect)
            
            # Disparar
            nuevos_lasers = enemigo.disparar(jugador.rect)
            lasers_enemigos.extend(nuevos_lasers)
            
            # Colisión con láseres del jugador
            for laser in lasers_jugador[:]:
                if laser["rect"].colliderect(enemigo.rect):
                    enemigo.vida -= laser["daño"]
                    lasers_jugador.remove(laser)
                    efectos_particulas.append(EfectoParticula(
                        laser["rect"].centerx, laser["rect"].centery, 
                        laser["color"], 10, 2
                    ))
                    # Actualizar enemigos_restantes cuando se elimina un enemigo
                    if enemigo.vida <= 0:
                        enemigos.remove(enemigo)                        
                        if enemigo.tipo == "jefe":
                            jefe_derrotado = True
                            
                        enemigos_restantes -= 1
                            
                        jugador.puntos += 3 if enemigo.tipo == "jefe" else 1
                        
                        explosiones.append(EfectoParticula(
                            enemigo.rect.centerx, enemigo.rect.centery,
                            enemigo.color, 30, 4
                        ))
                        if sonido_explosion:
                            sonido_explosion.play()
                        if enemigo.tipo == "jefe":
                            jefe_derrotado = True
                            spawn_objeto_especial("powerup")
                            spawn_objeto_especial("powerup")
                            spawn_objeto_especial("vida")
                        break
        
        # Actualizar láseres del jugador
        for laser in lasers_jugador[:]:
            laser["rect"].x += int(laser["direccion"][0] * laser["velocidad"])
            laser["rect"].y += int(laser["direccion"][1] * laser["velocidad"])
            
            # Eliminar si sale de pantalla
            if (laser["rect"].x < -50 or laser["rect"].x > ANCHO+50 or 
                laser["rect"].y < -50 or laser["rect"].y > ALTO+50):
                lasers_jugador.remove(laser)
        
        # Actualizar láseres enemigos
        for laser in lasers_enemigos[:]:
            laser["rect"].x += int(laser["direccion"][0] * laser["velocidad"])
            laser["rect"].y += int(laser["direccion"][1] * laser["velocidad"])
            
            # Colisión con jugador
            if laser["rect"].colliderect(jugador.rect):
                if jugador.recibir_dano(5 if laser["color"] == ROJO else 2):
                    lasers_enemigos.remove(laser)
                    efectos_particulas.append(EfectoParticula(
                        laser["rect"].centerx, laser["rect"].centery, 
                        laser["color"], 10, 2
                    ))
            
            # Eliminar si sale de pantalla
            if (laser["rect"].x < -50 or laser["rect"].x > ANCHO+50 or 
                laser["rect"].y < -50 or laser["rect"].y > ALTO+50):
                lasers_enemigos.remove(laser)
        
        # Actualizar objetos especiales
        for obj in objetos_especiales[:]:
            # Colisión con jugador
            if obj.rect.colliderect(jugador.rect):
                if obj.tipo == "tesoro":
                    jugador.puntos += obj.valor
                    if sonido_tesoro:
                        sonido_tesoro.play()
                elif obj.tipo == "powerup":
                    jugador.poderes[obj.tipo_powerup] = True
                    if obj.tipo_powerup == "escudo":
                        jugador.escudo_activo = True
                        jugador.escudo_duracion = time.time()
                    if sonido_powerup:
                        sonido_powerup.play()
                elif obj.tipo == "vida":
                    jugador.vidas = min(jugador.vidas_max, jugador.vidas + obj.valor)
                    if sonido_powerup:
                        sonido_powerup.play()
                
                objetos_especiales.remove(obj)
                efectos_particulas.append(EfectoParticula(
                    obj.rect.centerx, obj.rect.centery, 
                    obj.color, 20, 3
                ))
            elif not obj.esta_vivo():
                objetos_especiales.remove(obj)
        
        # Actualizar efectos de partículas
        for efecto in efectos_particulas[:]:
            efecto.actualizar()
            if not efecto.particulas:
                efectos_particulas.remove(efecto)

        # Modificar la condición de aparición del jefe:
        if nivel >= 2 and not jefe_aparecido and jugador.puntos >= puntos_objetivo * 0.7:  # 70% del objetivo
            jefe_aparecido = True
            # Spawnear 1 jefe en nivel 2, 2 en nivel 3, etc.
            for _ in range(min(nivel-1, 3)):  # Máximo 3 jefes
                enemigos.append(Enemigo(random.randint(0, ANCHO), -100, "jefe", nivel))
                enemigos_restantes += 1
            mostrar_mensaje(f"¡VIENEN {min(nivel-1, 3)} JEFES!", ROJO, 48, 2)
       
        # Verificar fin de nivel
        if (jugador.puntos >= puntos_objetivo and not jefe_aparecido) or jefe_derrotado:
            if nivel < 5:
                nivel += 1
                puntos_objetivo += 50 #Se cambia que tanto aumenta los puntos objetivos en cada nivel
                # Limpiar todo
                enemigos.clear()
                lasers_enemigos.clear()
                lasers_jugador.clear()
                objetos_especiales.clear()
                efectos_particulas.clear()
                
                # Reiniciar variables
                tiempo_inicio_nivel = None
                enemigos_restantes = 5 + nivel * 2  # Cantidad inicial basada en nivel
                spawn_timer = 0
                jefe_aparecido = False
                jefe_derrotado = False
                tiempo_ultimo_tesoro = time.time()
                
                # Spawn inicial de enemigos
                spawn_enemigos(10 + nivel * 3, nivel)
                
                #Mejorar jugador entre niveles
                jugador.vidas = jugador.vidas_max
                jugador.energia = jugador.energia_max
                
                if nivel % 2 == 0:
                    jugador.velocidad += 1
                    jugador.energia_max += 20
                    jugador.vidas_max += 20  # Añadir más vida máxima cada 2 niveles
                    jugador.vidas = jugador.vidas_max
                                    
                mostrar_mensaje(f"Nivel {nivel - 1} completado!", VERDE, 48, 2)
                mostrar_mensaje(f"Siguiente nivel: {nivel}", AMARILLO, 36, 1, 50)
            else:
                victoria = True
        
        # Verificar game over
        if jugador.vidas <= 0:
            game_over = True
        
        # Dibujado
        if fondos[nivel-1]:  # Usar el fondo correspondiente al nivel (nivel-1 porque la lista empieza en 0)
            pantalla.blit(fondos[nivel-1], (0, 0))
        else:
            pantalla.fill(NEGRO)
                
        # Dibujar objetos especiales
        for obj in objetos_especiales:
            obj.dibujar(pantalla)
        
        # Dibujar láseres
        for laser in lasers_jugador:
            pygame.draw.rect(pantalla, laser["color"], laser["rect"])
        for laser in lasers_enemigos:
            pygame.draw.rect(pantalla, laser["color"], laser["rect"])
        
        # Dibujar enemigos
        for enemigo in enemigos:
            enemigo.dibujar(pantalla)
        
        # Dibujar efectos
        for efecto in efectos_particulas:
            efecto.dibujar(pantalla)
        
        # Dibujar jugador
        jugador.dibujar(pantalla)
        
        # Dibujar HUD
        mostrar_hud()
        
        # Mensajes de nivel
        if tiempo_inicio_nivel and time.time() - tiempo_inicio_nivel < 3:
            texto = fuente_grande.render(f"Nivel {nivel}", True, BLANCO)
            pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//4))
        
        pygame.display.flip()
        
        # Pantallas de estado
        if game_over:
            if pantalla_final(False):
                reiniciar_juego()
            else:
                ejecutando = False
        elif victoria:
            if pantalla_final(True):
                reiniciar_juego()
            else:
                ejecutando = False
                
pygame.quit()