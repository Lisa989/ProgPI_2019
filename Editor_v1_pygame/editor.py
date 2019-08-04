from Editor_v1_pygame.editor_risorse import *
from Editor_v1_pygame.editor_window import *
from Editor_v1_pygame.editor_toolbar import ToolBar
from Editor_v1_pygame.editor_brick import BrickImmortal, BrickDouble, BrickSimple
from tkinter.filedialog import askopenfilename, asksaveasfilename
from json import dump, load

options = {'defaultextension': '.json',
           'filetypes': [('Levels', '.json'), ('All files', '*')],
           'initialdir': 'levels',
           'initialfile': ''
           }

MODE_NONE = 0
MODE_PAINT = 1
MODE_DELETE = 2
MODE_MOVE = 3


class Editor(Window):
    def __init__(self, width, height, caption="Arkanoid Editor"):
        super().__init__(width, height, caption)
        self.brick_grid = None
        self.bricks = None

        self.toolbar = None
        self.current_mode = MODE_NONE

        self.type_selected = None
        self.color_selected = None

        self.drag_drop = None

    def setup(self):
        Costanti.init()
        Costanti.on_scale(False)  # editor non è in fullscreen
        Risorse.load()
        self.toolbar = ToolBar()
        self.bricks = []
        for p in range(0, MAX_CLN * MAX_ROW):
            self.bricks.append(None)

        self.brick_grid = dict(
            x=Costanti.LEVEL_INFO['width'] / 2,
            y=Costanti.EDGE_INFO['size'],
            width=Costanti.LEVEL_INFO['width'],
            height=Costanti.LEVEL_INFO['height'] - Costanti.LEVEL_INFO['paddle_area_height'],
            right=(Costanti.LEVEL_INFO['width'] / 2) + Costanti.LEVEL_INFO['width'],
            bottom=Costanti.EDGE_INFO['size'] + (
                    Costanti.LEVEL_INFO['height'] - Costanti.LEVEL_INFO['paddle_area_height'])
        )

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    ********************************************--UPDATE/DRAW--*********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_update(self):
        pass

    def on_draw(self):
        # background
        self.screen.fill((0, 0, 0))

        self.screen.blit(Risorse.background, (
            Costanti.get_point_to_draw(Costanti.LEVEL_INFO['width'], Costanti.LEVEL_INFO['height'] / 2,
                                       Costanti.LEVEL_INFO["width"], Costanti.LEVEL_INFO['height'])))

        x, y, w, h = Costanti.EDGE_INFO['top']
        self.screen.blit(Risorse.borderH, (Costanti.get_point_to_draw(x, y, w, h)))
        x, y, w, h = Costanti.EDGE_INFO['left']
        self.screen.blit(Risorse.borderV, (Costanti.get_point_to_draw(x, y, w, h)))
        x, y, w, h = Costanti.EDGE_INFO['right']
        self.screen.blit(Risorse.borderV, (Costanti.get_point_to_draw(x, y, w, h)))

        if self.is_on_grid(pygame.mouse.get_pos()):
            x, y = self.get_pos_brick(pygame.mouse.get_pos())
            pygame.draw.rect(self.screen, WHITE, (x, y, Costanti.Brick_WIDTH, Costanti.Brick_HEIGHT), 1)

        self.toolbar.draw(self.screen)

        for brk in self.bricks:
            if brk is not None:
                brk.draw(self.screen)

        if self.current_mode == MODE_MOVE:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x, y = (mouse_x - self.drag_drop['offset_x']), (mouse_y - self.drag_drop['offset_y'])
            self.drag_drop['brk'].draw_break_img(self.screen, x, y)

    """
    --------------------------------------------------------------------------------------------------------------------
    ******************************************--CALCOLO DELLE--*********************************************************
    ********************************************--POSIZIONI--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def is_on_grid(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.brick_grid['x'] < mouse_x < self.brick_grid['right'] \
            and self.brick_grid['y'] < mouse_y < self.brick_grid['bottom']

    def get_pos_on_screen(self, row, column):
        """
        :param row:
        :param column:
        :return: x, y della casella
        """
        x_screen = self.brick_grid['x'] + Costanti.Brick_WIDTH * column
        y_screen = self.brick_grid['y'] + Costanti.Brick_HEIGHT * row
        return x_screen, y_screen

    def get_pos_on_grid(self, mouse_pos):
        """
        :param mouse_pos:
        :return: row, columd della casella
        """
        mouse_x, mouse_y = mouse_pos
        x, y = mouse_x - self.brick_grid['x'], mouse_y - self.brick_grid['y']

        column = int(x // Costanti.Brick_WIDTH)
        row = int(y // Costanti.Brick_HEIGHT)

        return row, column

    def get_pos_brick(self, mouse_pos):
        """
        :param mouse_pos:
        :return: x, y della casella
        """
        row, column = self.get_pos_on_grid(mouse_pos)
        return self.get_pos_on_screen(row, column)

    @staticmethod
    def get_index_brick_position(row, column):
        """
        :param row:
        :param column:
        :return: indice dell'array
        """
        return row + column + (MAX_CLN - 1) * row

    def get_index_brick_mouse(self, mouse_pos):
        """
        :param mouse_pos:
        :return: indice dell'array
        """
        row, column = self.get_pos_on_grid(mouse_pos)
        return row + column + (MAX_CLN - 1) * row

    """
    --------------------------------------------------------------------------------------------------------------------
    **************************************************--EDITOR--********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def put_brick(self, mouse_x, mouse_y):
        row, column = self.get_pos_on_grid((mouse_x, mouse_y))
        x, y = self.get_pos_on_screen(row, column)
        p = self.get_index_brick_position(row, column)

        if self.toolbar.selected_type == "type_simple":
            self.bricks[p] = BrickSimple(x, y, self.toolbar.selected_color)
        elif self.toolbar.selected_type == "type_double":
            self.bricks[p] = BrickDouble(x, y, self.toolbar.selected_color)
        elif self.toolbar.selected_type == "type_immortal":
            self.bricks[p] = BrickImmortal(x, y)

    def delete_brick(self, mouse_x, mouse_y):
        p = self.get_index_brick_mouse((mouse_x, mouse_y))
        self.bricks[p] = None

    def save_level(self):
        list_bricks = []
        options['title'] = 'Save level'
        for column in range(0, MAX_CLN):
            for row in range(0, MAX_ROW):
                p = self.get_index_brick_position(row, column)
                if self.bricks[p] is None:
                    list_bricks.append(None)
                else:
                    brk = dict(cln=column, row=row, color=self.bricks[p].color, type=self.bricks[p].type)
                    list_bricks.append(brk)

        filename = asksaveasfilename(**options)
        if filename:
            with open(filename, "w") as level:
                dump(list_bricks, level)
                level.close()

    def load_level(self):
        self.clear_screen()
        options['title'] = 'Open level'
        filename = askopenfilename(**options)
        if filename:
            with open(filename) as data_file:
                data = load(data_file)
                data_file.close()

            for p in range(0, MAX_ROW * MAX_CLN):
                if data[p] is not None:
                    x, y = self.get_pos_on_screen(data[p]["row"], data[p]["cln"])
                    tp = data[p]["type"]
                    if tp == "type_simple":
                        self.bricks[p] = BrickSimple(x, y, data[p]["color"])
                    elif tp == "type_double":
                        self.bricks[p] = BrickDouble(x, y, data[p]["color"])
                    elif tp == "type_immortal":
                        self.bricks[p] = BrickImmortal(x, y)
                else:
                    self.bricks[p] = None

    def clear_screen(self):
        brks = self.bricks.copy_brk()
        for p in range(0, MAX_ROW * MAX_CLN):
            self.bricks[p] = None
        return brks

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--INPUT--*************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_key_press(self, keys):
        if keys[pygame.K_ESCAPE]:  # chiudi finestra
            self.on_exit()
        if keys[pygame.K_c]:
            self.clear_screen()
        if keys[pygame.K_s]:
            self.save_level()
        if keys[pygame.K_l]:
            self.load_level()

    def on_mouse_motion(self, mouse_x, mouse_y):
        if self.toolbar.selected_color is not None and self.is_on_grid((mouse_x, mouse_y)):
            if self.current_mode == MODE_PAINT and self.is_on_grid((mouse_x, mouse_y)):
                self.put_brick(mouse_x, mouse_y)
            if self.current_mode == MODE_DELETE and self.is_on_grid((mouse_x, mouse_y)):
                self.delete_brick(mouse_x, mouse_y)

    def on_mouse_press(self, mouse_x, mouse_y, button):
        # bottone destro mouse down
        if button == MB_LEFT:
            # controllo selezione bottone tipo
            self.type_selected = self.toolbar.handle_input_type((mouse_x, mouse_y))
            # controllo selezione bottone colore
            self.toolbar.handle_input_color((mouse_x, mouse_y))
            # controllo click bottone tool
            self.toolbar.handle_input_tool((mouse_x, mouse_y))

            # click sulla griglia
            if self.is_on_grid((mouse_x, mouse_y)):
                p = self.get_index_brick_mouse((mouse_x, mouse_y))
                if self.bricks[p] is None and self.toolbar.selected_color is not None:  # paint
                    self.current_mode = MODE_PAINT
                    self.put_brick(mouse_x, mouse_y)
                elif self.bricks[p] is not None:  # drag and drop
                    self.current_mode = MODE_MOVE
                    x, y = self.get_pos_brick((mouse_x, mouse_y))
                    self.drag_drop = dict(old_pos=p, offset_x=abs(mouse_x - x), offset_y=abs(mouse_y - y),
                                          brk=self.bricks[p])
                    self.bricks[p] = None

        # bottone sinistro del mouse
        if button == MB_RIGHT:
            if self.is_on_grid((mouse_x, mouse_y)):
                self.current_mode = MODE_DELETE
                self.delete_brick(mouse_x, mouse_y)

    ## FIX ME:  brks = self.bricks.copy_brk() AttributeError: 'list' object has no attribute 'copy_brk'
    def on_mouse_release(self, mouse_x, mouse_y, button: int):
        if button == MB_LEFT:  # bottone destro mouse up
            for k in self.toolbar.bt_tool.keys():
                if self.toolbar.bt_tool[k].is_clicked((mouse_x, mouse_y)):
                    if k == "exit":
                        self.on_exit()
                    elif k == "clear":
                        self.clear_screen()
                    elif k == "save":
                        self.save_level()
                    elif k == "load":
                        self.load_level()
                # se non sono piu' sul bottone comunque lo deseleziono
                self.toolbar.bt_tool[k].selected = False

        # drag and drop
        if self.current_mode == MODE_MOVE:
            idx = self.get_index_brick_mouse((mouse_x, mouse_y))
            if self.is_on_grid((mouse_x, mouse_y)) and self.bricks[idx] is None:
                self.drag_drop['brk'].rect.x, self.drag_drop['brk'].rect.y = self.get_pos_brick((mouse_x, mouse_y))
            else:
                idx = self.drag_drop['old_pos']
            self.bricks[idx] = self.drag_drop['brk']
            self.drag_drop = None

        self.current_mode = MODE_NONE
