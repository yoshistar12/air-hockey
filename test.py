from ball import *
import sys, pygame, time, pygame.gfxdraw

clock = pygame.time.Clock()

def color_picker(n):
    'velger fargen til en ball som skal legges ut ved å syklere mellom noen farger (color_order)'
    m = 0
    if n >= len(color_order):
        m = n % len(color_order)
    else:
        m = n
    return pygame.Color(*color_order[m])

state = 0 # setter "tilstanden til 0, der man kan velge hvor å plassere ballene"

def draw_circle(coords, color): 
    '''
    Funksjon for å tegne sirkelen.
    '''
    ncoords = [] #

    if (isinstance(coords, Vector)): # Sjekker om vi har en vektor (?)
        ncoords.append(int(coords.x)) # Hvis vi har det, så legger vi til x koordinaten i ncoords lista.
        ncoords.append(int(coords.y)) # Hvis vi har det, så legger vi til y koordinaten i ncoords lista.
    else:
        ncoords.append(int(coords[0])) # Hvis ikke vi har en vektor, så legger vi til 1. elementet i coords lista.
        ncoords.append(int(coords[1])) # Hvis ikke vi har en vektor, så legger vi til 2. elementet i coords lista.
    pygame.gfxdraw.aacircle(screen, *ncoords, int(d_rad), color) # Tegner sirkelen
    pygame.gfxdraw.filled_circle(screen, *ncoords, int(d_rad), color) # Tegner sirkelen

pygame.init()
size = width, height = 800, 400 # Definerer en variabel med størrelsene på vinduet.
border = 20 # Setter av kanter til 20 px
screen = pygame.display.set_mode(size) # Setter størrelse på pygame vinduet.
dt = 0.003 # Tidsforskjell mellom hver beregning.
speed_bound = 2 # Hvor lav må farten være før friksjonen virker
speed_limit = 5000 # Hvor hardt du kan treffe ballen dersom du treffer fra kanten
g = 9.81 # Gravitasjon

#Farger
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(178,58,58)
GRAY = pygame.Color(122, 122, 122)
GREEN = pygame.Color(33,101,67)
BLUE = pygame.Color(58, 118, 178)
YELLOW = pygame.Color(255, 255, 0)
C2 = pygame.Color(63, 42, 20)
color_order = ((255, 10, 2), (2, 255, 90), (7, 20, 255), (230, 230, 15), (153, 0, 153), (255, 128, 0), (255, 51, 153), (142, 62, 25))

d_mass = 1 # Masse
d_rad = 15.83 # Radius til kule
mu = 50 # My, Friksjon
damp_wall = 0.2 # Vegg fartsdemper
damp_ball = 0.04 # Hvis 2 baller kolliderer, mister Ek.

balls = [] # "Boksen" med ballene.

again = False # Again, altså legg ball ut "igjen". Du kan ikke legge ut flere baller, før du har lagt den ene.

