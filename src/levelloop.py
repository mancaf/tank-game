"""Main level loop."""

# Imports

import pygame
import sys
import os

from . import utils
from .bullet_cursor import Cursor
from .aiplayer import Player, YellowAI, YellowPlusAI, BlueAI, BluePlusAI, \
    RedAI, RedPlusAI, PurpleAI, PurplePlusAI, Spawner, SpawnerPlus
from .importation import get_level, get_unlocked, overwrite_unlocked

from pygame_assets import load
from .assets import get_font

join = os.path.join
path = os.getcwd()


# Programme principal

def pause(screen, player, background, walls_group, AI_group, bullets_group,
          all_dead_AI, all_spawners, all_dead_spawners, all_spawned_AI):
    """Pause loop."""
    global clickSound
    paused = True
    font = get_font(36)
    resume = utils.Button("Resume Game", font, 512, 200, (200, 0, 0))
    exit = utils.Button("Return to Menu", font, 512, 300, (200, 0, 0))

    cursor = Cursor()
    c = pygame.time.Clock()

    while paused:
        c.tick(60)
        screen.blit(background.image, (0, 0))

        cursor.update()

        screen.blit(player.body.image, player.body.rect)
        screen.blit(player.canon.image, player.canon.rect)

        for IA in AI_group:
            screen.blit(IA.body.image, IA.body.rect)
            screen.blit(IA.canon.image, IA.canon.rect)
        for IA in all_dead_AI:
            screen.blit(IA.body.image, IA.body.rect)
        for IA in all_spawners:
            screen.blit(IA.image, IA.rect)
        for IA in all_dead_spawners:
            screen.blit(IA.image, IA.rect)
        for bullet in bullets_group:
            screen.blit(bullet.image, bullet.rect)
        for IA in all_spawned_AI:
            screen.blit(IA.body.image, IA.body.rect)
            screen.blit(IA.canon.image, IA.canon.rect)
        for wall in walls_group:
            screen.blit(wall.image, wall.rect)

        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                    resume.hover):
                clickSound.play()
                return False
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                    exit.hover):
                clickSound.play()
                return True
            if event.type == pygame.QUIT:  # le player choisit de quitter
                clickSound.play()
                pygame.mixer.music.fadeout(200)
                c.tick(5)
                pygame.quit()
                return True

        resume.update()
        exit.update()
        pygame.display.flip()


def dead_menu(screen, player, background, walls_group, AI_group, bullets_group,
              all_dead_AI, all_spawners, all_dead_spawners, all_spawned_AI):
    """Dead menu loop."""
    global clickSound
    paused = True
    font1 = get_font(36)
    recommencer = utils.Button("Try Again", font1, 512, 220, (200, 0, 0))
    quitter = utils.Button("Return to Menu", font1, 512, 350, (200, 0, 0))
    font2 = get_font(50)
    you_died = font2.render("You died!", 1, (200, 0, 0))
    you_died_pos = you_died.get_rect(centerx=512, centery=150)
    cursor = Cursor()
    c = pygame.time.Clock()
    deadimg = load.image('tank_destroyed.png')

    while paused:
        c.tick(60)
        screen.blit(background.image, (0, 0))

        cursor.update()

        screen.blit(deadimg, player.body.rect)

        for IA in AI_group:
            screen.blit(IA.body.image, IA.body.rect)
            screen.blit(IA.canon.image, IA.canon.rect)
        for IA in all_dead_AI:
            screen.blit(IA.body.image, IA.body.rect)
        for IA in all_spawners:
            screen.blit(IA.image, IA.rect)
        for IA in all_dead_spawners:
            screen.blit(IA.image, IA.rect)
        for bullet in bullets_group:
            screen.blit(bullet.image, bullet.rect)
        for IA in all_spawned_AI:
            screen.blit(IA.body.image, IA.body.rect)
            screen.blit(IA.canon.image, IA.canon.rect)
        for wall in walls_group:
            screen.blit(wall.image, wall.rect)

        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                    recommencer.hover):
                clickSound.play()
                pygame.mixer.fadeout(200)
                return True
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                    quitter.hover):
                clickSound.play()
                pygame.mixer.music.fadeout(200)
                return False
            if event.type == pygame.QUIT:  # le player choisit de quitter
                clickSound.play()
                pygame.mixer.music.fadeout(200)
                c.tick(5)
                pygame.quit()
                return False
        screen.blit(you_died, you_died_pos)
        recommencer.update()
        quitter.update()
        pygame.display.flip()


