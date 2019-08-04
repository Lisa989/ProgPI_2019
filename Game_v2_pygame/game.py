#!/usr/bin/python
# -*- coding: utf-8 -*-

from json import load

import pygame
import sys

from Game_v2_pygame.Sprite.game_ball import Ball
from Game_v2_pygame.Sprite.game_brick import BrickSimple, BrickDouble, BrickImmortal
from Game_v2_pygame.Sprite.game_button import Button
from Game_v2_pygame.Sprite.game_paddle import Paddle
from Game_v2_pygame.game_risorse import Immagini, MyFont
from Game_v2_pygame.window import Window
from costanti.color import *
from costanti.game_v2_pygame_costanti import *

# stati di gioco
MENU_START = 0
PAUSE = 1
RUNNING = 2
GAME_OVER = 3
GAME_WIN = 4
LIST_LEVELS = 5
INSTRUCTIONS = 6


class Game(Window):
    def __init__(self, width, height):
        """
        Main application class. (Window)
        :param width: larghezza finestra
        :param height: altezza finestra
        """
        Window.__init__(self, width, height, "Arkanoid")
        # strutture di gioco
        self.__paddle = None
        self.__ball = None
        self.__bricks = None

        # liste dei bottoni delle varie schernate
        self.__button_list_menu_start = None
        self.__button_list_pause = None
        self.__button_list_game_over_win = None
        self.__button_list_levels = None
        self.__button_list_instruction = None

        # variabili necessarie per il gioco
        self.__brick_count = 0
        self.__prev_input_x = 0
        self.__save_change_ball = (0, 0)
        self.__level_number = 0
        self.__current_state = None
        self.__player = None

        self.__all_sprites_list = None

    def setup(self):
        """
            Inizializza Game
        """
        # Carica Font e Immagini
        MyFont.init_font()
        Immagini.load_img()

        self.backgroundImage = Immagini.background

        self.set_mouse_visible(True)
        self.set_background_color(AMAZON)

        # crea liste bottoni e le inizializza
        self.__set_button_menu_start()
        self.__set_button_menu_pause()
        self.__set_button_menu_game_over_win()
        self.__set_button_menu_levels()
        self.__set_button_menu_instructions()

        # crea paddle e ball
        self.__paddle = Paddle()
        self.__ball = Ball()

        # setta lo stato corrente al menu iniziale
        self.__set_state_menu_start()

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--LIVELLI--***************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_menu_levels(self):
        """
        Inizializza bottoni del menu scelta LIVELLI
        :return:
        """
        self.__button_list_levels = []
        row = 2
        column = 0
        if DEBUG:
            print("num_livelli: " + str(MAX_LEVEL))
        for i in range(1, MAX_LEVEL + 1):
            self.__button_list_levels.append(Button(row, column, "Livello " + str(i), self.__select_level, bt_id=i))
            column += 1
            if column == 3:
                column = 0
                row += 1
        self.__button_list_levels.append(Button(9, 1, "BACK", self.__set_state_menu_start))

    def __set_state_list_levels(self):
        """
        Imposta lo stato corrente a LIST_LEVELS
        :return:
        """
        self.__current_state = LIST_LEVELS

    def __select_level(self, livello):
        """
        Seleziona il livello scelto come livello di partenza
        :param livello:
        :return:
        """
        self.set_mouse_visible(False)
        self.__current_state = RUNNING
        self.__player = dict(life=3, score=0)
        self.__level_number = livello - 1
        self.__load_next_level()

    def __draw_menu_list_levels(self):
        """
        Disegna il menu scelta livello
        :return:
        """
        self.text_to_screen(txt="LIVELLI", font=MyFont.font60, riga=1, align="center", colore=WHITE)
        for bt in self.__button_list_levels:
            bt.draw(self.screen)

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--ISTRUZIONI--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_menu_instructions(self):
        """
        Inizializza bottoni menu ISTRUZIONI
        :return:
        """
        self.__button_list_instruction = []
        self.__button_list_instruction.append(Button(9, 1, "BACK", self.__set_state_menu_start))

    def __set_state_instructions(self):
        """
        Imposta stato corrente a INSTRUCTIONS
        :return:
        """
        self.__current_state = INSTRUCTIONS

    def __draw_menu_instructions(self):
        """
        Disegna menu INSTRUCTIONS
        :return:
        """
        # bottone indietro
        self.__button_list_instruction[0].draw(self.screen)

        # set_state_istruzioni
        # text_to_screen(txt, font, riga, align, colore)
        self.text_to_screen("Comandi:", MyFont.font40, 1, "center", WHITE)
        self.text_to_screen("P: pausa:", MyFont.font30, 2, "center", WHITE)
        self.text_to_screen("↑: lancia la pallina", MyFont.font30, 3, "center", WHITE)
        self.text_to_screen("←/→: muovi il paddle", MyFont.font30, 4, "center", WHITE)

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--MENU--*****************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_menu_start(self):
        """
        Inizializza i bottoni del menu start
        :return:
        """
        # Button (riga, colonna, txt, function, id=0)
        self.__button_list_menu_start = []
        self.__button_list_menu_start.append(Button(2, 1, "START", self.__start_game))
        self.__button_list_menu_start.append(Button(3, 1, "LIVELLI", self.__set_state_list_levels))
        self.__button_list_menu_start.append(Button(4, 1, "ISTRUZIONI", self.__set_state_instructions))
        self.__button_list_menu_start.append(Button(5, 1, "EXIT", sys.exit))

    def __set_button_menu_game_over_win(self):
        """
        Inizializza i bottoni del menu GAME_OVER/GAME_WIN
        :return:
        """
        self.__button_list_game_over_win = []
        self.__button_list_game_over_win.append(Button(3, 1, "RESTART", self.__start_game))
        self.__button_list_game_over_win.append(Button(4, 1, "MENU", self.__set_state_menu_start))

    def __draw_menu(self, menu, buttons):
        """
        Disegna il menu principale
        :param menu:
        :param buttons:
        return:
        """
        # text_to_screen(txt, font, riga, align, colore)
        self.text_to_screen(menu, MyFont.font60, 1, "center", WHITE)

        # Draw the buttons
        for bt in buttons:
            bt.draw(self.screen)

    def __set_state_menu_start(self):
        """
        Imposta lo stato corrente a MENU_START
        :return:
        """
        self.__current_state = MENU_START
        self.backgroundImage = Immagini.background

    """
    --------------------------------------------------------------------------------------------------------------------
    ********************************************--PAUSE--**************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_menu_pause(self):
        """
        Inizializza i bottoni del munu PAUSE
        :return:
        """
        # bottoni menu pause
        self.__button_list_pause = []
        self.__button_list_pause.append(Button(3, 1, "RIPRENDI", self.__exit_menu_pause))
        self.__button_list_pause.append(Button(4, 1, "RESTART", self.__start_game))
        self.__button_list_pause.append(Button(5, 1, "MENU", self.__set_state_menu_start))

    def __draw_menu_pause(self):
        """
        Disegna il menu PAUSE
        :return:
        """
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        s.fill(ALPHA_BLACK)
        self.screen.blit(s, (0, 0))
        self.__draw_menu("PAUSE", self.__button_list_pause)

    def __exit_menu_pause(self):
        """
        Esci dal menu PAUSE e reimposta lo stato RUNNING
        :return:
        """
        self.set_mouse_visible(False)
        self.__ball.change_x, self.__ball.change_y = self.__save_change_ball
        self.__current_state = RUNNING

    def __set_menu_pause(self):
        """
        Imposta lo stato corrente a PAUSE
        :return:
        """
        self.set_mouse_visible(True)
        self.__save_change_ball = self.__ball.change_x, self.__ball.change_y
        self.__ball.change_x, self.__ball.change_y = 0, 0
        self.__current_state = PAUSE

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--RUNNING--**************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __draw_state_running(self):
        """
        Disegna il livello di gioco
        :return:
        """
        # text_to_screen(txt, font, riga, align, colore)

        # disegna numero livello, vite, punteggio
        txt = "LIVELLO " + str(self.__level_number)
        self.text_to_screen(txt, MyFont.font60, 1, "left", BLACK)
        self.text_to_screen("LIFES", MyFont.font50, 2, "left", BLACK)

        cx, cy = get_row_column_center(row=3, align='life')
        for i in range(0, self.__player['life']):
            x, y = cx + (NEXT_ROW * i) - LIFE_SIZE, cy - LIFE_SIZE / 2
            self.screen.blit(Immagini.img_life, (x, y))

        self.text_to_screen("SCORE", MyFont.font50, 4, "left", BLACK)
        self.text_to_screen(str(self.__player['score']), MyFont.font40, 5, "left", BLACK)

        # disegna ball, brick e paddle
        self.__all_sprites_list.draw(self.screen)

    def __update_state_running(self):
        """
        Aggiorna stato di gioco
        :return:
        """
        # verifica collisioni
        self.__check_collision()

        # aggiorna spostamenti ball e paddle
        self.__ball.update()
        self.__paddle.update()

        # se la palla è ancorata al paddle la disegna sulla x corrispondente al paddle
        if self.__ball.ancorata:
            self.__ball.rect.x = self.__paddle.rect.x + (self.__paddle.rect.width / 2 - self.__ball.rect.width / 2)

        # se il numero di brick è 0, passa al prossimo livello
        if self.__brick_count == 0:
            self.__ball.stop()
            self.__load_next_level()

    def __start_game(self):
        """
        Inizia una nuova partita
        :return:
        """
        if DEBUG:
            print("start game")
        self.set_mouse_visible(False)
        self.__current_state = RUNNING
        self.__player = dict(life=3, score=0)
        self.__level_number = 0
        self.__load_next_level()

    def __load_next_level(self):
        """
        Carica il prossimo livello
        :return:
        """
        self.__level_number += 1
        if DEBUG:
            print("new level, num: " + str(self.__level_number))
        self.__paddle.restart_paddle()
        self.__ball.stop()

        # se ho finito i livelli chiama il game over, altrimenti cariac il livello
        if self.__level_number <= MAX_LEVEL:
            self.__brick_count = self.__load_level(get_level_name(self.__level_number))
        else:
            self.__game_over()

    def __game_over(self):
        """
        Il gioco è terminato o hai perso
        :return:
        """
        self.set_mouse_visible(True)

        # se i livelli sono terminati imposta lo stato corrente a GAME_WIN,
        # altrimenti hai terminato le vite e imposta lo stato corrente a GAME_OVER
        if self.__level_number > MAX_LEVEL:
            if DEBUG:
                print('non ci sono altri livelli')
            self.__current_state = GAME_WIN
        else:
            if DEBUG:
                print("GAME OVER")
            self.__current_state = GAME_OVER

    def __check_collision(self):
        """
        Verifica le collisioni
        :return:
        """
        # ball vs paddle
        # calcola change_x a seconda dell'angolo
        if pygame.sprite.collide_rect(self.__paddle, self.__ball):
            if DEBUG:
                print(
                    "brick paddle prima", "(dx,dy): (", self.__ball.change_x, ",", self.__ball.change_y, "), (x,Y): (",
                    self.__ball.rect.x, ",", self.__ball.rect.y, ")")
            dx = limit_delta((self.__ball.center_x - self.__paddle.center_x) / self.__paddle.rect.width)
            self.__ball.change_y *= -1
            self.__ball.change_x = dx
            if self.__ball.center_y >= AREA_PADDLE_BOTTOM:
                self.__ball.update_xy(self.__ball.rect.x, self.__ball.start_y)
            if DEBUG:
                print("brick paddle dopo", "(dx,dy): (", self.__ball.change_x, ",", self.__ball.change_y,
                      "), (x,Y): (", self.__ball.rect.x, ",", self.__ball.rect.y, ")")

        # ball vs fondo schermo
        if self.__ball.bottom >= SCREEN_LEVEL_BOTTOM:
            self.__ball.stop()
            self.__player['life'] -= 1
            if DEBUG:
                print('life lost, n:life: ', self.__player['life'])

            # se ho finito le vite chiamo il game over
            if self.__player['life'] == 0:
                self.__game_over()

        # ball vs brick
        brks_hit = pygame.sprite.spritecollide(self.__ball, self.__bricks, False)

        # for brick in brks_hit:
        if not len(brks_hit) == 0:
            brick = brks_hit[0]
            # calcola il cambio di direzione e lo limita
            dx = limit_delta((self.__ball.center_x - brick.center_x) / brick.rect.width)
            dy = limit_delta((self.__ball.center_y - brick.center_y) / brick.rect.height)

            if DEBUG:
                print("brick colpito")
                print("ball prima", "(dx,dy): (", self.__ball.change_x, ",", self.__ball.change_y,
                      "), (x,Y): (", self.__ball.rect.x, ",", self.__ball.rect.y, ")")

            points = brick.on_collide()
            self.__player['score'] += points
            if brick.dead:
                brick.kill()
                self.__brick_count -= 1

            # x = self.__ball.rect.x
            # y = self.__ball.rect.y

            # se il brick è stato colpito dall'alto
            if self.__ball.top <= brick.top <= self.__ball.bottom:
                self.__ball.change_y = dy
                # y = brick.top - (BALL_RADIUS * 2) - 1
            # se il brick è stato colpito dal basso
            elif brick.top <= self.__ball.top <= self.__ball.bottom:
                self.__ball.change_y = dy
                # y = brick.bottom + 1
            # se il brick è stato colpito a sinistra
            if self.__ball.left <= brick.left <= self.__ball.right:
                self.__ball.change_x = dx
                # x = brick.left - (BALL_RADIUS * 2) - 1
            # se il brick è stato colpito a destra
            elif self.__ball.left <= brick.right <= self.__ball.right:
                self.__ball.change_x = dx
                # x = brick.right + 1

            # self.__ball.update_xy(x, y)

            if DEBUG:
                print("ball dopo", "(dx,dy): (", self.__ball.change_x, ",", self.__ball.change_y,
                      "), (x,Y): (", self.__ball.rect.x, ",", self.__ball.rect.y, ")")

    def __handler_key_press_running(self, key):
        # inizia a spostare il paddle
        if key == pygame.K_LEFT:
            if self.__paddle.change_x != 0:
                self.__prev_input_x = 1
            self.__paddle.change_x = -1

        elif key == pygame.K_RIGHT:
            if self.__paddle.change_x != 0:
                self.__prev_input_x = -1
            self.__paddle.change_x = 1

    def __handler_key_release_running(self, key):
        # ferma il puddle
        if key == pygame.K_LEFT:
            if self.__prev_input_x < 0:
                self.__prev_input_x = 0
            elif self.__prev_input_x > 0:
                self.__paddle.change_x = 1
                self.__prev_input_x = 0
            else:
                self.__paddle.change_x = 0
        elif key == pygame.K_RIGHT:
            if self.__prev_input_x > 0:
                self.__prev_input_x = 0
            elif self.__prev_input_x < 0:
                self.__paddle.change_x = -1
                self.__prev_input_x = 0
            else:
                self.__paddle.change_x = 0

        # lancia la pallina da tastiera
        # key up e down invertiti in pygame
        elif not key == pygame.K_DOWN:
            if self.__ball.ancorata:
                self.__ball.start()

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--LOAD LEVEL--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    @staticmethod
    def __get_pos_on_screen(row, column):
        """
        Calcola x, y dove disegnare il brick
        :param row: riga
        :param column: colonna
        :return: x, y sullo schermo
        """
        x_screen = SCREEN_LEVEL_LEFT + BRICK_WIDTH * column
        y_screen = SCREEN_LEVEL_TOP + BRICK_HEIGHT * row
        return x_screen, y_screen

    def __load_level(self, level):
        """
        Carica livello da file
        :param level: nome del livello
        :return: numero dei brick nel livello
        """
        brick_n = 0
        filename = resource_path(LEVEL_DIR + level)
        if filename:
            with open(filename) as data_file:
                data = load(data_file)
                data_file.close()

            self.__all_sprites_list = pygame.sprite.Group()
            self.__bricks = pygame.sprite.Group()
            self.__all_sprites_list.add(self.__paddle)
            self.__all_sprites_list.add(self.__ball)

            for p in range(0, MAX_ROW * MAX_CLN):
                if data[p] is not None:
                    x, y = self.__get_pos_on_screen(data[p]["row"], data[p]["cln"])
                    tp = data[p]["type"]
                    if tp == ID_SIMPLE:
                        brk = BrickSimple(x, y, data[p]["color"])
                        brick_n += 1
                    elif tp == ID_DOUBLE:
                        brk = BrickDouble(x, y, data[p]["color"])
                        brick_n += 1
                    elif tp == ID_IMMORTAL:
                        brk = BrickImmortal(x, y)
                    else:
                        brk = None
                    self.__bricks.add(brk)
                    self.__all_sprites_list.add(brk)
            if DEBUG:
                print(self.__bricks)

            self.backgroundImage = Immagini.backgrounds[self.__level_number % len(Immagini.backgrounds)]
        else:
            self.__current_state = MENU_START
            if DEBUG:
                print("file " + filename + " non trovato")
            return 0

        return brick_n

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--GAME--*****************************************************************
    *****************************************--OVERRIDE--***************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_draw(self):
        """
        Render the screen.
        """
        # cancalla ciò che è stato disegnato al frame precedente e resetta lo schermo al background_color
        self.start_render()

        # Draw the background texture
        self.screen.blit(self.backgroundImage, (SCREEN_LEVEL_LEFT, SCREEN_LEVEL_TOP))

        self.screen.blit(Immagini.img_edge_v, EDGE_RIGHT)
        self.screen.blit(Immagini.img_edge_v, EDGE_LEFT)
        self.screen.blit(Immagini.img_edge_h, EDGE_TOP)

        # disegna lo stato corrente
        if self.__current_state == MENU_START:
            self.__draw_menu("MENU", self.__button_list_menu_start)
        elif self.__current_state == RUNNING:
            self.__draw_state_running()
        elif self.__current_state == PAUSE:
            self.__draw_menu_pause()
        elif self.__current_state == GAME_OVER:
            self.__draw_menu("GAME OVER", self.__button_list_game_over_win)
        elif self.__current_state == GAME_WIN:
            self.__draw_menu("YOU WIN", self.__button_list_game_over_win)
        elif self.__current_state == INSTRUCTIONS:
            self.__draw_menu_instructions()
        elif self.__current_state == LIST_LEVELS:
            self.__draw_menu_list_levels()

    def on_update(self):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.__current_state == RUNNING:
            self.__update_state_running()

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    ***********************************************--INPUT--************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    # TASTIERA
    def on_key_press(self, key):
        """
        Gestione evento pygame.KEYDOWN
        :param key: tasto premuto
        :return:
        """
        # tasto premuto ESCAPE
        if key == pygame.K_ESCAPE:
            sys.exit(0)

        # Gestione tasti stato RUNNING
        if self.__current_state == RUNNING:
            self.__handler_key_press_running(key)

        # tasto premuto P, gestito a seconda dello stato
        if key == pygame.K_p:
            if self.__current_state == RUNNING:
                self.__set_menu_pause()
            elif self.__current_state == PAUSE:
                self.__exit_menu_pause()

    def on_key_release(self, key):
        """
        Gestione evento pygame.KEYUP
        :param key: tasto rilasciato
        :return:
        """
        if self.__current_state == RUNNING:
            self.__handler_key_release_running(key)

    # MOUSE
    def on_mouse_motion(self, x, y):
        """
        Gestione evento pygame.MOUSEMOTION
        :param x:
        :param y:
        :return:
        """
        pass

    def on_mouse_press(self, x, y, button):
        """
        Gestione evento pygame.MOUSEBUTTONDOWN
        :param x:
        :param y:
        :param button:
        :return:
        """
        # verifica se nella lista dei bottoni relativi allo stato corrente ce ne è uno premuto
        if self.__current_state == MENU_START:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_menu_start)
        if self.__current_state == PAUSE:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_pause)
        if self.__current_state == GAME_WIN or self.__current_state == GAME_OVER:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_game_over_win)
        if self.__current_state == INSTRUCTIONS:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_instruction)
        if self.__current_state == LIST_LEVELS:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_levels)

    def on_mouse_release(self, x, y, button):
        """
        Gestione evento pygame.MOUSEBUTTONUP
        :param x:
        :param y:
        :param button:
        :return:
        """
        # verifica se nella lista dei bottoni relativi allo stato corrente ce ne è uno rilasciato
        if self.__current_state == MENU_START:
            Button.check_mouse_release_for_buttons(x, y, self.__button_list_menu_start)
            for bt in self.__button_list_menu_start:
                bt.pressed = False
        elif self.__current_state == PAUSE:
            Button.check_mouse_release_for_buttons(x, y, self.__button_list_pause)
            for bt in self.__button_list_pause:
                bt.pressed = False
        elif self.__current_state == GAME_WIN or self.__current_state == GAME_OVER:
            Button.check_mouse_release_for_buttons(x, y, self.__button_list_game_over_win)
            for bt in self.__button_list_game_over_win:
                bt.pressed = False
        elif self.__current_state == INSTRUCTIONS:
            Button.check_mouse_release_for_buttons(x, y, self.__button_list_instruction)
            for bt in self.__button_list_instruction:
                bt.pressed = False
        elif self.__current_state == LIST_LEVELS:
            Button.check_mouse_release_for_buttons(x, y, self.__button_list_levels)
            for bt in self.__button_list_levels:
                bt.pressed = False
