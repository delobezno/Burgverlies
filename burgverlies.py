import pgzrun
import random

# 1. KONSTANTEN
RASTER_BREITE = 16
RASTER_HOEHE = 12
RASTER_GROESSE = 50
WACHE_INTERVALL = 0.5
HINTERGRUND_SEED = 123456

WIDTH = RASTER_BREITE * RASTER_GROESSE
HEIGHT = RASTER_HOEHE * RASTER_GROESSE

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

# 2. GLOBALE VARIABLEN INITIALISIEREN
game_over = False
gewonnen = False
spieler = None
schluessel_sammeln = []
wachen = []

# 3. HILFSFUNKTIONEN
def fenster_koord(x, y):
    return x * RASTER_GROESSE, y * RASTER_GROESSE

def raster_koord(actor):
    return round(actor.x / RASTER_GROESSE), round(actor.y / RASTER_GROESSE)

def setup_game():
    global game_over, gewonnen, spieler, schluessel_sammeln, wachen
    game_over = False
    gewonnen = False
    spieler = Actor("player", anchor=("left", "top"))
    schluessel_sammeln = []
    wachen = []
    for y in range(RASTER_HOEHE):
        for x in range(RASTER_BREITE):
            kachel = MAP[y][x]
            if kachel == "S":
                spieler.pos = fenster_koord(x, y)
            elif kachel == "K":
                schluessel = Actor("key", anchor=("left", "top"), pos=fenster_koord(x, y))
                schluessel_sammeln.append(schluessel)
            elif kachel == "G":
                wache = Actor("guard", anchor=("left", "top"), pos=fenster_koord(x, y))
                wachen.append(wache)

# 4. ZEICHEN-FUNKTIONEN
def zeichnen_hintergrund():
    random.seed(HINTERGRUND_SEED)
    for y in range(RASTER_HOEHE):
        for x in range(RASTER_BREITE):
            # Schachbrett-Muster für Boden
            if x % 2 == y % 2:
                screen.blit("floor1", fenster_koord(x, y))
            else:
                screen.blit("floor2", fenster_koord(x, y))
            
            # Zufällige Risse im Boden
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
                screen.blit("wall", fenster_koord(x, y))
            elif kachel == "T":
                # Tür wird nur gezeichnet, wenn noch Schlüssel da sind
                if len(schluessel_sammeln) > 0:
                    screen.blit("door", fenster_koord(x, y))

def draw():
    screen.clear()
    zeichnen_hintergrund()
    zeichnen_szenerie()
    spieler.draw()
    for s in schluessel_sammeln: s.draw()
    for w in wachen: w.draw()
    
    if game_over:
        screen_middle = (WIDTH / 2, HEIGHT / 2)
        farbe = "green" if gewonnen else "red"
        text = "GEWONNEN!" if gewonnen else "VERLOREN!"
        screen.draw.text("GAME OVER", midbottom=screen_middle, fontsize=60, color="cyan")
        screen.draw.text(text, midtop=screen_middle, fontsize=50, color=farbe)
        screen.draw.text("Leertaste für Neustart", midtop=(WIDTH/2, HEIGHT/2 + 70), fontsize=30)

# 5. LOGIK & BEWEGUNG
def move_spieler(dx, dy):
    global game_over, gewonnen
    if game_over: return
    
    x, y = raster_koord(spieler)
    x += dx
    y += dy
    
    # Kollision mit Wand/Grenzen
    if x < 0 or x >= RASTER_BREITE or y < 0 or y >= RASTER_HOEHE: return
    kachel = MAP[y][x]
    if kachel == "W": return
    
    # Ziel erreichen
    if kachel == "T":
        if len(schluessel_sammeln) == 0:
            game_over = True
            gewonnen = True
        return

    # Schlüssel einsammeln
    for s in schluessel_sammeln[:]:
        sx, sy = raster_koord(s)
        if x == sx and y == sy:
            schluessel_sammeln.remove(s)
    
    animate(spieler, pos=fenster_koord(x, y), duration=0.1)

def on_key_down(key):
    if key == keys.LEFT: move_spieler(-1, 0)
    elif key == keys.RIGHT: move_spieler(1, 0)
    elif key == keys.UP: move_spieler(0, -1)
    elif key == keys.DOWN: move_spieler(0, 1)
    elif key == keys.SPACE and game_over: setup_game()

def move_wachen():
    global game_over
    if game_over: return
    
    spieler_x, spieler_y = raster_koord(spieler)
    for wache in wachen:
        w_x, w_y = raster_koord(wache)
        
        # Einfache Verfolgungs-KI
        if spieler_x > w_x and MAP[w_y][w_x + 1] != "W": w_x += 1
        elif spieler_x < w_x and MAP[w_y][w_x - 1] != "W": w_x -= 1
        elif spieler_y > w_y and MAP[w_y + 1][w_x] != "W": w_y += 1
        elif spieler_y < w_y and MAP[w_y - 1][w_x] != "W": w_y -= 1
        
        animate(wache, pos=fenster_koord(w_x, w_y), duration=0.3)
        
        if w_x == spieler_x and w_y == spieler_y:
            game_over = True

# 6. START
setup_game()
clock.schedule_interval(move_wachen, WACHE_INTERVALL)
pgzrun.go()
