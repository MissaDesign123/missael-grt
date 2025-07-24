import pygame
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carros 2D")

# Cargar imagen de fondo en formato .webp
fondo = pygame.image.load("imgs/fondo.webp")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Cargar imagen del auto
auto = pygame.image.load("imgs/auto.png")
auto = pygame.transform.scale(auto, (60, 40))

x, y = 500, 120
velocidad = 5

# Definir el "túnel" como rectángulo para detectar colisión (no se dibuja)
tunel_rect = pygame.Rect(300, 200, 100, 80)

auto_visible = True

# Función para dibujar el semáforo en pantalla
def dibujar_semaforo(superficie, pos_x, pos_y):
    # Cuerpo del semáforo
    cuerpo_rect = pygame.Rect(pos_x, pos_y, 40, 120)
    pygame.draw.rect(superficie, (50, 50, 50), cuerpo_rect)  # gris oscuro

    # Luces (círculos)
    radio = 15
    # Rojo (arriba)
    pygame.draw.circle(superficie, (255, 0, 0), (pos_x + 20, pos_y + 20), radio)
    # Amarillo (medio)
    pygame.draw.circle(superficie, (255, 255, 0), (pos_x + 20, pos_y + 60), radio)
    # Verde (abajo)
    pygame.draw.circle(superficie, (0, 255, 0), (pos_x + 20, pos_y + 100), radio)

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

    # Dibujar fondo y auto
    pantalla.blit(fondo, (0, 0))         # Dibujar imagen de fondo
    pantalla.blit(auto, (x, y))          # Dibujar el auto encima
    pygame.display.update()

pygame.quit()
