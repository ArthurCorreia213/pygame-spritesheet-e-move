import pygame
import sys

from spritesheet_explicada import SpriteSheet
from sprite_teste_v2 import Personagem
from inimigo_teste import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()  # Inicializa o relógio do jogo para controlar a taxa de quadros

#omori_sprite_sheet = SpriteSheet("omori_sprites/PC Computer - Omori - Omori.png", 0, 15, 32, 32, 4,[3,3,3,3], (0, 0, 0))

bg = pygame.image.load("fundo.png")

camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

novo_sprite = SpriteSheet("omori_sprites/Download5005.png", 0, 512, 64, 64, 4,[7 for i in range(34)], (0, 0, 0))

game_over = pygame.image.load("GAME_OVER.png")

# Cria o objeto player utilizando a classe Personagem e a imagem inicial

player = Personagem(novo_sprite)

enemy = Inimigo(player_rect=player.rect)

inimigos = pygame.sprite.Group()

player_group = pygame.sprite.Group()

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
player_group.add(player)

all_sprites.add(enemy)
inimigos.add(enemy)

contador = 0

run = True  # Variável de controle do loop principal
while run:

    clock.tick(60)  # Limita a atualização para 3 FPS (controla a velocidade da animação)

    screen.fill((100, 100, 100))  # Preenche o fundo com uma cor sólida

    #print(player.sheet.action)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.direction = 'UP'
    elif keys[pygame.K_s]:
        player.direction = 'DOWN'
    elif keys[pygame.K_a]:
        player.direction = 'LEFT'
    elif keys[pygame.K_d]:
        player.direction = 'RIGHT'
    else:
        player.direction = None  # Nenhuma direção se nenhuma tecla for pressionada


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.direction = None
            elif event.key == pygame.K_s:
                player.direction = None
            elif event.key == pygame.K_a:
                player.direction = None
            elif event.key == pygame.K_d:
                player.direction = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.nova_direcao = True
            elif event.key == pygame.K_s:
                player.nova_direcao = True
            elif event.key == pygame.K_a:
                player.nova_direcao = True
            elif event.key == pygame.K_d:
                player.nova_direcao = True
            elif event.key == pygame.K_LSHIFT:
                player.correr()

    click = pygame.mouse.get_pressed()[0]

    mouse_pos = pygame.mouse.get_pos()
    
    if click:
        if contador % 20 == 0:
            player.shoot(mouse_pos)
        #print(mouse_pos)

    # Atualiza os sprites
    all_sprites.update()

    camera.center = player.rect.center

    if player.rect.left <= -15:
        player.rect.left = -15

    if player.rect.right >= bg.get_width()-10:
        player.rect.right = bg.get_width()-10

    if player.rect.bottom >= bg.get_height()-28:
        player.rect.bottom = bg.get_height()-28

    if player.rect.top <= -15:
        player.rect.top = -15

    camera.left = max(0, camera.left)
    camera.top = max(0, camera.top)
    camera.right = min(bg.get_width(), camera.right)
    camera.bottom = min(bg.get_height(), camera.bottom)

    screen.blit(bg, (0, 0), camera)

    contador+=1

    # if contador % 50 == 0:
    #     for enemy in inimigos:
    #         enemy.HP -=1
    #         print(enemy.HP)
    #         if enemy.HP == 0:
    #             enemy.image = pygame.Surface((32, 32), pygame.SRCALPHA)
    #             inimigos.remove(enemy)
    #             all_sprites.remove(enemy)

    if contador % 30 == 0:
        enemy.shoot(player.rect)
    if contador % 1000 == 0:
        if enemy.mover:
            enemy.mover = False
        else:
            enemy.mover = True

    player_hits =  pygame.sprite.groupcollide(player.balas,inimigos, False, False)
    enemy_hits = pygame.sprite.groupcollide(enemy.balas, player_group, False, False)

    if len(enemy_hits)>0:
        a = (enemy_hits.keys())
        enemy.balas.remove(a)
        
        player.HP -= 1
        print(player.HP)
        #enemy.remover_todas_balas()

    if len(player_hits) > 0:
        a = (player_hits.keys())
        player.balas.remove(a)

        enemy.HP -= 1
        print(enemy.HP)
        #player.remover_todas_balas()

    if enemy.HP == 0:
        enemy.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        enemy.remover_todas_balas()
        inimigos.remove(enemy)
        all_sprites.remove(enemy)

    enemy.draw_balas(screen,camera)
    player.draw_balas(screen,camera)

    screen.blit(enemy.image, (enemy.rect.x - camera.left, enemy.rect.y - camera.top))

    player.sheet.draw(screen, player.rect.x - camera.left , player.rect.y - camera.top)

    if player.HP == 0:
        player.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        player.remover_todas_balas()
        player_group.remove(player)
        all_sprites.remove(player)
        screen.fill((0,0,0))

    pygame.display.update()  # Atualiza a tela com as novas imagens
