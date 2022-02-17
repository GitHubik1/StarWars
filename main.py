import pygame as pg
import time as tm
import random as rnd

def main():
    class playerAmmo(pg.sprite.Sprite):
        def __init__(self, y, x, speed, surf, group):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.image.load(surf).convert_alpha()
            self.rect = self.image.get_rect(center=(1920 - x, y))
            self.speed = speed
            self.add(group)

        def update(self, *args):
            if self.rect.x > -65:
                self.rect.x -= self.speed
            else:
                self.kill()

    class enemy(pg.sprite.Sprite):
        def __init__(self, y, speed, surf, group, hp):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.image.load(surf).convert_alpha()
            self.rect = self.image.get_rect(center=(0, y))
            self.speed = speed
            self.hp = hp
            self.add(group)

        def update(self, *args):
            if self.rect.x < 1960:
                self.rect.x += self.speed
            else:
                self.kill()
            if self.hp < 1:
                self.kill()

    pg.init()
    pg.mixer.pre_init(44100, -16, 1, 512)
    resume = True
    FPS = 60
    W, H = 1920, 1080
    sc = pg.display.set_mode((W, H))
    speed = 3

    player = pg.image.load('images/big_ship.png')
    playerRect = player.get_rect(right=W-80, centery=H//2)
    font = pg.font.Font('fonts/font.TTF', 36)
    game_score = 0

    gametime = 0
    bombSound1 = pg.mixer.Sound('sounds/bomb.ogg')
    bombSound2 = pg.mixer.Sound('sounds/bomb2.ogg')
    bombSound3 = pg.mixer.Sound('sounds/bomb3.ogg')
    laserSound = pg.mixer.Sound('sounds/laser.ogg')
    W_BACKGROUND = 1920

    clock = pg.time.Clock()
    background1, background2 = pg.image.load('images/stars.jpg').convert(), pg.image.load('images/stars.jpg').convert()
    x_background1, x_background2 = 0, W_BACKGROUND
    ticks = 0
    playerAmmoGroup = pg.sprite.Group()
    enemyGroup = pg.sprite.Group()

    def createPlayerAmmo(group, y, x):
        return playerAmmo(playerRect.centery + y, x, 3, 'images/patron.png', group)

    def createEnemy(group):
        t = rnd.randint(0, H)
        return enemy(t, rnd.randint(1, 3), 'images/small_ship.png', group, 100)

    def collidepoints():
        nonlocal game_score
        for enemy in enemyGroup:
            for ammo in playerAmmoGroup:
                if enemy.rect.colliderect(ammo.rect):
                    n = rnd.randint(1, 100)
                    if n < 34:
                        bombSound1.play()
                    elif n < 67:
                        bombSound2.play()
                    else:
                        bombSound3.play()
                    enemy.hp -= 100
                    ammo.kill() 
                    game_score += 100

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        
        if ((pg.time.get_ticks() // 10) * 10) % 50:
            gametime += 1
            if gametime % 120 == 0:
                createEnemy(enemyGroup)
        
            if resume:
                keys = pg.key.get_pressed()
                if keys[pg.K_UP]:
                        playerRect.y -= speed
                        if playerRect.y < 0:
                            playerRect.y = 0
                elif keys[pg.K_DOWN]:
                    playerRect.y += speed
                    if playerRect.y > H-playerRect.height:
                        playerRect.y = H-playerRect.height
                elif keys[pg.K_SPACE]:
                    if (gametime - ticks) >= 10:
                        createPlayerAmmo(playerAmmoGroup, 20, 130)
                        createPlayerAmmo(playerAmmoGroup, -20, 130)
                        createPlayerAmmo(playerAmmoGroup, 30, 110)
                        createPlayerAmmo(playerAmmoGroup, -30, 110)
                        laserSound.play()
                        ticks = gametime

                collidepoints()
            
                if gametime % 10 == 0:
                    x_background1 -= 1
                    x_background2 -= 1
                sc.blit(background1, (x_background1, 0))
                sc.blit(background1, (x_background2, 0))
                if (x_background1 <= (0 - W_BACKGROUND)):
                        x_background1 = W_BACKGROUND
                if (x_background2 <= (0 - W_BACKGROUND)):
                    x_background2 = W_BACKGROUND

                playerAmmoGroup.draw(sc)
                enemyGroup.draw(sc)
                sc.blit(player, playerRect)
                sc_text = font.render(str(game_score), 1, (94, 138, 14))
                sc.blit(sc_text, (20, 10))

            pg.display.update()
            clock.tick(FPS)
            if resume:
                playerAmmoGroup.update()
                enemyGroup.update()

if __name__ == "__main__":
    main()