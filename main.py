import pygame
import random
import time

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

# Jugador
x, y = 400, 300
velocidad = 5
jugador_rect = pygame.Rect(x, y, 12, 12)

# Enemigos y poderes
cuadrados_rojos = []
velocidad_cuadrados = 1

# Tesoros
tesoro = None
mostrar_tesoro = False
tiempo_ultimo_tesoro = 0
esperar_un_segundo = False
jugador_se_movio = False

# Láser
lazers = []

# Fondo
fondo = pygame.image.load("imgs/fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Juego
vidas = 100
puntos = 0
puntos_objetivo = 5
nivel = 1
tiempo_nivel = 2
nivel_terminado = False
tiempo_inicio = None

fuente = pygame.font.SysFont(None, 36)

reloj = pygame.time.Clock()
ejecutando = True

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
    if teclas[pygame.K_f]:
        # Disparar láser
        laser = pygame.Rect(jugador_rect.centerx - 2, jugador_rect.y - 10, 4, 10)
        lazers.append(laser)

    if dx != 0 or dy != 0:
        jugador_rect.x += dx
        jugador_rect.y += dy
        jugador_se_movio = True

    # Mostrar tesoro si se ha movido y ha pasado 1 segundo
    if jugador_se_movio and not mostrar_tesoro:
        if not esperar_un_segundo:
            tiempo_ultimo_tesoro = time.time()
            esperar_un_segundo = True
        elif time.time() - tiempo_ultimo_tesoro >= 1:
            tesoro = pygame.Rect(random.randint(0, ANCHO - 20), random.randint(0, ALTO - 20), 20, 20)
            mostrar_tesoro = True
            esperar_un_segundo = False

    # Dibujar tesoro
    if mostrar_tesoro and tesoro:
        pygame.draw.rect(pantalla, DORADO, tesoro)
        if jugador_rect.colliderect(tesoro):
            puntos += 1
            mostrar_tesoro = False
            jugador_se_movio = False
            tesoro = None

    # Dibujar jugador
    pygame.draw.rect(pantalla, ROJO, jugador_rect)

    # Láser
    for laser in lazers[:]:
        laser.y -= 10
        pygame.draw.rect(pantalla, AZUL, laser)
        if laser.y < 0:
            lazers.remove(laser)
        else:
            for enemigo in cuadrados_rojos[:]:
                if laser.colliderect(enemigo):
                    cuadrados_rojos.remove(enemigo)
                    if laser in lazers:
                        lazers.remove(laser)
                    break

    # Iniciar caída de enemigos al moverse por primera vez
    if jugador_se_movio and tiempo_inicio is None:
        tiempo_inicio = time.time()

    # Enemigos caen
    if tiempo_inicio:
        if random.randint(1, 20) == 1:
            cuadrados_rojos.append(pygame.Rect(random.randint(0, ANCHO - 20), 0, 20, 20))

        for enemigo in cuadrados_rojos[:]:
            enemigo.y += velocidad_cuadrados
            if enemigo.colliderect(jugador_rect):
                vidas -= 1
                cuadrados_rojos.remove(enemigo)
            elif enemigo.y > ALTO:
                cuadrados_rojos.remove(enemigo)
            else:
                pygame.draw.rect(pantalla, ROJO, enemigo)

    # Mostrar HUD
    texto_vidas = fuente.render(f"Vidas: {vidas}/100", True, BLANCO)
    texto_puntos = fuente.render(f"Puntos: {puntos}/{puntos_objetivo}", True, BLANCO)
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntos, (10, 40))
    pantalla.blit(texto_nivel, (10, 70))

    # Verificar si se ganó el nivel
    if puntos >= puntos_objetivo and not nivel_terminado:
        texto_ganar = fuente.render("¡HAS GANADO!", True, (0, 255, 0))
        pantalla.blit(texto_ganar, (ANCHO // 2 - 100, ALTO // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        nivel += 1
        puntos = 0
        puntos_objetivo += 5
        velocidad_cuadrados += 1
        cuadrados_rojos.clear()
        mostrar_tesoro = False
        jugador_se_movio = False
        tiempo_inicio = None
        nivel_terminado = False
        continue

    if vidas <= 0:
        texto_gameover = fuente.render("GAME OVER", True, ROJO)
        pantalla.blit(texto_gameover, (ANCHO // 2 - 100, ALTO // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        ejecutando = False

    pygame.display.update()

pygame.quit()














