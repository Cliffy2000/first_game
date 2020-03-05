import os
import pygame
import random
pygame.init()


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480


win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('First game')
clock = pygame.time.Clock()
bg = pygame.image.load(os.path.join('res','bg.jpg'))
score = 0
pause = False
pauseTimer = 0

bulletSound = pygame.mixer.Sound(os.path.join('res','bullet.wav'))
hitSound = pygame.mixer.Sound(os.path.join('res','hit.wav'))
jumpSound = pygame.mixer.Sound(os.path.join('res','jump.wav'))
enemykillSound = pygame.mixer.Sound(os.path.join('res','enemy_die.wav'))
playerkillSound = pygame.mixer.Sound(os.path.join('res','player_die.wav'))
music = pygame.mixer.music.load(os.path.join('res','music.mp3'))
pygame.mixer.music.play(-1)


class player(object):
    walkRight = [pygame.image.load(os.path.join('res', f'R{i}.png')) for i in range(1, 10)]
    walkLeft = [pygame.image.load(os.path.join('res', f'L{i}.png')) for i in range(1, 10)]
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = True
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    
    def draw(self, win):
        if self.walkCount > 26:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left:
                win.blit(self.walkLeft[self.walkCount//3], (int(self.x), int(self.y)))
                self.walkCount += 1
            elif self.right:
                win.blit(self.walkRight[self.walkCount//3], (int(self.x), int(self.y)))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (int(self.x), int(self.y)))
            else:
                win.blit(self.walkLeft[0], (int(self.x), int(self.y)))
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 25
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 60)
        text = font1.render('You got killed', 1, (255,0,0))
        playerkillSound.play()
        win.blit(text, (int(250 - (text.get_width()/2)), 200))
        pygame.display.update()
        
        i = 0
        while i < 200:
            pygame.time.delay(20)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 12 * facing
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load(os.path.join('res', f'R{i}E.png')) for i in range(1, 12)]
    walkLeft = [pygame.image.load(os.path.join('res', f'L{i}E.png')) for i in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 23, self.y + 2, 25, 57)
        self.health = 9
        self.visible = True
        self.isJump = False
        self.jumpCount = 9
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount > 32:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (int(self.x), int(self.y)))
            else:
                win.blit(self.walkLeft[self.walkCount//3], (int(self.x), int(self.y)))
            self.walkCount += 1

            pygame.draw.rect(win, (128,0,0), (self.hitbox[0], self.hitbox[1]-20, 45, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1]-20, 5 * self.health, 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        
        self.hitbox = (self.x + 23, self.y + 2, 25, 57)    
    
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            enemykillSound.play()


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (370, 10))
    man.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)
man = player(300, 410, 64, 64)
goblins = [enemy(100, 410, 64, 64, 450)]
bullets = []
shoot = 0
run = True
while run:
    death = False
    clock.tick(30)
    keys = pygame.key.get_pressed()

    # Check game status
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pauseTimer = int((pauseTimer + 1) % 10)

    if keys[pygame.K_p] and pauseTimer == 0:
        if pause == True:
            pause = False
        else:
            pause = True
        pauseTimer = 1
    
    if pause:
        font2 = pygame.font.SysFont('comicsans', 48)
        text2 = font2.render('Game Paused', 1, (255,0,0))
        win.blit(text2, (int(250 - (text2.get_width()/2)), 150))
        pygame.display.update()
        continue

    # Check if player is alive
    for goblin in goblins:
        if goblin.visible == True:
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                    if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                        man.hit()
                        death = True
                        score -= 10
                        break
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    hitSound.play()
                    bullets.pop(bullets.index(bullet))
                    score += 1

            if bullet.x < SCREEN_WIDTH and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))
    
    if death:
        count = len(goblins)
        goblins = []
        for i in range(count):
            x = random.randint(125, 300)
            d = random.randint(64, 430-x)
            new = enemy(x, 410, 64, 64, x+d)
            goblins.append(new)

    # Player movement and shooting
    if shoot > 0:
        shoot += 1
    if shoot > 8:
        shoot = 0

    if keys[pygame.K_SPACE] and shoot == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing))
        shoot = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < SCREEN_WIDTH - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.walkCount = 0
        man.standing = True

    if not(man.isJump):
        if keys[pygame.K_UP]:
            jumpSound.play()
            man.isJump = True
            man.left = False
            man.Right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    
    check = True
    for goblin in goblins:
        if goblin.visible:
            check = False

    for goblin in goblins:
        if not(goblin.visible):
            goblins.pop(goblins.index(goblin))

    if check:
        goblins = []
        for i in range(random.randint(1,3)):
            x = man.x
            while abs(x - man.x) < 50:
                x = random.randint(0, 300)
            d = random.randint(64, 430-x)
            new = enemy(x, 410, 64, 64, x+d)
            goblins.append(new)
            a = random.randint(0, 1)
            if a == 1:
                new.x = new.end

        
    redrawGameWindow()


pygame.quit()
