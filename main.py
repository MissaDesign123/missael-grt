import pygame
import random
import time
import math

pygame.init()

# Configuración
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Tesoros")

# Colores
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
DORADO = (255, 215, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
CIAN = (0, 255, 255)
MORADO = (128, 0, 128)
VERDE = (0, 255, 0)

# Jugador
x, y = 400, 300
velocidad = 5
jugador_rect = pygame.Rect(x, y, 12, 12)

# Enemigos
enemigo = None
enemigo_lasers = []
velocidad_enemigo = 2

meteoritos = []
velocidad_meteoritos = 2

# Tesoros
tesoro = None
mostrar_tesoro = False
tiempo_ultimo_tesoro = 0
esperar_un_segundo = False
jugador_se_movio = False

# Láseres jugador
lazers = []
mega_lasers = []
usar_poder_r = False
energia = 100

# Fondo
fondo = pygame.image.load("imgs/fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Juego
vidas = 100
puntos = 0
puntos_objetivo = 5
nivel = 1
nivel_terminado = False
tiempo_inicio = None

fuente = pygame.font.SysFont(None, 36)

reloj = pygame.time.Clock()
ejecutando = True

def mover_enemigo_hacia_jugador(enemigo_rect, jugador_rect, velocidad):
    # Calcula vector hacia jugador
    dx = jugador_rect.centerx - enemigo_rect.centerx
    dy = jugador_rect.centery - enemigo_rect.centery
    distancia = math.hypot(dx, dy)
    if distancia == 0:
        return enemigo_rect  # No se mueve si está en la misma posición
    dx_norm = dx / distancia
    dy_norm = dy / distancia
    enemigo_rect.x += int(dx_norm * velocidad)
    enemigo_rect.y += int(dy_norm * velocidad)
    return enemigo_rect

while ejecutando:
    reloj.tick(60)
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    dx = dy = 0
    if teclas[pygame.K_LEFT]:
        dx = -velocidad
    if teclas[pygame.K_RIGHT]:
        dx = velocidad
    if teclas[pygame.K_UP]:
        dy = -velocidad
    if teclas[pygame.K_DOWN]:
        dy = velocidad
    if teclas[pygame.K_f] and energia >= 10:
        laser = pygame.Rect(jugador_rect.centerx - 2, jugador_rect.y - 10, 4, 10)
        lazers.append(laser)
        energia -= 10
    if teclas[pygame.K_r] and usar_poder_r and energia >= 20:
        if enemigo:
            mega_laser = pygame.Rect(jugador_rect.centerx - 5, jugador_rect.y - 60, 10, 60)
            mega_lasers.append(mega_laser)
            usar_poder_r = False
            energia -= 20

    if dx != 0 or dy != 0:
        jugador_rect.x += dx
        jugador_rect.y += dy
        jugador_se_movio = True

    # Limitar jugador a pantalla
    jugador_rect.x = max(0, min(ANCHO - jugador_rect.width, jugador_rect.x))
    jugador_rect.y = max(0, min(ALTO - jugador_rect.height, jugador_rect.y))

    if jugador_se_movio and not mostrar_tesoro:
        if not esperar_un_segundo:
            tiempo_ultimo_tesoro = time.time()
            esperar_un_segundo = True
        elif time.time() - tiempo_ultimo_tesoro >= 1:
            tesoro = pygame.Rect(random.randint(0, ANCHO - 20), random.randint(0, ALTO - 20), 20, 20)
            mostrar_tesoro = True
            esperar_un_segundo = False

    if mostrar_tesoro and tesoro:
        pygame.draw.rect(pantalla, DORADO, tesoro)
        if jugador_rect.colliderect(tesoro):
            puntos += 1
            mostrar_tesoro = False
            jugador_se_movio = False
            tesoro = None
            energia = min(100, energia + 15)
            if puntos == 2:
                usar_poder_r = True

    pygame.draw.rect(pantalla, ROJO, jugador_rect)

    # Aparecer enemigo único si el jugador se movió y no existe
    if jugador_se_movio and enemigo is None:
        enemigo = pygame.Rect(random.randint(0, ANCHO - 40), 0, 40, 40)

    # Mover enemigo persiguiendo jugador
    if enemigo:
        enemigo = mover_enemigo_hacia_jugador(enemigo, jugador_rect, velocidad_enemigo)
        pygame.draw.rect(pantalla, MORADO, enemigo)

        # Enemigo dispara láseres aleatoriamente
        if random.randint(1, 100) == 1:
            laser_e = pygame.Rect(enemigo.centerx - 2, enemigo.y + 40, 4, 10)
            enemigo_lasers.append(laser_e)

        # Mover y dibujar láseres enemigo
        for laser_e in enemigo_lasers[:]:
            laser_e.y += 7
            pygame.draw.rect(pantalla, MORADO, laser_e)
            if laser_e.y > ALTO:
                enemigo_lasers.remove(laser_e)
            elif laser_e.colliderect(jugador_rect):
                vidas -= 5
                enemigo_lasers.remove(laser_e)

        if enemigo.colliderect(jugador_rect):
            vidas -= 10
            enemigo = None
            enemigo_lasers.clear()

    # Crear y mover meteoritos (cuadritos rojos)
    if tiempo_inicio:
        if random.randint(1, 20) == 1:
            meteorito = pygame.Rect(random.randint(0, ANCHO - 20), 0, 20, 20)
            meteoritos.append(meteorito)

        for meteorito in meteoritos[:]:
            meteorito.y += velocidad_meteoritos
            pygame.draw.rect(pantalla, ROJO, meteorito)
            if meteorito.colliderect(jugador_rect):
                vidas -= 1
                meteoritos.remove(meteorito)
            elif meteorito.y > ALTO:
                meteoritos.remove(meteorito)

    for laser in lazers[:]:
        laser.y -= 10
        pygame.draw.rect(pantalla, AZUL, laser)
        if laser.y < 0:
            lazers.remove(laser)
        elif enemigo and laser.colliderect(enemigo):
            enemigo = None
            lazers.remove(laser)
            enemigo_lasers.clear()

    for mlaser in mega_lasers[:]:
        mlaser.y -= 15
        pygame.draw.rect(pantalla, CIAN, mlaser)
        if mlaser.y < 0:
            mega_lasers.remove(mlaser)
        elif enemigo and mlaser.colliderect(enemigo):
            enemigo = None
            mega_lasers.remove(mlaser)
            enemigo_lasers.clear()

    # Iniciar tiempo cuando el jugador se mueve
    if jugador_se_movio and tiempo_inicio is None:
        tiempo_inicio = time.time()

    # HUD
    texto_vidas = fuente.render(f"Vidas: {vidas}/100", True, BLANCO)
    texto_puntos = fuente.render(f"Puntos: {puntos}/{puntos_objetivo}", True, BLANCO)
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, BLANCO)
    texto_energia = fuente.render(f"Energía: {energia}/100", True, VERDE)
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntos, (10, 40))
    pantalla.blit(texto_nivel, (10, 70))
    pantalla.blit(texto_energia, (10, 100))

    if usar_poder_r:
        texto_r = fuente.render("¡Poder desbloqueado! Presiona R", True, DORADO)
        pantalla.blit(texto_r, (10, 130))

    if puntos >= puntos_objetivo and not nivel_terminado:
        texto_ganar = fuente.render("¡HAS GANADO!", True, VERDE)
        pantalla.blit(texto_ganar, (ANCHO // 2 - 100, ALTO // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        nivel += 1
        puntos = 0
        puntos_objetivo += 5
        velocidad_enemigo += 1
        velocidad_meteoritos += 1
        enemigo = None
        enemigo_lasers.clear()
        meteoritos.clear()
        mostrar_tesoro = False
        jugador_se_movio = False
        tiempo_inicio = None
        energia = 100
        continue

    if vidas <= 0:
        texto_gameover = fuente.render("GAME OVER", True, ROJO)
        pantalla.blit(texto_gameover, (ANCHO // 2 - 100, ALTO // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        ejecutando = False

    pygame.display.update()

pygame.quit()
