import arcade
from costanti.game_v1_arcade_costanti import Costanti
from Game_v1_arcade.game_risorse import Immagini


class TextButton:
    """
    Text-based button
    """

    def __init__(self, center_x, center_y, width, height, text, action_function, bt_id,
                 font_size=18, font_face="Arial", button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text

        self.bt_id = bt_id

        self.action_function = action_function

        self.button = Immagini.img_button_yellow
        self.button_press = Immagini.img_button_orange

        self.font_size = font_size
        self.font_face = font_face

        self.pressed = False

        self.button_height = button_height

    def draw(self):
        """
        Disegna il bottone e il suo testo
        :return:
        """
        if not self.pressed:
            img = self.button
        else:
            img = self.button_press

        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, img)

        # disegna testo
        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y, arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center", anchor_x="center", anchor_y="center")

    def on_press(self):
        """
        Seleziona bottone premuto
        :return:
        """
        self.pressed = True

    def on_release(self):
        """
        Seleziona bottone rilasciato ed esegui la funzione associata
        :return:
        """
        self.pressed = False
        if self.bt_id == 0:
            self.action_function()
        else:
            self.action_function(self.bt_id)

    def on_scale(self, scale):
        """
        Scala le dimensioni il caso di cambio modalità fullscreen
        :param scale:
        :return:
        """
        self.center_x *= scale
        self.center_y *= scale
        self.width = Costanti.Button_WIDTH
        self.height = Costanti.Button_HEIGHT


class Button(TextButton):
    """
    TextButton Button
    """
    def __init__(self, row, column, text, action_function, bt_id=0):
        """
        Crea un TextButton alle coordinate calcolate secondo row e column
        :param row: riga dello schermo
        :param column: colonna dello schermo
        :param text: testo del bottone
        :param action_function: funzione associata
        :param bt_id: id del bottone
        """
        center_x, center_y = Costanti.get_row_column_center(row, column)
        super().__init__(center_x, center_y, Costanti.Button_WIDTH, Costanti.Button_HEIGHT, text, action_function, bt_id)

    # test click bottone
    @staticmethod
    def check_mouse_press_for_buttons(x, y, button_list):
        """ Given an x, y, see if we need to register any button clicks. """
        for button in button_list:
            if x > button.center_x + button.width / 2:
                continue
            if x < button.center_x - button.width / 2:
                continue
            if y > button.center_y + button.height / 2:
                continue
            if y < button.center_y - button.height / 2:
                continue
            button.on_press()

    @staticmethod
    def check_mouse_release_for_buttons(button_list):
        """ If a mouse button has been released, see if we need to process
            any release events. """
        for button in button_list:
            if button.pressed:
                button.on_release()
