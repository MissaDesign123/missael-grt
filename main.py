import pygame
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carros 2D Terrorífico")



# Cargar imágenes
fondo = pygame.image.load("imgs/fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

auto = pygame.image.load("imgs/auto.jpg")
auto = pygame.transform.scale(auto, (60, 40))

# Posición inicial
x, y = 500, 120
velocidad = 5

# Vidas y contador de golpes
vidas = 20
golpes = 0
fuente = pygame.font.SysFont("Arial", 24)

# Cuadrados rojos
cuadro_tamano = 30
cuadro_velocidad = 5
cuadro_posiciones = [[random.randint(0, ANCHO - cuadro_tamano), random.randint(-300, -30)] for _ in range(5)]

# Cuadrados azules (invisibles al principio)
cuadros_azules = []
mostrar_azules = False
ganaste = False

# Semáforo
def dibujar_semaforo(superficie, x, y):
    cuerpo = pygame.Rect(x, y, 40, 120)
    pygame.draw.rect(superficie, (50, 50, 50), cuerpo)
    pygame.draw.circle(superficie, (255, 0, 0), (x + 20, y + 20), 15)
    pygame.draw.circle(superficie, (255, 255, 0), (x + 20, y + 60), 15)
    pygame.draw.circle(superficie, (0, 255, 0), (x + 20, y + 100), 15)

# Bucle principal
ejecutando = True
empezar_caida = False
auto_visible = True

while ejecutando:
    pygame.time.delay(30)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    if any([teclas[pygame.K_LEFT], teclas[pygame.K_RIGHT], teclas[pygame.K_UP], teclas[pygame.K_DOWN]]):
        empezar_caida = True

    if not ganaste and vidas > 0:
        if teclas[pygame.K_LEFT]: x -= velocidad
        if teclas[pygame.K_RIGHT]: x += velocidad
        if teclas[pygame.K_UP]: y -= velocidad
        if teclas[pygame.K_DOWN]: y += velocidad

    auto_rect = pygame.Rect(x, y, 60, 40)

    pantalla.blit(fondo, (0, 0))

    if auto_visible:
        pantalla.blit(auto, (x, y))

    if empezar_caida and vidas > 0 and not ganaste:
        for cuadro in cuadro_posiciones:
            cuadro[1] += cuadro_velocidad
            rect_cuadro = pygame.Rect(cuadro[0], cuadro[1], cuadro_tamano, cuadro_tamano)

            if auto_rect.colliderect(rect_cuadro):
                vidas -= 1
                golpes += 1
                cuadro[0] = random.randint(0, ANCHO - cuadro_tamano)
                cuadro[1] = random.randint(-300, -30)

            if cuadro[1] > ALTO:
                cuadro[0] = random.randint(0, ANCHO - cuadro_tamano)
                cuadro[1] = random.randint(-300, -30)

            pygame.draw.rect(pantalla, (255, 0, 0), rect_cuadro)

    # Mostrar azules si hubo 30 golpes
    if golpes >= 30 and not mostrar_azules:
        for _ in range(30):
            pos_x = random.randint(0, ANCHO - cuadro_tamano)
            pos_y = random.randint(0, ALTO - cuadro_tamano)
            cuadros_azules.append((pos_x, pos_y))
        mostrar_azules = True
        ganaste = True

    if mostrar_azules:
        for pos in cuadros_azules:
            pygame.draw.rect(pantalla, (0, 0, 255), (*pos, cuadro_tamano, cuadro_tamano))

    # Mostrar semáforo
    dibujar_semaforo(pantalla, ANCHO - 50, 10)

    # Mostrar vidas
    texto_vidas = fuente.render(f"{vidas}/20 vidas", True, (255, 255, 255))
    pantalla.blit(texto_vidas, (10, 10))

    # Mostrar mensaje de victoria
    if ganaste:
        texto = fuente.render("¡Ganaste el juego!", True, (0, 255, 0))
        pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2))

    # Mostrar mensaje de Game Over
    if vidas <= 0:
        texto = fuente.render("GAME OVER", True, (255, 0, 0))
        pantalla.blit(texto, (ANCHO // 2 - 80, ALTO // 2))

    pygame.display.update()

pygame.quit()