while True:
    '''
    Default pygame plugin
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # tegner airhockey-bakgrunnen
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, height, width, -height))    
    pygame.draw.rect(screen, WHITE, (border, height-border, width - 2*border, -height + 2*border))
    pygame.gfxdraw.filled_circle(screen, *(400, 200), 52, RED)
    pygame.gfxdraw.aacircle(screen, *(400, 200), 52, RED)
    pygame.gfxdraw.filled_circle(screen, *(400, 200), 48, WHITE)
    pygame.gfxdraw.aacircle(screen, *(400, 200), 48, WHITE)
    pygame.draw.rect(screen, RED, (398, 19, 4, 362))

    if state == 2: # dette er tilstanden der alle ballene er i bevegelse; her kan du ikke gi fart til baller
        if all(ball.speed() == 0 for ball in balls):
            state = 1
            continue

        combos = [] # alle kombinasjoner av to baller som har blitt skjekket for kollisjon

        for ball1 in balls:
            for ball2 in balls:
                if ball1 != ball2 and (ball1.pos + (ball1.vel * dt) - (ball2.pos + (ball2.vel * dt))).mag() < ball1.rad + ball2.rad and (ball1.pos - ball2.pos).mag() > ((ball1.pos + (ball1.vel * dt)) - (ball2.pos + (ball2.vel * dt))).mag():
                    # dette er bare litt vektorregning
                    N = (ball2.pos - ball1.pos).normalize()
                    T = Vector(-1 * N.y, N.x)
                    V_a_N_before = N * ball1.vel
                    V_a_T_before = T * ball1.vel
                    V_b_N_before = N * ball2.vel
                    V_b_T_before = T * ball2.vel
                    V_a_N_after = V_b_N_before
                    V_b_N_after = V_a_N_before
                    ball1.vel = (1 - damp_ball) * ((V_a_N_after * N) + (V_a_T_before * T))
                    ball2.vel = (1 - damp_ball) * ((V_b_N_after * N) + (V_b_T_before * T))
                    combos.append({ball1, ball2})

        for ball in balls:
        # Dette sjekker friksjon.
            if ball.speed() > speed_bound:
                ball.vel -= ball.dir() * mu * g * dt
            else:
                ball.vel = Vector(0, 0)
            if ball.pos.x + ball.vel.x * dt < ball.rad + border or ball.pos.x + ball.vel.x * dt > width - ball.rad - border:
                ball.vel.x *= damp_wall - 1
            if ball.pos.y + ball.vel.y * dt < ball.rad + border or ball.pos.y + ball.vel.y * dt > height - ball.rad - border:
                ball.vel.y *= damp_wall - 1
            ball.is_checked = False

        
        for ball in balls:
            ball.pos += ball.vel * dt # basic integration ;)

        # her vises "ballene" på skjermen
        for n in range(len(balls)):
            draw_circle(balls[n].pos, color_picker(n))
        pygame.display.flip()


    if state == 0: # dette er når du starter spillet. I denne tilstanden kan du legge til baller med left-click
        if pygame.mouse.get_pressed()[2] and balls:
            state = 1
            continue

        # dette skjekker om ballen kan plasserer i en gyldig posisjon eller ikke
        mouse_pos = list(pygame.mouse.get_pos())
        if mouse_pos[0] < border+d_rad:
            mouse_pos[0] = border+d_rad
        elif mouse_pos[0] > width-border-d_rad:
            mouse_pos[0] = width-border-d_rad
        if mouse_pos[1] < border+d_rad:
            mouse_pos[1] = border+d_rad
        elif mouse_pos[1] > height-border-d_rad:
            mouse_pos[1] = height-border-d_rad
        mouse_pos[0] = int(mouse_pos[0])
        mouse_pos[1] = int(mouse_pos[1])

        nope = False # nope er true hvis du peker over en ball,da  kan du ikke plassere en ny ball der (obviously)

        # her skjekker vi om du kan sette en ball i den posisjonen du har valgt eller ikke
        for ball in balls:
            if (Vector(*mouse_pos) - ball.pos).mag() < d_rad + ball.rad:
                nope = True
        if nope: # hvis du ikke kan plassere ballen der du hoverer over
            for n in range(len(balls)):
                draw_circle(balls[n].pos, color_picker(n))
            draw_circle(mouse_pos, BLACK)
            pygame.display.flip()
            continue
        draw_circle(mouse_pos, GRAY)
        if again and pygame.mouse.get_pressed()[0]: # hvis du kan plassere en ball der, så blir det en ball til
            balls.append(Ball(Vector(mouse_pos[0], mouse_pos[1])))
            again = False
        for n in range(len(balls)):
            draw_circle(balls[n].pos, color_picker(n))
        pygame.display.flip()
        if not pygame.mouse.get_pressed()[0]:
            again = True

    if state == 1: # her kan du gi en ball fart ved å trykke på en ball med venstre-click. Ballen går motsatt vei av der du trakk, og jo større avstand fra sentrum, jo fortere går den
        if pygame.mouse.get_pressed()[0]:
            for ball in balls:
                mouse_pos = Vector(*pygame.mouse.get_pos())
                if (mouse_pos - ball.pos).mag() < ball.rad:
                    ball.vel = ((ball.pos - mouse_pos).mag() * speed_limit / ball.rad) * (ball.pos - mouse_pos).normalize()
                    state = 2
                    break
        if state == 2:
            continue
        for n in range(len(balls)):
            draw_circle(balls[n].pos, color_picker(n))
        pygame.display.flip()
        
    time.sleep(dt)
    #pygame.time.delay(int(dt * 1000))
    #clock.tick(1 / dt)

    



