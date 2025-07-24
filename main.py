import pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carros 2D")

# Colores
VERDE = (0, 200, 0)

# Cargar imagen del auto
auto = pygame.image.load("imgs/auto.png")
auto = pygame.transform.scale(auto, (60, 40))  # Ajusta el tamaño si es necesario
x = 100
y = 100
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
    pantalla.fill(VERDE)
    pantalla.blit(auto, (x, y))
    pygame.display.update()

pygame.quit()
