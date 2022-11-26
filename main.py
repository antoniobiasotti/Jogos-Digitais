import pygame
import sys
from pygame.locals import *
import random
from pygame import mixer


pygame.init()

sw = 800
sh = 600

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption('Game Space Defenders')

pygame.mixer.music.load('sounds/Menu.ogg')
pygame.mixer.music.play(-1)
music = True

somclick = mixer.Sound('sounds/menu_selection_click.wav')

menu_bg = pygame.image.load('img/menu.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, (sw, sh))

score_value = 0

# Fonts
fonte_menu = pygame.font.Font('fonts/hachicro.TTF', 50)
fonte_menu2 = pygame.font.Font('fonts/hachicro.TTF', 40)
fonte_historia = pygame.font.Font('fonts/Phatone-Regular.otf', 12)
fonte_regras = pygame.font.Font('fonts/Gamer.ttf', 35)
fonte_regras2 = pygame.font.Font('fonts/Gamer.ttf', 42)
font = pygame.font.Font('fonts/BungeeSpice-Regular.ttf', 32)
font_credits1 = pygame.font.Font('fonts/game_over.ttf', 72)
font_credits2 = pygame.font.Font('fonts/monstapix.ttf', 12)

# Texts
menu_titulo = "SPACE DEFENDERS"
menu_play = "PLAY"
menu_instructions = "INSTRUCTIONS"
menu_quit = "QUIT"
menu_credits = "CREDITS"

historia = "Em 2054, a humanidade colonizou Marte, "
historia2 = "mas o descaso do homem com a preservação do planeta tornou "
historia3 = "a Terra inabitável. Diante dessa crise global, você foi escolhido para fazer parte de um esquadrão da NASA criado para "
historia4 = "abrir caminho pelo lixo espacial até o planeta vermelho, garantindo "
historia5 = "assim, que todos cheguem em segurança lá. O futuro da humanidade "
historia6 = "está em suas mãos, "
historia7 = "Boa sorte."
pressspace = "PRESSIONE ENTER PARA DECOLAR"

instructions1 = 'Instruções:'
rule1 = 'Objetivo do jogo: O objetivo é fazer o máximo de pontos, por meio '
rule2 = 'da destruição dos lixos espaciais.'
instructions2 = 'Poderes no jogo:'
rule3 = 'Tiro duplo - boost que aumentará o ataque do jogador através de '
rule4 = 'um tiro extra'
rule5 = 'Vida - concede 20% da vida base'
instructions3 = 'Jogabilidade:'
rule6 = 'Setas - o jogador conseguirá movimentar sua nave em todas '
rule7 = 'direções e ao passar por cima de um poder, será possível usá-lo'
rule8 = 'Barra de Espaço - o jogador conseguirá atirar nos lixos espaciais '
rule9 = 'e nos asteroides'
instructions4 = 'Fim do jogo:'
rule10 = 'O jogo se encerra quando o jogador é atingido 5 vezes.'
press_escape = "PRESSIONE ESC PARA VOLTAR AO MENU"

credits1 = 'Créditos'
c1 = 'Design.....................................................................................Gabriel Moreira Cabral'
c2 = 'Sound Effects.....................................................................................Benjamin Kim'
c3 = 'Narratology.....................................................................................Enzo Cecone'
c4 = 'Game Dev.....................................................................................Augusto Koshiyama'
c5 = 'Game Dev.....................................................................................Antonio Biasotti'

# Buttons
button_play_x = 100
button_play_y = 255
button_instructions_x = 100
button_instructions_y = 310
button_quit_x = 100
button_quit_y = 420
button_credits_x = 100
button_credits_y = 366

textX = 10
textY = 10

POWERUPTIME = 8000

musicicon = pygame.image.load('img/music.png')
rect_music = musicicon.get_rect()
rect_music.x = 750
rect_music.y = 10

nave = pygame.image.load('img/navezinha.png')
tiro = pygame.image.load('img/tiro.png')
gameover = pygame.image.load('img/gameover.png')

game_over = 0

ret_play = pygame.Rect(322, 254, 100, 43)
ret_quit = pygame.Rect(322, 374, 95, 43)

game_bg = pygame.image.load('img/espaco.png').convert_alpha()
game_bg = pygame.transform.scale(game_bg, (sw, sh))

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(('img/navezinha.png')).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (50, 40))
        self.rect = self.surf.get_rect(
            center=(
                400,
                550,
            )
        )
        self.bullets = []
        self.cool_down_count = 0
        self.hitbox = (self.rect.x, self.rect.y, 64, 64)
        self.health = 100
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    #Movimento
    def update(self, tecla):
        game_over = 0
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUPTIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if tecla[K_UP]:
            self.rect.move_ip(0, -6.5)
        if tecla[K_DOWN]:
            self.rect.move_ip(0, 6.5)
        if tecla[K_LEFT]:
            self.rect.move_ip(-6.5, 0)
        if tecla[K_RIGHT]:
            self.rect.move_ip(6.5, 0)

        # Constrain
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > sw:
            self.rect.right = sw
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= sh:
            self.rect.bottom = sh

        if player.health <= 0:
            explosion = Explosion(player.rect.x + 15, player.rect.y + 10, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over

    def draw(self, screen):
        self.hitbox = (self.rect.x - 20, self.rect.y - 45, 90, 110)
        pygame.draw.rect(screen, (255, 0, 0), (680, 15, 100, 10))
        if self.health >= 0:
            pygame.draw.rect(screen, (0, 255, 0), (680, 15, self.health, 10))

    def cooldown(self):
        if self.cool_down_count >= 12:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self, tecla):
        self.hit()
        self.cooldown()
        if self.power == 1:
            if tecla[K_SPACE] and self.cool_down_count == 0:
                bullet = Bullet(self.rect.x, self.rect.y)
                self.bullets.append(bullet)
                somtiro = mixer.Sound('sounds/laser1.wav')
                somtiro.play()
                self.cool_down_count = 1
            for bullet in self.bullets:
                bullet.move()
                if bullet.off_screen():
                    self.bullets.remove(bullet)
        if self.power >= 2:
            if tecla[K_SPACE] and self.cool_down_count == 0:
                bullet1 = Bullet(self.rect.x - 10, self.rect.y)
                bullet2 = Bullet(self.rect.x + 10, self.rect.y)
                self.bullets.append(bullet1)
                self.bullets.append(bullet2)
                somtiro = mixer.Sound('sounds/laser1.wav')
                somtiro.play()
                self.cool_down_count = 1
            for bullet in self.bullets:
                bullet.move()
                if bullet.off_screen():
                    self.bullets.remove(bullet)

    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:
                    explosion = Explosion(enemy.rect.x + 20, enemy.rect.y + 40, 2)
                    explosion_group.add(explosion)
                    global score_value
                    enemy.kill()
                    destroy = mixer.Sound('sounds/destroimeteoro.wav')
                    destroy.play()
                    self.bullets.remove(bullet)
                    score_value += 5
        for spacetrash in trashes:
            for bullet in self.bullets:
                if spacetrash.hitbox[0] < bullet.x < spacetrash.hitbox[0] + spacetrash.hitbox[2] and spacetrash.hitbox[1] < bullet.y < spacetrash.hitbox[1] + spacetrash.hitbox[3]:
                    explosion = Explosion(spacetrash.rect.x + 20, spacetrash.rect.y + 40, 2)
                    explosion_group.add(explosion)
                    spacetrash.kill()
                    destroy = mixer.Sound('sounds/destroimeteoro.wav')
                    destroy.play()
                    self.bullets.remove(bullet)
                    score_value += 20

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(('img/meteoro roxo ' + str(random.randint(2, 3)) + '.png')).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (75, 75))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(sw + 30, sw + 100),
                random.randint(100, sh - 50),
            )
        )
        self.speed = random.randint(3, 15)
        self.hitbox = (self.rect.x, self.rect.y, 64, 64)


    def draw(self, screen):
        self.hitbox = (self.rect.x - 20, self.rect.y, 100, 70)

    def update(self):
        self.hit()
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def hit(self):
        if player.hitbox[0] < self.rect.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < self.rect.y + 32 < player.hitbox[1] + player.hitbox[3]:
            explosion = Explosion(player.rect.x + 15, player.rect.y + 10, 2)
            explosion_group.add(explosion)
            global score_value
            player.health -= 21
            self.kill()
            damage = mixer.Sound('sounds/damagesound.wav')
            damage.play()
            score_value -= 10
            if score_value <= 0:
                score_value = 0