# n est le numéro du niveau qui va être joué.
# On va chercher un niveau custom si custom=True
def main(n, custom=False, start=False, from_selection=False):
    """Main level loop."""
    global clickSound
    pygame.display.set_caption("Level %d" % n)
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()
    walls_group, pits_group, pos_joueur, pos_IA, points_list = get_level(
        path, n, custom)
    pygame.mouse.set_visible(False)       # remplacement de la souris
    curseur = Cursor()
    walls_pits = pygame.sprite.Group()
    unlocked = get_unlocked()  # les niveaux disponibles
    font = get_font(36)
    clickSound = load.sound("click_sound.wav")
    v = utils.get_volume('music')

    # Si on a lancé le niveau depuis le menu (pas de changement de musique
    # lors de l'enchainement de deux niveaux
    if start:
        if sys.platform == "win32":
            load.music('MainTheme.ogg', volume=v)
        else:
            load.music('MainTheme.wav', volume=v)
        pygame.mixer.music.play(-1)

    for elt in walls_group:
        walls_pits.add(elt)
    for elt in pits_group:
        walls_pits.add(elt)

    background = utils.Background(n, custom)

    pygame.font.init()
    font = get_font(18)
    if (n == 1 or n == 2) and not custom:
        if n == 1:
            help_msg1 = font.render("Use the mouse to control your cannon", 1,
                                    (69, 52, 16))
            msgpos1 = help_msg1.get_rect(centerx=800, centery=600)
            help_msg2 = font.render("and press left click to fire a bullet.",
                                    1, (69, 52, 16))
            msgpos2 = help_msg2.get_rect(centerx=800, centery=630)
        else:
            help_msg1 = font.render(
                "Use Z,Q,S,D or up, down, left and right to move.", 1,
                (69, 52, 16))
            msgpos1 = help_msg1.get_rect(centerx=700, centery=600)
            help_msg2 = font.render("Press ESC to pause at any moment.",
                                    1, (69, 52, 16))
            msgpos2 = help_msg2.get_rect(centerx=800, centery=630)

    player = Player(pos_joueur)

    AI_group = []
    all_dead_AI = []
    all_spawners = []
    all_dead_spawners = []
    all_spawned_AI = []

    for element in pos_IA:
        if element[0] == 'yellow':
            yellow = YellowAI(element[1], pos_joueur)
            AI_group.append(yellow)
        if element[0] == 'yellowPlus':
            yellowp = YellowPlusAI(element[1], pos_joueur)
            AI_group.append(yellowp)
        elif element[0] == 'blue':
            blue = BlueAI(element[1], pos_joueur, points_list.pop(0))
            AI_group.append(blue)
        elif element[0] == 'bluePlus':
            bluep = BluePlusAI(element[1], pos_joueur, points_list.pop(0))
            AI_group.append(bluep)
        elif element[0] == 'red':
            red = RedAI(element[1], pos_joueur)
            AI_group.append(red)
        elif element[0] == 'redPlus':
            redp = RedPlusAI(element[1], pos_joueur)
            AI_group.append(redp)
        elif element[0] == 'purple':
            purple = PurpleAI(element[1], pos_joueur, points_list.pop(0))
            AI_group.append(purple)
        elif element[0] == 'purplePlus':
            purplep = PurplePlusAI(element[1], pos_joueur, points_list.pop(0))
            AI_group.append(purplep)
        elif element[0] == 'spawner':
            spawner = Spawner('spawner.png', element[1])
            all_spawners.append(spawner)
        elif element[0] == 'spawnerPlus':
            spawnerp = SpawnerPlus('spawnerPlus.png', element[1])
            all_spawners.append(spawnerp)

    bullets_group = pygame.sprite.Group()

    RUNNING = 1  # variable de boucle
    # On lance la boucle de jeu
    if sys.platform == "win32":
        deadTheme = load.sound("DeadTheme.ogg")
    else:
        deadTheme = load.sound("DeadTheme.wav")
        deadTheme.set_volume(v)
    has_begun = False
    begin_msg = font.render("CLICK TO BEGIN !", 1, (200, 0, 0))
    begin_msg_rect = begin_msg.get_rect(centerx=player.body.rect.centerx,
                                        centery=player.body.rect.centery - 50)

    while RUNNING:
        clock.tick(60)  # on maximise le fps à 60
        if has_begun:
            if player.alive:
                # 1/ Gestion d'évènements divers
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and len(player.bullets) < 4:
                            # si clic gauche, on crée un boulet
                            player.fire_sound.play()
                            pos = (event.pos[0], event.pos[1])
                            blt = player.create_bullet(pos)
                            player.bullets.add(blt)
                            bullets_group.add(blt)
                    elif event.type == pygame.QUIT:
                        RUNNING = 0
                        pygame.mixer.music.fadeout(200)
                        clock.tick(5)
                        pygame.quit()
                        return False
                # 2/ On gère les déplacements du player
                keys = pygame.key.get_pressed()
                right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
                left = keys[pygame.K_LEFT] or keys[pygame.K_a]
                up = keys[pygame.K_UP] or keys[pygame.K_w]
                down = keys[pygame.K_DOWN] or keys[pygame.K_s]

                player.move(right, left, up, down)

                if keys[pygame.K_ESCAPE]:
                    end = pause(screen, player, background, walls_pits,
                                AI_group, bullets_group,
                                all_dead_AI, all_spawners,
                                all_dead_spawners, all_spawned_AI)
                    if end:
                        try:
                            pygame.mixer.music.fadeout(200)
                            clock.tick(5)
                            RUNNING = 0  # on retourne au menu
                            return False
                        except:
                            return False

                # 3/ On met à jour les sprites

                collisions_dict = pygame.sprite.groupcollide(
                    bullets_group, walls_group, False, False,
                    pygame.sprite.collide_rect)

                screen.blit(background.image, (0, 0))

                # affichage des messages d'aide dans les premiers niveaux

                if (n == 1 or n == 2) and not custom:
                    screen.blit(help_msg1, msgpos1)
                    screen.blit(help_msg2, msgpos2)

                # affichage des sprites morts
                for IA in all_dead_AI:
                    screen.blit(IA.body.image, IA.body.rect)
                for spawner in all_dead_spawners:
                    screen.blit(spawner.image, spawner.rect)

                for bullet in bullets_group:
                    if bullet in collisions_dict:
                        bullet.kill()
                for elt in walls_pits:
                    screen.blit(elt.image, elt.rect)

                bullets_group.update()

                player.update(path, pygame.mouse.get_pos(), bullets_group,
                              walls_pits)

                for IA in AI_group:
                    if IA.alive:
                        bullets = IA.update(path, player.body.rect.center,
                                            walls_group, pits_group,
                                            bullets_group)
                        if bullets is not None:
                            for bullet in bullets:
                                bullets_group.add(bullet)
                    else:
                        (x, y) = IA.body.rect.center
                        IA.body.image, IA.body.rect = load.image_with_rect(
                            'tank_destroyed.png')
                        IA.body.rect.center = (x, y)
                        all_dead_AI.append(IA)
                        AI_group.remove(IA)

                for IA in all_spawned_AI:
                    if IA.alive:
                        bullets = IA.update(path, player.body.rect.center,
                                            walls_group, pits_group,
                                            bullets_group)
                        if bullets is not None:
                            for bullet in bullets:
                                bullets_group.add(bullet)
                    else:
                        (x, y) = IA.body.rect.center
                        IA.body.image, IA.body.rect = load.image_with_rect(
                            'tank_destroyed.png')
                        IA.body.rect.center = (x, y)
                        all_dead_AI.append(IA)
                        IA.id.spawned = False
                        all_spawned_AI.remove(IA)

                for spawner in all_spawners:
                    if spawner.alive:
                        IAspawned = spawner.update(
                            path, player.body.rect.center, bullets_group)
                        if IAspawned is not None:
                            all_spawned_AI.append(IAspawned)
                    else:
                        all_spawners.remove(spawner)
                        center = spawner.rect.center
                        spawner.image, spawner.rect = load.image_with_rect(
                            'spawner_destroyed.png')
                        spawner.rect.center = center
                        all_dead_spawners.append(spawner)

                curseur.update()

                # toutes les IA ont été détruites, on a gagné
                if all(len(g) == 0
                       for g in (AI_group, all_spawned_AI, all_spawners)):
                    if not unlocked[n] and not custom:
                        unlocked[n] = 1  # le niveau suivant est débloqué
                        overwrite_unlocked(unlocked)
                    if from_selection:
                        pygame.mixer.music.fadeout(200)
                        clock.tick(5)
                    return True
                # 4/ on met à jour l'ensemble de l'image
                pygame.display.flip()

            else:   # le player est mort, on affiche la boite de dialogue
                pygame.mixer.music.fadeout(10)
                deadTheme.play()
                again = dead_menu(
                    screen, player, background, walls_pits, AI_group,
                    bullets_group, all_dead_AI, all_spawners,
                    all_dead_spawners, all_spawned_AI)
                if again:  # on veut recommencer
                    return main(n, custom, True, from_selection)
                else:
                    try:
                        deadTheme.fadeout(200)
                        return False
                    except:
                        return False

        else:  # on attend que le player clique
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clickSound.play()
                    has_begun = True
                elif event.type == pygame.QUIT:
                    pygame.mixer.music.fadeout(200)
                    clock.tick(5)
                    pygame.quit()
                    return False
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_ESCAPE):
                    end = pause(
                        screen, player, background, walls_pits, AI_group,
                        bullets_group, all_dead_AI, all_spawners,
                        all_dead_spawners, all_spawned_AI)
                    if end:
                        pygame.mixer.music.fadeout(200)
                        clock.tick(5)
                        RUNNING = 0  # on retourne au menu
                        return False
            screen.blit(background.image, (0, 0))
            cible = pygame.mouse.get_pos()
            player.canon.update(player.body.rect.center, cible)
            screen.blit(player.body.image, player.body.rect)
            screen.blit(player.canon.image, player.canon.rect)
            for IA in AI_group:
                screen.blit(IA.body.image, IA.body.rect)
                screen.blit(IA.canon.image, IA.canon.rect)
            for spawner in all_spawners:
                screen.blit(spawner.image, spawner.rect)
            for x in walls_pits:
                screen.blit(x.image, x.rect)
            if (n == 1 or n == 2) and not custom:
                screen.blit(help_msg1, msgpos1)
                screen.blit(help_msg2, msgpos2)
            screen.blit(begin_msg, begin_msg_rect)
            curseur.update()
            pygame.display.flip()
