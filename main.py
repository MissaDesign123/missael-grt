import pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carros 2D")

# Cargar imagen de fondo
fondo = pygame.image.load("imgs/fondo.webp")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Redimensionar al tamaño de la pantalla

# Cargar imagen del auto
auto = pygame.image.load("imgs/auto.png")
auto = pygame.transform.scale(auto, (60, 40))  # Ajusta el tamaño si es necesario

# Posición inicial del auto (esquina superior izquierda con margen)
x = 500
y = 120

velocidad = 5

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(30)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_UP]:
        y -= velocidad
    if teclas[pygame.K_DOWN]:
        y += velocidad

    pantalla.blit(fondo, (0, 0))
    pantalla.blit(auto, (x, y))
    pygame.display.update()

pygame.quit()