class Trash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(('img/lixo ' + str(random.randint(1, 2)) + '.png')).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (100, 100))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(sw + 30, sw + 100),
                random.randint(100, sh - 100),
            )
        )
        self.speed = random.randint(3, 15)
        self.hitbox = (self.rect.x, self.rect.y, 64, 64)

    def draw(self, screen):
        self.hitbox = (self.rect.x - 20, self.rect.y, 110, 70)

    def update(self):
        self.hit()
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

    def hit(self):
        if player.hitbox[0] < self.rect.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < self.rect.y + 32 < player.hitbox[1] + player.hitbox[3]:
            explosion = Explosion(player.rect.x + 15, player.rect.y + 10, 2)
            explosion_group.add(explosion)
            global score_value
            player.health -= 41
            self.kill()
            damage = mixer.Sound('sounds/damagesound.wav')
            damage.play()
            score_value -= 20
            if score_value <= 0:
                score_value = 0

class Bullet:
    def __init__(self, x, y):
        self.x = x + 10
        self.y = y - 40

    def draw_bullet(self):
        screen.blit(tiro, (self.x, self.y))

    def move(self):
        self.y -= 15

    def off_screen(self):
        return not(self.y + 100 >= 0 and self.y <= sh)

class Pow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['vida', 'doubleshot'])
        self.surf = powerup_images[self.type]
        self.surf = pygame.transform.scale(self.surf, (50, 50))
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(sw + 30, sw + 100),
                random.randint(100, sh - 50),
            )
        )
        self.speed = random.randint(3, 10)
        self.hitbox = (self.rect.x, self.rect.y, 64, 64)

    def draw(self, screen):
        self.hitbox = (self.rect.x - 20, self.rect.y, 100, 70)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

