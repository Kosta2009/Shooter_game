from pygame import *
from random import randint, random

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

window.blit(background, (0,0))

mixer.init()
mixer.music.load('space.ogg') 
fire = mixer.Sound('fire.ogg')

mixer.music.play()

lost = 0
score = 0

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 100)

text = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
text2 = font1.render("Сбито: " + str(score), 1, (255, 255, 255))

bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7.5, self.rect.y, 15, 20, 5)
        global bullets
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global text
        if self.rect.y > 500:
            self.speed = randint(1,3)
            self.rect.x = randint(80, 500 - 80)
            self.rect.y = 0
            lost = lost + 1
            text = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
player = Player('rocket.png', 310, 400, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    speed = random()*3
    if speed < 1:
        speed = 1
    print(speed)
    monsters.add(Enemy('ufo.png', randint(5,715), 0, 80, 50, speed))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.speed = randint(1,3)
            self.rect.x = randint(80, 500 - 80)
            self.rect.y = 0

asteroids = sprite.Group()
for i in range(5):
    speed = random()*3
    if speed < 1:
        speed = 1
    print(speed)
    asteroids.add(Asteroid('asteroid.png', randint(5,715), 0, 80, 50, speed))

wait = 0
shots = 0

finish = False

clock = time.Clock()
game = True
while game:
    if finish != True:
        sprites = sprite.groupcollide(bullets, monsters, True, True)
        for monster in sprites:
            score += 1
            text2 = font1.render("Сбито: " + str(score), 1, (255, 255, 255))
            speed = random()*3
            if speed < 1:
                speed = 1
            monsters.add(Enemy('ufo.png', randint(5,715), 0, 80, 50, speed))
        sprites = sprite.groupcollide(bullets, asteroids, True, False)
        window.blit(background, (0,0))
        window.blit(text, (10,10))
        window.blit(text2, (10,50))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        keys = key.get_pressed()
        if score >= 10:
            win_text = font2.render("ПОБЕДА", 1, (0, 255, 0))
            window.blit(win_text, (190,230))
            finish = True
        if lost >= 3 or sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            lose_text = font2.render("ПОРАЖЕНИЕ", 1, (255, 0, 0))
            window.blit(lose_text, (120,230))
            finish = True
        if shots >= 5:
            wait = 180
            reload_text = font1.render("Перезарядка...", 1, (255, 0, 0))
            shots = 0
        if wait <= 0:
            reload_text = font1.render("", 1, (255, 0, 0))
            if keys[K_SPACE]:
                player.fire()
                shots += 1
                wait = 20
        else:
            wait -= 1
        window.blit(reload_text, (230, 400))
        display.update()
        clock.tick(60)
    for e in event.get():
        if e.type == QUIT:
            game = False

input('Ентер')