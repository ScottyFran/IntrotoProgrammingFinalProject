####### SOURCES ##########
# SCOTTY FRANCIS 
# content from kids can code: http://kidscancode.org/blog/
# W3 Schools
# main_side.py
# https://www.freepik.com/
# https://freemusicarchive.org/search/?quicksearch=Super+Mario
# Microsoft Paint 
# https://www.youtube.com/watch?v=dGwmmBBMlKs&t=33s
# https://www.youtube.com/watch?v=iIb_xOs2a_E&t=112s
# https://www.youtube.com/watch?v=dGwmmBBMlKs&t=41s
# Charlie 
# https://www.youtube.com/watch?v=2BikxsbkuIU&t=277s

########## GAME RULES ############
# jump off platforms and collect cubes  
# collect 20 cubes to win 


##### GOALS GOALS GOALS #####
# Finished!!

#Import Settings File 
from settings import *


##Set Up Asset Folders for images 
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')


# Draws the text shown on screen (Points)
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte():
    return random.randint(0,255)




# Creates player sprite  which defines (color) and (size)
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        # Creates mario by pulling file from an outside source and adding it to player sprite
        self.image = pg.image.load(os.path.join(img_folder, 'supermario.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
# makes controls for the player 
    def controls(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_a]:
            self.acc.x = -5
     
        if keys[pg.K_d]:
            self.acc.x = 5

#Allows player to be able to jump off plats
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.vel.y = -20
    def draw(self):
        pass
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
#Updates my player
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        self.inbounds()
        self.rect.midbottom = self.pos

# platforms/ creates appearence of platorms 
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
# creates the general mob class 
class Mob(Sprite):
   def __init__(self, x, y, w, h, color, typeof):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.typeof = typeof
        self.speedx = 5*random.choice([-1,1])
        self.speedy = 5*random.choice([-1,1])
        self.inbounds = True
# Makes Mobs Bounce Off Walls 
   def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_plats, False)
            if hits:
                
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                

                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            

# keeps player for going off the screen by checking if it touching the sides of screen
   def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.speedx *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speedy *= -1
# Creates the "tetris like movement" of the "boss" MOB
   def update(self):
        if self.typeof == "boss":
            self.rect.x += self.speedx
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speedx *= -1
                self.rect.y += 50
        else:
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speedx *= -1
#Checks for boundaries so blocks can collide with the wals of the screen 
            self.boundscheck()
            self.collide_with_walls('x')
            self.collide_with_walls('y')
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        

# init pygame and create a window (creates game window)
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Scotty Francis Game")
clock = pg.time.Clock()

# Background
background = pg.image.load(os.path.join(img_folder, 'Background.jpg')).convert()
background_rect = background.get_rect()



# create groups (Platforms, sprite groups, and mobs)
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes/ shows where plats are located
player = Player()
plat = Platform(0, 580, 1000, 90)
plat2 = Platform(200, 400, 100, 35)
plat3 = Platform(700, 400, 100, 35)
plat4 = Platform(450, 250, 100, 35)

# Spawns in amount of "REGULAR" mobs + defines size and random color
for i in range(40):
    m = Mob(randint(-1000,WIDTH), randint(0,HEIGHT), 25, 25, (colorbyte(),colorbyte(),colorbyte()), "regular")
    all_sprites.add(m)
    mobs.add(m)
    print(m)
# creates big red cubes "BOSS" + defines size and color 
for i in range(5):
    m= Mob(randint(0,WIDTH), randint(0,HEIGHT/3), 50, 50, (255,0,0), "boss")
    all_sprites.add(m)
    mobs.add(m)
    print(m)



# add player to all sprites group
all_sprites.add(player)
all_plats.add(plat, plat2, plat3, plat4)

# add platform to all sprites group
all_sprites.add(plat)
all_sprites.add(plat2)
all_sprites.add(plat3)
all_sprites.add(plat4)



#Background Sound 
music = pg.mixer.music.load('SM.mp3')
pg.mixer.music.play(-1)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)
    # detects collision with mobs and objects/gives points 
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        player.pos.y = hits[0].rect.top
        player.vel.y = 0
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        SCORE += 1

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
        
    ############ Update ##############
    # update all sprites
    all_sprites.update()



    ############ Draw ############
    # draw the background screen
    screen.fill(BLACK)
    screen.blit(background, (0,0))



    # draw all sprites
    all_sprites.draw(screen)
    # Draws points on screen
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)

    
    
    # If points hit 20, you win  
    if SCORE >= 20:
        draw_text ("you win !!!!!", 100, RED, WIDTH/2, HEIGHT/4 )
    
    # buffer - after drawing everything, flip display   
    pg.display.flip()
pg.quit()