def apresentacao():

  while True:

    pygame.display.set_caption('Apresentação')
    for evento in pygame.event.get():
      if evento.type == QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == KEYDOWN:
        if evento.key == K_ESCAPE:
          menu(sh)
        elif evento.key == K_RETURN:
            somclick.play()
            start_game()
    screen.fill((0, 0, 0))
    intro = fonte_historia.render(historia, True, (0, 247, 0))
    screen.blit(intro, (10, 70))
    intro = fonte_historia.render(historia2, True, (0, 247, 0))
    screen.blit(intro, (10, 95))
    intro = fonte_historia.render(historia3, True, (0, 247, 0))
    screen.blit(intro, (10, 120))
    intro = fonte_historia.render(historia4, True, (0, 247, 0))
    screen.blit(intro, (10, 145))
    intro = fonte_historia.render(historia5, True, (0, 247, 0))
    screen.blit(intro, (10, 170))
    intro = fonte_historia.render(historia6, True, (0, 247, 0))
    screen.blit(intro, (10, 195))
    intro = fonte_historia.render(historia7, True, (0, 247, 0))
    screen.blit(intro, (100, 285))
    intro = fonte_historia.render(pressspace, True, (0, 247, 0))
    screen.blit(intro, (230, 520))

    pygame.display.update()

