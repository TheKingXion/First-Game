import pygame, sys, random
from button import Button

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAS CARRERAS DE MANFINFLA")

# IMG Y BACKGROUND
BG = pygame.image.load("assets/img/Background.png")
BGgame = pygame.image.load("assets/img/Backgroundgm.png")
icono = pygame.image.load("assets/img/ico.png")
pygame.display.set_icon(icono)

# Cargar y ajustar el tamaño de las imágenes de fondo de los ganadores
def load_scaled_image(path, width, height):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (width, height))

winner_backgrounds = [
    load_scaled_image("assets/img/BGW1.jpg", WIDTH, HEIGHT),  # Fondo para Buses
    load_scaled_image("assets/img/BGW2.jpg", WIDTH, HEIGHT), 
    load_scaled_image("assets/img/BGW3.jpg", WIDTH, HEIGHT), 
    load_scaled_image("assets/img/BGW4.jpg", WIDTH, HEIGHT)   
]

# Música/sonidos
def play_winner_music(index):
    winner_music = [
        'assets/sound/W1.ogg',
        'assets/sound/W2.ogg',
        'assets/sound/W3.ogg',
        'assets/sound/W4.ogg'
    ]
    pygame.mixer.music.load(winner_music[index])
    pygame.mixer.music.play(-1)

def play_menu_music():
    pygame.mixer.music.load('assets/sound/xd.ogg')
    pygame.mixer.music.play(-1)

def play_game_music():
    pygame.mixer.music.load('assets/sound/gamesound.ogg')
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Configuración de Buses
bus_images = ["assets/img/horse1.png", "assets/img/horse2.png", "assets/img/horse3.png", "assets/img/horse4.png"]
bus_sizes = [(280, 150), (260, 98), (300, 95), (262, 100)]
buses = []
for image, size in zip(bus_images, bus_sizes):
    bus = pygame.image.load(image)
    bus = pygame.transform.scale(bus, size)
    buses.append(bus)

# Posiciones iniciales de los Buses
bus_positions = [(-220, 40), (-200, 245), (-233, 390), (-200, 530)]
bus_rects = [bus.get_rect(topleft=pos) for bus, pos in zip(buses, bus_positions)]

# Línea de meta
FINISH_LINE = WIDTH - 100

# Velocidades
speeds = [random.randint(2, 6) for _ in range(len(buses))] 

# Estado del juego
running = True
menu = True
betting_screen = False
game_over = False
winner = None

# Variables de apuestas
bets = [0] * len(buses)  # Apuestas para cada bus
total_bets = 0

# Fuente
font = pygame.font.SysFont("assets/font/Casino.ttf", 55)

def get_font(size):
    return pygame.font.Font("assets/font/Casino.ttf", size)

def show_menu():
    screen.blit(BG, (0, 0))
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("MENU PRINCIPAL", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, 100))

    PLAY_BUTTON = Button(image=pygame.image.load("assets/img/Play Rect.png"), pos=(WIDTH // 2, 250),
                        text_input="JUGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/img/Options Rect.png"), pos=(WIDTH // 2, 400),
                            text_input="APUESTAS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/img/Quit Rect.png"), pos=(WIDTH // 2, 550),
                         text_input="SALIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    screen.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        button.changeColor(MENU_MOUSE_POS)
        button.update(screen)

    pygame.display.update()

    return PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON

def reset_game():
    global betting_screen, game_over, winner, bus_rects, speeds, bets, total_bets
    betting_screen = False
    game_over = False
    winner = None
    bus_rects = [bus.get_rect(topleft=pos) for bus, pos in zip(buses, bus_positions)]
    speeds = [random.randint(2, 6) for _ in range(len(buses))]
    bets = [0] * len(buses)  # Reiniciar las apuestas
    total_bets = 0

def betting():
    global betting_screen, total_bets
    input_boxes = [pygame.Rect(640 + 320, 30 + i * 170 + 50, 140, 50) for i in range(len(buses))]
    active_boxes = [False] * len(buses)
    user_texts = [""] * len(buses)
    
    while betting_screen:
        screen.fill(WHITE)
        bet_prompt = font.render("Introduce tu apuesta para cada Bus", True, BLACK)
        screen.blit(bet_prompt, (640 - bet_prompt.get_width() // 2, 20))
        button_back = font.render("Preciona ESC para volver atras", True, BLACK)
        screen.blit(button_back, (640 - button_back.get_width() // 1, 655))
        
        for i, bus in enumerate(buses):
            screen.blit(bus, (100, 10 + i * 180))
            bet_text = font.render(f"Apostar al Bus {i + 1}", True, BLACK)
            screen.blit(bet_text, (540, 35 + i * 170 + 50))
        
        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, BLACK, box, 2)
            text_surface = font.render(user_texts[i], True, BLACK)
            screen.blit(text_surface, (box.x + 5, box.y + 5))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_boxes[i] = True
                    else:
                        active_boxes[i] = False
            if event.type == pygame.KEYDOWN:
                for i in range(len(buses)):
                    if active_boxes[i]:
                        if event.key == pygame.K_RETURN and user_texts[i].isdigit():
                            bet_amount = int(user_texts[i])
                            bets[i] += bet_amount
                            total_bets += bet_amount
                            user_texts[i] = ''
                        elif event.key == pygame.K_BACKSPACE:
                            user_texts[i] = user_texts[i][:-1]
                        else:
                            user_texts[i] += event.unicode

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            betting_screen = False
            global menu
            menu = True

def game_loop():
    global game_over, winner, bus_rects, speeds

    # Reproducir música para el juego
    play_game_music()

    while not game_over:
        screen.fill(WHITE)
        screen.blit(BGgame, (0, 0))

        for i, rect in enumerate(bus_rects):
            if rect.x + rect.width >= FINISH_LINE:
                game_over = True
                winner = i
                break
            rect.x += speeds[i]

        for bus, rect in zip(buses, bus_rects):
            screen.blit(bus, rect)

        pygame.draw.line(screen, BLACK, (FINISH_LINE, 0), (FINISH_LINE, HEIGHT), 5)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # Detener la música cuando el juego termina
    stop_music()

def show_game_over_screen():
    global menu, game_over, winner, bets, total_bets
    # Cargar y mostrar el fondo de pantalla del ganador
    if winner is not None:
        screen.blit(winner_backgrounds[winner], (0, 0))
        play_winner_music(winner)
        winning_amount = total_bets if bets[winner] > 0 else 0
        result_text = font.render(f"¡Bus {winner + 1} ha ganado! Has ganado ${winning_amount:.2f}!", True, BLACK)
    else:
        result_text = font.render("¡La carrera ha terminado sin un ganador!", True, BLACK)

    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - result_text.get_height() // 2))

    button_text = font.render("Volver al Menú", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 100, button_text.get_width(), button_text.get_height())
    pygame.draw.rect(screen, GREEN, button_rect)
    screen.blit(button_text, (button_rect.x, button_rect.y))
    
    pygame.display.flip()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    if button_rect.collidepoint(event.pos):
                        menu = True
                        reset_game()  # Reiniciar el estado del juego al volver al menú
                        stop_music()  # Detener música antes de reiniciar
                        play_menu_music()  # Reproducir música del menú

def main():
    global running, menu, betting_screen

    # Reproducir música del menú al iniciar
    play_menu_music()

    while running:
        if menu:
            PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON = show_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        menu = False
                        game_loop()
                        show_game_over_screen()
                    elif OPTIONS_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        betting_screen = True
                        betting()
                    elif QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        running = False
        else:
            if betting_screen:
                betting()
            elif game_over:
                show_game_over_screen()
            else:
                game_loop()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
