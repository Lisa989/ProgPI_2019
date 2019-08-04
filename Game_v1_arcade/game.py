from Game_v1_arcade.Sprite.game_brick import BrickSimple, BrickDouble, BrickImmortal
from Game_v1_arcade.Sprite.game_paddle import Paddle
from Game_v1_arcade.Sprite.game_ball import Ball
from Game_v1_arcade.Sprite.game_button import Button

from Game_v1_arcade.game_risorse import Immagini
from costanti.game_v1_arcade_costanti import *

from json import load
import arcade
import sys

# stati di gioco
MENU = 0
PAUSE = 1
RUNNING = 2
GAME_OVER = 3
GAME_WIN = 4
LEVELS = 5
INSTRUCTION = 6


class Game(arcade.Window):
    def __init__(self, width, height):
        """
        Main application class.
        :param width: larghrzza finestra not fullscreen
        :param height: altezza finetra not fullscreen
        """
        super().__init__(width, height, "Arkanoid", fullscreen=True)

        # strutture di gioco
        self.__paddle = None
        self.__ball = None
        self.__bricks = None

        # liste dei bottoni dei vari stati
        self.__button_list_menu_start = None
        self.__button_list_pause = None
        self.__button_list_game_over = None
        self.__button_list_levels = None
        self.__button_list_instruction = None

        # variabili necessarie al gioco
        self.__brick_count = 0
        self.__prev_input_x = 0
        self.__save_change_ball = (0, 0)
        self.__level_number = 0
        self.__current_state = None
        self.__player = None

    def setup(self):
        """
            Inizializza Game
        """
        # inizializza le costanti carica le risorse
        Costanti.init()
        Immagini.load_img()

        self.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.AMAZON)

        # crea liste bottoni e le inizializza
        self.__set_button_menu_start()
        self.__set_button_munu_pause()
        self.__set_button_menu_game_over_win()
        self.__set_button_menu_livelli()
        self.__set_button_menu_instruction()

        # crea paddle e ball
        self.__paddle = Paddle()
        self.__ball = Ball(self.__paddle.center_x, self.__paddle.center_y + self.__paddle.height / 2)

        # se il gioco non inizia in fullscreen ricalcola le costanti
        if not self.fullscreen:
            self.__resize()

        # setta lo stato corrente al menu iniziale
        self.__set_menu_start()

    @staticmethod
    def __draw_text(text, row, pt, color, align='center'):
        """
        Funzione per disegnare testo che calcola la posizione data la riga
        :param text: testo da disegnare
        :param row: riga in cui disegnare
        :param pt: dimensione testo
        :param color: colore
        :param align: dove disengare il testo
        """
        x, y = Costanti.get_row_column_center(row, align=align)
        arcade.draw_text(text, x, y, color, pt, align="center", anchor_x="center", anchor_y="center")

    def __resize(self):
        """
        Calcola le costanti e le dimensioni delle sprite a seconda delle dimensioni dello schermo
        """
        Costanti.on_scale(self.fullscreen)

        if self.fullscreen:
            scale = Costanti.to_full_screen
        else:
            scale = Costanti.to_not_full_screen

        self.__paddle.on_scale(scale)
        self.__ball.on_scale(scale)

        if self.__bricks is not None:
            for b in self.__bricks:
                b.on_scale(scale)

        for bt in self.__button_list_menu_start:
            bt.on_scale(scale)

        for bt in self.__button_list_pause:
            bt.on_scale(scale)

        for bt in self.__button_list_game_over:
            bt.on_scale(scale)

        for bt in self.__button_list_levels:
            bt.on_scale(scale)

        for bt in self.__button_list_instruction:
            bt.on_scale(scale)

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--LIVELLI--***************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_menu_livelli(self):
        """
        Inizializza i bottoni del menu scelta livelli
        :return:
        """
        self.__button_list_levels = []
        # bottoni menu selezione livello
        row = 1
        column = 0
        if DEBUG:
            print("num_livelli: "+str(Costanti.MAX_LEVEL))
        for i in range(1, Costanti.MAX_LEVEL + 1):
            self.__button_list_levels.append(Button(row, column, "Livello " + str(i), self.__imposta_livello_scelto, bt_id=i))
            column += 1
            if column == 3:
                column = 0
                row += 1
        self.__button_list_levels.append(Button(9, 0, "BACK", self.__set_menu_start))

    def __set_state_elenco_livelli(self):
        """
        Setta lo stato corrente a l'elenco dei livalli
        :return:
        """
        self.__current_state = LEVELS

    def __imposta_livello_scelto(self, livello):
        """
        Setta il livello che si vuole giocare come livello di partenza
        :param livello: livello da disegnare
        :return:
        """
        self.set_mouse_visible(False)
        self.__current_state = RUNNING
        self.__player = dict(life=3, score=0)
        self.__level_number = livello - 1
        self.__new_level()

    def __draw_menu_scelta_livello(self):
        """
        Disegna il menu scelta livello
        :return:
        """
        self.__draw_text("LIVELLI", 0, Costanti.PT_FONT['title'], arcade.color.WHITE)
        for bt in self.__button_list_levels:
            bt.draw()

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--ISTRUZIONI--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_menu_instruction(self):
        """
        Inizializza i bottoni del menu istruzioni
        :return:
        """
        self.__button_list_instruction = []
        # bottone back menu set_state_istruzioni
        self.__button_list_instruction.append(Button(9, 1, "BACK", self.__set_menu_start))

    def __set_state_istruzioni(self):
        """
        Setta lo stato corrente a menu istruzioni
        :return:
        """
        self.__current_state = INSTRUCTION

    def __draw_menu_istruction(self):
        # bottone indietro
        self.__button_list_instruction[0].draw()

        # istruzioni
        self.__draw_text("Comandi:", 1, Costanti.PT_FONT['text'], arcade.color.WHITE)
        self.__draw_text("F: fullscreen", 2, Costanti.PT_FONT['text2'], arcade.color.WHITE)
        self.__draw_text("P: pausa", 3, Costanti.PT_FONT['text2'], arcade.color.WHITE)
        self.__draw_text("↑: lancia la pallina", 4, Costanti.PT_FONT['text2'], arcade.color.WHITE)
        self.__draw_text("←/→: muovi il paddle", 5, Costanti.PT_FONT['text2'], arcade.color.WHITE)

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
        # bottoni menu start
        self.__button_list_menu_start = []
        self.__button_list_menu_start.append(Button(2, 1, "START", self.__start_game))
        self.__button_list_menu_start.append(Button(3, 1, "LIVELLI", self.__set_state_elenco_livelli))
        self.__button_list_menu_start.append(Button(4, 1, "ISTRUZIONI", self.__set_state_istruzioni))
        self.__button_list_menu_start.append(Button(5, 1, "EXIT", sys.exit))

    def __set_button_menu_game_over_win(self):
        """
        Inizializza i bottoni del menu game over/win
        :return:
        """
        self.__button_list_game_over = []
        # bottoni menu game_over/win
        self.__button_list_game_over.append(Button(3, 0, "RESTART", self.__start_game))
        self.__button_list_game_over.append(Button(4, 0, "MENU", self.__set_menu_start))

    def __draw_menu(self, menu, buttons):
        """
        Disegna un menu
        :param menu: menu da disegnare (Stringa titolo)
        :param buttons: (lista dei bottoni)
        :return:
        """
        # draw MENU
        self.__draw_text(menu, 1, Costanti.PT_FONT['title'], arcade.color.WHITE)

        # Draw the buttons
        for bt in buttons:
            bt.draw()

    def __set_menu_start(self):
        """
        Setta lo stato al menu principale
        :return:
        """
        self.__current_state = MENU

    """
    --------------------------------------------------------------------------------------------------------------------
    ********************************************--PAUSE--**************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def __set_button_munu_pause(self):
        """
        Inizializza i bottoni del menu pause
        :return:
        """
        # bottoni menu pause
        self.__button_list_pause = []
        self.__button_list_pause.append(Button(3, 1, "RIPRENDI", self.__exit_pause))
        self.__button_list_pause.append(Button(4, 1, "RESTART", self.__start_game))
        self.__button_list_pause.append(Button(5, 1, "MENU", self.__set_menu_start))

    def __draw_menu_pause(self):
        """
        Disegna il menu pause
        :return:
        """
        width, height = self.get_size()
        arcade.draw_rectangle_filled(width / 2, height / 2, width, height,
                                     arcade.make_transparent_color(arcade.color.BLACK, 100))
        self.__draw_menu("PAUSE", self.__button_list_pause)

    def __exit_pause(self):
        """
        Reimposta le i movimenti di ball e setta lo stato corrente a RUNNING
        :return:
        """
        self.set_mouse_visible(False)
        self.__ball.change_x, self.__ball.change_y = self.__save_change_ball
        self.__current_state = RUNNING

    def __set_menu_pause(self):
        """
        Azzera i movimenti di ball e setta lo stato PAUSE
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
        DIsegna lo stato RUNNING
        :return:
        """
        # disenga numero livello, vite, e punteggio
        txt = "LIVELLO " + str(self.__level_number)
        self.__draw_text(txt, 1, Costanti.PT_FONT['title'], arcade.color.BLACK, align='left')
        self.__draw_text("LIFES", 2, Costanti.PT_FONT['title2'], arcade.color.BLACK, align='left')

        x, y = Costanti.get_row_column_center(row=3, align='life')
        ball_size = Costanti.BALL_LIFE_SIZE
        for i in range(0, self.__player['life']):
            arcade.draw_texture_rectangle(x + ((Costanti.NEXT_ROW / 2) * i), y, ball_size, ball_size, Immagini.img_ball)

        self.__draw_text("SCORE", 4, Costanti.PT_FONT['title2'], arcade.color.BLACK, align='left')
        self.__draw_text(str(self.__player['score']), 5, Costanti.PT_FONT['text'], arcade.color.BLACK, align='left')

        # disegna ball, paddle e brick
        self.__ball.draw()
        self.__paddle.draw()
        self.__bricks.draw()

    def __update_state_running(self):
        """
        Aggiorna il gioco
        :return:
        """
        # verifica le collisioni
        self.__check_collision()

        # aggiorna i movimenti di ball e paddle
        self.__ball.update()
        self.__paddle.update()

        # se la palla è ancorata al paddle, disegna la palla al centro del paddle
        if self.__ball.ancorata:
            self.__ball.center_x = self.__paddle.center_x

        # se i brick sono 0, ferma la palla e inizializza un nuovo livello
        if self.__brick_count == 0:
            self.__ball.stop()
            self.__new_level()

    def __restart_paddle(self):
        """
        riporta il paddle alle coordinate iniziali
        :return:
        """
        self.__paddle.change_x = 0
        self.__paddle.center_x = Costanti.LEVEL_INFO['width']

    def __start_game(self):
        """
        Inizializza una nuova partita
        :return:
        """
        if DEBUG:
            print("start game")
        self.set_mouse_visible(False)
        self.__current_state = RUNNING
        self.__player = dict(life=3, score=0)
        self.__level_number = 0
        self.__new_level()

    def __new_level(self):
        """
        Inizializza un nuovo livello
        :return:
        """
        self.__level_number += 1
        if DEBUG:
            print("new level, num: " + str(self.__level_number))
        self.__restart_paddle()
        self.__ball.stop()

        # verifica che ci siano ancora livelli disponibili
        if self.__level_number <= Costanti.MAX_LEVEL:
            self.__brick_count = self.__load_level(get_level_name(self.__level_number))
        else:
            self.__game_over()

    def __game_over(self):
        """
        Gioco terminato: WIN se i livelli sono terminati, LOST se le vite sono finite
        :return:
        """
        self.set_mouse_visible(True)

        if self.__level_number > Costanti.MAX_LEVEL:
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
        if arcade.check_for_collision(self.__paddle, self.__ball):
            # cambia direzione x, y
            # se la palla è sotto il bottom, setta la y di ball sopra
            self.__ball.change_y *= -1
            self.__ball.change_x = (self.__ball.center_x - self.__paddle.center_x) / self.__paddle.width
            if self.__ball.center_y <= Costanti.LEVEL_INFO['bottom']:
                self.__ball.center_y = Costanti.LEVEL_INFO['bottom'] + Costanti.Ball_RADIUS + 1

        # ball vs fine schermo
        if self.__ball.bottom < 0:
            # ferma la palla, scala una vita, se non ci sono più vite chiama game_over
            self.__ball.stop()
            self.__player['life'] -= 1
            if self.__player['life'] == 0:
                self.__game_over()

        # ball vs brick
        for brick in self.__bricks:
            if arcade.check_for_collision(self.__ball, brick):
                # aggiorna il punteggio, se il brick è dead lo rimuove e aggiorna brick_count
                self.__player['score'] += brick.on_collide()
                if brick.dead:
                    self.__bricks.remove(brick)
                    self.__brick_count -= 1

                # aggiusta le coordinate di ball a seconda di dove a colpito il brick
                if self.__ball.bottom - Costanti.Ball_RADIUS <= brick.top <= self.__ball.bottom + Costanti.Ball_RADIUS:
                    # il brick è stato colpito da sopra
                    self.__ball.change_y = (self.__ball.center_y - brick.center_y) / brick.height
                    self.__ball.bottom = brick.top
                elif self.__ball.top - Costanti.Ball_RADIUS <= brick.bottom <= self.__ball.top + Costanti.Ball_RADIUS:
                    # il brick è stato colpito da sotto
                    self.__ball.change_y = (self.__ball.center_y - brick.center_y) / brick.height
                    self.__ball.top = brick.bottom

                if self.__ball.right - Costanti.Ball_RADIUS <= brick.left <= self.__ball.right + Costanti.Ball_RADIUS:
                    # il brick è stato colpito a sinistra
                    self.__ball.change_x = (self.__ball.center_x - brick.center_x) / brick.width
                    self.__ball.right = brick.left
                elif self.__ball.left - Costanti.Ball_RADIUS <= brick.right <= self.__ball.left + Costanti.Ball_RADIUS:
                    # il brick è stato colpito a destra
                    self.__ball.change_x = (self.__ball.center_x - brick.center_x) / brick.width
                    self.__ball.left = brick.right

    def __handler_key_press_running(self, key):
        """
        Gestione key_press in modalità RUNNING
        :param key: Tasto premuto
        :return:
        """
        # inizia a spostare il paddle
        if key == arcade.key.LEFT:
            if self.__paddle.change_x != 0:
                self.__prev_input_x = 1
            self.__paddle.change_x = -1

        elif key == arcade.key.RIGHT:
            if self.__paddle.change_x != 0:
                self.__prev_input_x = -1
            self.__paddle.change_x = 1

    def __handler_key_release_running(self, key):
        """
        Gestione key_release modalità RUNNING
        :param key: tasto rilasciato
        :return:
        """
        # ferma il puddle
        if key == arcade.key.LEFT:
            if self.__prev_input_x < 0:
                self.__prev_input_x = 0
            elif self.__prev_input_x > 0:
                self.__paddle.change_x = 1
                self.__prev_input_x = 0
            else:
                self.__paddle.change_x = 0
        elif key == arcade.key.RIGHT:
            if self.__prev_input_x > 0:
                self.__prev_input_x = 0
            elif self.__prev_input_x < 0:
                self.__paddle.change_x = -1
                self.__prev_input_x = 0
            else:
                self.__paddle.change_x = 0

        # lancia la pallina da tastiera
        if key == arcade.key.UP:
            if self.__ball.ancorata:
                self.__ball.start()

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--LOAD LEVEL--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    @staticmethod
    def __get_pos_on_screen(r, c):
        """
        Calcola x, y dove disegnare il brick
        :param r: riga
        :param c: colonna
        :return: x, y sullo schermo
        """
        x = Costanti.LEVEL_INFO['width'] // 2 + Costanti.Brick_WIDTH // 2 + 1
        y = Costanti.LEVEL_INFO['height'] - Costanti.Brick_HEIGHT // 2
        return x + Costanti.Brick_WIDTH * c, y - Costanti.Brick_HEIGHT * r

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

            self.__bricks = arcade.SpriteList()
            for p in range(0, MAX_ROW * MAX_CLN):
                if data[p] is not None:
                    x, y = self.__get_pos_on_screen(data[p]["row"], data[p]["cln"])
                    tp = data[p]["type"]
                    if tp == ID_SIMPLE:
                        self.__bricks.append(BrickSimple(x, y, data[p]["color"]))
                        brick_n += 1
                    elif tp == ID_DOUBLE:
                        self.__bricks.append(BrickDouble(x, y, data[p]["color"]))
                        brick_n += 1
                    elif tp == ID_IMMORTAL:
                        self.__bricks.append(BrickImmortal(x, y))
        else:
            self.__current_state = MENU
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
        # cancalla ciò che è stato disegnato al frame precedente e resetta lo schermo al arcade.set_background_color
        arcade.start_render()

        # Draw the background texture
        arcade.draw_texture_rectangle(Costanti.LEVEL_INFO['width'], Costanti.LEVEL_INFO['height'] // 2,
                                      Costanti.LEVEL_INFO['width'],
                                      Costanti.LEVEL_INFO['height'], Immagini.background)

        cx, cy, w, h = Costanti.EDGE_INFO['left']
        arcade.draw_texture_rectangle(cx, cy, w, h, Immagini.img_edge)
        cx, cy, w, h = Costanti.EDGE_INFO['right']
        arcade.draw_texture_rectangle(cx, cy, w, h, Immagini.img_edge)
        cx, cy, w, h = Costanti.EDGE_INFO['top']
        arcade.draw_texture_rectangle(cx, cy, h, w, Immagini.img_edge, 90)

        # disegna lo stato settato
        if self.__current_state == MENU:
            self.__draw_menu("MENU", self.__button_list_menu_start)
        elif self.__current_state == RUNNING:
            self.__draw_state_running()
        elif self.__current_state == PAUSE:
            self.__draw_menu_pause()
        elif self.__current_state == GAME_OVER:
            self.__draw_menu("GAME OVER", self.__button_list_game_over)
        elif self.__current_state == GAME_WIN:
            self.__draw_menu("YOU WIN", self.__button_list_game_over)
        elif self.__current_state == INSTRUCTION:
            self.__draw_menu_istruction()
        elif self.__current_state == LEVELS:
            self.__draw_menu_scelta_livello()

    def on_update(self, delta_time):
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
    def on_key_press(self, key, modifiers):
        """
        Gestione evento key_press
        :param key: tasto premuto
        :param modifiers:
        :return:
        """
        # tasto ESCAPE, chiudi il gioco
        if key == arcade.key.ESCAPE:
            sys.exit(0)

        # tasto F, esci/entra in modalità fullscreen
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)
            self.__resize()

        # gestione tasti modalità RUNNING
        if self.__current_state == RUNNING:
            self.__handler_key_press_running(key)

        # tasto P, entra esci PAUSE a seconda dello stato
        if key == arcade.key.P:
            if self.__current_state == RUNNING:
                self.__set_menu_pause()
            elif self.__current_state == PAUSE:
                self.__exit_pause()

    def on_key_release(self, key, key_modifiers):
        """
        Gestione evento key_release
        :param key: tasto rilasciato
        :param key_modifiers:
        :return:
        """
        if self.__current_state == RUNNING:
            self.__handler_key_release_running(key)

    # MOUSE
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Gestione evento mouse_motion
        :param x:
        :param y:
        :param dx:
        :param dy:
        :return:
        """
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Gestione evento premi tasto mouse
        :param x:
        :param y:
        :param button:
        :param modifiers:
        :return:
        """

        # a seconda dello stato verifica se un bottone nella lista è stato premuto
        if self.__current_state == MENU:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_menu_start)
        if self.__current_state == PAUSE:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_pause)
        if self.__current_state == GAME_WIN or self.__current_state == GAME_OVER:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_game_over)
        if self.__current_state == INSTRUCTION:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_instruction)
        if self.__current_state == LEVELS:
            Button.check_mouse_press_for_buttons(x, y, self.__button_list_levels)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Gestione evento rilascio tasto mouse
        :param x:
        :param y:
        :param button:
        :param modifiers:
        :return:
        """
        # a seconda dello stato verifica se un bottone della lista è stato rilasciato
        if self.__current_state == MENU:
            Button.check_mouse_release_for_buttons(self.__button_list_menu_start)
        if self.__current_state == PAUSE:
            Button.check_mouse_release_for_buttons(self.__button_list_pause)
        if self.__current_state == GAME_WIN or self.__current_state == GAME_OVER:
            Button.check_mouse_release_for_buttons(self.__button_list_game_over)
        if self.__current_state == INSTRUCTION:
            Button.check_mouse_release_for_buttons(self.__button_list_instruction)
        if self.__current_state == LEVELS:
            Button.check_mouse_release_for_buttons(self.__button_list_levels)