def instructions():

  while True:

    pygame.display.set_caption('Instructions')
    for evento in pygame.event.get():
      if evento.type == QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == KEYDOWN:
        if evento.key == K_ESCAPE:
            somclick.play()
            menu(sh)
    screen.fill((0, 0, 0))
    regra = fonte_regras.render(instructions1, True, (0, 247, 0))
    screen.blit(regra, (10, 10))
    regra = fonte_regras.render(rule1, True, (0, 255, 127))
    screen.blit(regra, (10, 35))
    regra = fonte_regras.render(rule2, True, (0, 255, 127))
    screen.blit(regra, (10, 60))
    regra = fonte_regras.render(instructions2, True, (0, 247, 0))
    screen.blit(regra, (10, 105))
    regra = fonte_regras.render(rule3, True, (0, 255, 127))
    screen.blit(regra, (10, 130))
    regra = fonte_regras.render(rule4, True, (0, 255, 127))
    screen.blit(regra, (10, 155))
    regra = fonte_regras.render(rule5, True, (0, 255, 127))
    screen.blit(regra, (10, 200))
    regra = fonte_regras.render(instructions3, True, (0, 247, 0))
    screen.blit(regra, (10, 245))
    regra = fonte_regras.render(rule6, True, (0, 255, 127))
    screen.blit(regra, (10, 270))
    regra = fonte_regras.render(rule7, True, (0, 255, 127))
    screen.blit(regra, (10, 295))
    regra = fonte_regras.render(rule8, True, (0, 255, 127))
    screen.blit(regra, (10, 340))
    regra = fonte_regras.render(rule9, True, (0, 255, 127))
    screen.blit(regra, (10, 365))
    regra = fonte_regras.render(instructions4, True, (0, 247, 0))
    screen.blit(regra, (10, 410))
    regra = fonte_regras.render(rule10, True, (0, 255, 127))
    screen.blit(regra, (10, 435))
    regra = fonte_regras2.render(press_escape, True, (0, 247, 0))
    screen.blit(regra, (160, 520))

    pygame.display.update()

def credits():
    while True:
        pygame.display.set_caption('Créditos')
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    somclick.play()
                    menu(sh)
        screen.fill((0, 0, 0))
        logo = pygame.image.load('img/pychads.png').convert_alpha()
        screen.blit(logo, (70, 40))
        c = font_credits1.render(credits1, True, (0, 247, 0))
        screen.blit(c, (320, 50))
        c = font_credits1.render(c1, True, (0, 247, 0))
        screen.blit(c, (40, 145))
        c = font_credits1.render(c2, True, (0, 247, 0))
        screen.blit(c, (40, 175))
        c = font_credits1.render(c3, True, (0, 247, 0))
        screen.blit(c, (40, 205))
        c = font_credits1.render(c4, True, (0, 247, 0))
        screen.blit(c, (40, 235))
        c = font_credits1.render(c5, True, (0, 247, 0))
        screen.blit(c, (40, 270))
        pygame.display.update()

