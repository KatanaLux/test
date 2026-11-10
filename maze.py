from pygame import *
import sys

init()
mixer.init()

window = display.set_mode((700, 500))
display.set_caption("Maze")

background = transform.scale(
    image.load("background.jpg"),
    (700, 500)
)

mixer.music.load("jungles.ogg")
mixer.music.play(-1)

money_sound = mixer.Sound("money.ogg")
kick_sound = mixer.Sound("kick.ogg")

clock = time.Clock()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image),
            (size_x, size_y)
        )
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.start_x = player_x
        self.start_y = player_y

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 75:
            self.rect.x -= 5
        if keys[K_d] and self.rect.x < 605:
            self.rect.x += 5
        if keys[K_w] and self.rect.y > 55:
            self.rect.y -= 5
        if keys[K_s] and self.rect.y < 435:
            self.rect.y += 5

    def respawn(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.direction = "right"

    def update(self):
        if self.rect.x <= 145:
            self.direction = "right"
        if self.rect.x >= 565:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= 3
        else:
            self.rect.x += 3


class Wall(sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


hero = Player("hero.png", 100, 400, 60, 60)
cyborg = Enemy("cyborg.png", 350, 60, 60, 60)
treasure = GameSprite("treasure.png", 570, 400, 60, 60)

GREEN = (100, 220, 80)

walls = [
    Wall(GREEN, 50, 30, 600, 20),
    Wall(GREEN, 50, 30, 20, 450),
    Wall(GREEN, 50, 460, 600, 20),
    Wall(GREEN, 630, 30, 20, 450),

    Wall(GREEN, 120, 100, 20, 250),
    Wall(GREEN, 120, 100, 300, 20),
    Wall(GREEN, 400, 100, 20, 150),
    Wall(GREEN, 500, 200, 20, 250),
    Wall(GREEN, 200, 350, 20, 110),
    Wall(GREEN, 280, 250, 150, 20),
    Wall(GREEN, 300, 350, 200, 20),
    Wall(GREEN, 450, 350, 20, 110),
]

main_font = font.Font(None, 70)
win_text = main_font.render("ТЫ ПОБЕДИЛ, УРА!", True, (255, 215, 0))
lose_text = main_font.render("БРО, УЧИСЬ ИГРАТЬ!", True, (200, 30, 30))

small_font = font.Font(None, 40)

game = True
finish = False
lives = 3

hurt_timer = 0
hurt_cooldown = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))

        for w in walls:
            w.reset()

        hero.reset()
        hero.update()

        cyborg.reset()
        cyborg.update()

        treasure.reset()

        if hurt_timer > 0:
            hurt_timer -= 1

        if sprite.collide_rect(hero, treasure):
            finish = True
            money_sound.play()

        if hurt_timer == 0:
            for w in walls:
                if sprite.collide_rect(hero, w):
                    lives -= 1
                    kick_sound.play()
                    hero.respawn()
                    hurt_timer = hurt_cooldown
                    break

        if hurt_timer == 0 and sprite.collide_rect(hero, cyborg):
            lives -= 1
            kick_sound.play()
            hero.respawn()
            hurt_timer = hurt_cooldown

        if lives <= 0:
            finish = True
            kick_sound.play()

        lives_text = small_font.render(f"Жизни: {lives}", True, (255, 255, 255))
        window.blit(lives_text, (20, 20))

    else:
        window.blit(background, (0, 0))
        for w in walls:
            w.reset()
        cyborg.reset()
        treasure.reset()
        hero.reset()
        if lives <= 0:
            window.blit(lose_text, (50, 200))
        else:
            window.blit(win_text, (50, 200))

    display.update()
    clock.tick(60)

quit()
sys.exit()