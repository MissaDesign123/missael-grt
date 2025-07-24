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
x = 500
y = 120
velocidad = 5

# Bucle principal
ejecutando = True
while ejecutando:
    pygame.time.delay(30)  # Control de velocidad

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Teclas presionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidad
    if teclas[pygame.K_RIGHT]:
        x += velocidad
    if teclas[pygame.K_UP]:
        y -= velocidad
    if teclas[pygame.K_DOWN]:
        y += velocidad

    # Dibujar fondo y auto
    pantalla.blit(fondo, (0, 0))         # Dibujar imagen de fondo
    pantalla.blit(auto, (x, y))          # Dibujar el auto encima
    pygame.display.update()

pygame.quit()