def menu(sh):
    while True:
        pygame.display.set_caption('Menu - Space Defenders')
        rel_y = sh % menu_bg.get_rect().height
        screen.blit(menu_bg, (0, rel_y - menu_bg.get_rect().height))
        if rel_y < sh:
            screen.blit(menu_bg, (0, rel_y))
        sh += 0.1

        titulo = fonte_menu.render(menu_titulo, True, (0, 247, 0))
        screen.blit(titulo, (47, 75))
        play = fonte_menu2.render(menu_play, True, (255, 255, 255))
        screen.blit(play, (button_play_x, button_play_y))
        instructions_button = fonte_menu2.render(menu_instructions, True, (255, 255, 255))
        screen.blit(instructions_button, (button_instructions_x, button_instructions_y))
        quitgame = fonte_menu2.render(menu_quit, True, (255, 255, 255))
        screen.blit(quitgame, (button_quit_x, button_quit_y))
        creditstext = fonte_menu2.render(menu_credits, True, (255, 255, 255))
        screen.blit(creditstext, (button_credits_x, button_credits_y))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                if click[0] in range(button_play_x, button_play_x + 160) and click[1] in range(button_play_y, button_play_y + 40):
                    somclick.play()
                    apresentacao()
                if click[0] in range(button_instructions_x, button_instructions_x + 465) and click[1] in range(button_instructions_y, button_instructions_y + 38):
                    somclick.play()
                    instructions()
                if click[0] in range(button_quit_x, button_quit_x + 150) and click[1] in range(button_quit_y, button_quit_y + 38):
                    somclick.play()
                    pygame.quit()
                    sys.exit()
                if click[0] in range(button_credits_x, button_credits_x + 270) and click[1] in range(button_credits_y, button_credits_y + 40):
                    somclick.play()
                    credits()
        pygame.display.update()


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def start_game():
    global sprite_sheet
    pygame.display.set_caption('Space Defenders')

    game_over = 0
    JogoAtivo = True

    while JogoAtivo:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == QUIT:
                #JogoAtivo = False
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu(sh)
                elif tecla[K_F10]:
                    if music:
                        pygame.mixer.music.pause()
                        music = False
                    else:
                        pygame.mixer.music.unpause()
                        music = True

            if event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            if event.type == ADDBOOST:
                pow = Pow()
                powerups.add(pow)
                all_sprites.add(pow)

            if event.type == ADDTRASH:
                trash = Trash()
                trashes.add(trash)
                all_sprites.add(trash)

        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'vida':
                player.health += 21
                regen = mixer.Sound('sounds/somvida.wav')
                regen.play()
                if player.health >= 100:
                    player.health = 100
            if hit.type == 'doubleshot':
                doublegun = mixer.Sound('sounds/somshot.wav')
                doublegun.play()
                player.powerup()

        tecla = pygame.key.get_pressed()

        player.shoot(tecla)

        enemies.update()

        powerups.update()

        trashes.update()

        screen.blit(game_bg, (0, 0))

        player.draw(screen)

        explosion_group.update()
        explosion_group.draw(screen)

        show_score(textX, textY)

        for bullet in player.bullets:
            bullet.draw_bullet()

        for enemy in enemies:
            enemy.draw(screen)

        for life in powerups:
            life.draw(screen)

        for spacetrash in trashes:
            spacetrash.draw(screen)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if game_over == 0:
            game_over = player.update(tecla)
        else:
            if game_over == -1:
                pygame.display.update()
                somexplosao = mixer.Sound('sounds/explosion.wav')
                somgrito = mixer.Sound('sounds/dano.mp3')
                somexplosao.set_volume(0.25)
                somexplosao.play()
                somgrito.play()
                pygame.time.delay(1500)
                pygame.mixer.music.load('sounds/gameover.mp3')
                screen.blit(gameover, (125, 150))
                pygame.mixer.music.play()
                pygame.display.update()
                pygame.time.delay(3000)
                JogoAtivo = False
                player.rect.x = 400
                player.rect.y = 550
                all_sprites.add(player)
                player.health = 100
                score_value = 0
                pygame.mixer.music.load('sounds/Menu.ogg')
                pygame.mixer.music.play(-1)
                menu(sh)
        pygame.display.update()

ADDENEMY = pygame.USEREVENT + 0
pygame.time.set_timer(ADDENEMY, 500)

ADDBOOST = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBOOST, 15000)

ADDTRASH = pygame.USEREVENT + 2
pygame.time.set_timer(ADDTRASH, 6000)

powerup_images = {}
powerup_images['vida'] = pygame.image.load(('img/boostvida.png')).convert()
powerup_images['doubleshot'] = pygame.image.load(('img/double_shot.png')).convert()

player = Player()

enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
trashes = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load('sounds/Menu.ogg')
pygame.mixer.music.play(-1)
menu(sh)
