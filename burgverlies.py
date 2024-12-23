import pgzrun
import random

RASTER_BREITE = 16
RASTER_HOEHE = 12
RASTER_GROESSE = 50
WACHE_INTERVALL = 0.5

WIDTH = RASTER_BREITE * RASTER_GROESSE
HEIGHT = RASTER_HOEHE * RASTER_GROESSE

pgzrun.go()

MAP = ["WWWWWWWWWWWWWWWW",
       "W              W",
       "W              W",
       "W  W  KG       W",
       "W  WWWWWWWWWW  W",
       "W              W",
       "W      S       W",
       "W  WWWWWWWWWW  W",
       "W      GK   W  W",
       "W              W",
       "W              T",
       "WWWWWWWWWWWWWWWW"]

def fenster_koord(x, y):
    return x * RASTER_GROESSE, y * RASTER_GROESSE

def raster_koord(actor):
    return round(actor.x / RASTER_GROESSE), round(actor.y / RASTER_GROESSE)

def setup_game():
    global game_over, spieler, schluessel_sammeln, wachen
    game_over = False
    gewonnen = False
    spieler = Actor("player", anchor=("left", "top"))
    schluessel_sammeln = []
    wachen = []
    for y in range(RASTER_HOEHE):
        for x in range(RASTER_BREITE):
            kachel = MAP[y][x]
            if kachel == "S":
                spieler.pos = fenster_koord(x,y)
            elif kachel == "K":
                schluessel = Actor("key", anchor=("left", "top"), pos=fenster_koord(x, y))
                schluessel_sammeln.append(schluessel)
            elif kachel == "G":
                wache = Actor("guard", anchor=("left", "top"), pos=fenster_kord(x, y))
                wachen.append(wache)
def zeichnen_hintergrund():
    random.seed(HINTERGRUND_SEED)
    for y in range(RASTER_HOEHE):
        for x in range(RASTER_BREITE):
            if x % 2 == y % 2:
                screen.blit("floor1", fenster_koord(x, y))
            else:
                screen.blit("floor2", fenster_koord(x,y))

            n = random.randint(0, 99)
            if n < 5:
                screen.blit("crack1", fenster_koord(x, y))
            elif n < 10:
                screen.blit("crack2", fenster_koord(x, y))

def zeichnen_szenerie():
    for y in range(RASTER_HOEHE):
        for x in range(RASTER_BREITE):
            kachel = MAP[y][x]
            if kachel == "W":
                screen.blit("wall", fenster_koord(x,y))
            elif kachel == "T" and len(schluessel_sammeln) > 0:
                screen.blit("door", fenster_koord(x,y))

def zeichnen_actors():
    spieler.draw()
    for schluessel in schluessel_sammeln:
        schluessel.draw()
    for wache in wachen:
        wache.draw()

def zeichnen_game_over():
    screen_middle = (WIDTH / 2, HEIGHT / 2)
    screen.draw.text("GAME OVER", midbottom=screen_middle, frontsize=RASTER_GROESSE, color="cyan", owidth=1)

    if gewonnen:
        screen.draw.text("Gewonnen!", midtop=screen_middle, \
                         fontsize=RASTER_GROESSE, color="green", owidth=1)
    else:
        screen.draw.text("Verloren!", midtop=screen_middle, \
                         fontsize=RASTER_GROESSE, color="red", owidth=1)

    screen.draw.text("Leertaste für Neustart", midtop=(WIDTH / 2, \
                                                       HEIGHT / 2 + RASTER_GROESSE), \
                     fontsize=RASTER_GROESSE / 2, color="cyan", owidth=1)
def draw():
    zeichnen_hintergrund()
    zeichnen_szenerie()
    zeichnen_actors()
    if game_over:
        zeichnen_game_over()

def on_key_up(key):
    if key == keys.SPACE and game_over:
        setup_game()

def on_key_down(key):
    if key == keys.LEFT:
        move_spieler(-1, 0)
    elif key == keys.UP:
        move_spieler(0, -1)
    elif key == keys.RIGHT:
        move_spieler(1, 0)
    elif key == keys.DOWN:
        move_spieler(0, 1)

def move_spieler(dx, dy):
    SPIELER_MOVE_INTERVALL = 0.1
    HINTERGRUND_SEED = 123456
    global game_over, gewonnen
    if game_over:
        return
    (x, y) = raster_koord(spieler)
    x += dx
    y += dy
    kachel = MAP[y][x]
    if kachel == "W":
        return
    elif kachel == "T":
        if len(schluessel_sammeln) > 0:
            return
        else:
            game_over = True
            gewonnen = True
    for schluessel in schluessel_sammeln:
        (schluessel_x, schluessel_y) = raster_koord(schluessel)
        if x == schluessel_x and y == schluessel_y:
            schluessel_sammeln.remove(schluessel)
            break
    animate(spieler, pos=fenster_koord(x,y), \
            duration=SPIELER_MOVE_INTERVALL, \
            on_finished=repeat_spieler_move)
    spieler.pos = fenster_koord(x, y)

def repeat_spieler_move():
    if keyboard.left:
        move_spieler(-1, 0)
    elif keyboard.up:
        move_spieler(0, -1)
    elif keyboard.right:
        move_spieler(1, 0)
    elif keyboard.down:
        move_spieler(0, 1)

def move_wache(wache):
    global game_over
    if game_over:
        return
    (spieler_x, spieler_y) = raster_koord(spieler)
    (wache_x, wache_y) = raster_koord(wache)
    if spieler_x > wache_x and MAP[wache_y][wache_x + 1] != "W":
        wache_x += 1
    elif spieler_x < wache_x and MAP[wache_y][wache_x - 1] != "W":
        wache_x -= 1
    elif spieler_y > wache_y and MAP[wache_y + 1][wache_x] != "W":
        wache_y += 1
    elif spieler_y < wache_x and MAP[wache_y -1][wache_x] != "W":
        wache_y -= 1
    animate(wache, pos=fenster_koord(wache_x, wache_y), \
            duration=WACHE_MOVE_INTERVALL)
    if wache_x == spieler_x and wache_y == spieler_y:
        game_over = True

def move_wachen():
    for wache in wachen:
        move_wache(wache)

setup_game()
clock.schedule_interval(move_wachen(), WACHE_INTERVALL)
