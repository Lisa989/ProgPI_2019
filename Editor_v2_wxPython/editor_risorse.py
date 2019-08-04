import wx
from costanti.editor_v2_wxPython_costanti import *
from costanti.images_names import *


class Immagini:
    background = None
    edge_top = None
    edge_vertical = None
    buttons_yellow = dict()
    buttons_orange = dict()
    type_label = None
    color_label = None

    color_bricks = dict()
    bricks = dict()
    bricks_break = dict()

    @classmethod
    def load(cls):
        #  label
        cls.type_label = cls.load_scale(img_label_type_brick, BUTTON_WIDTH, BUTTON_HEIGHT)
        cls.color_label = cls.load_scale(img_label_color_brick, BUTTON_WIDTH, BUTTON_HEIGHT)

        #  backround
        cls.background = cls.load_scale(img_background_0, SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT)
        edge = wx.Image(img_edge)
        cls.edge_vertical = cls.scale_image(edge, EDGE_VERTICAL_SIZE[0], EDGE_VERTICAL_SIZE[1])
        edge = edge.Rotate90()
        cls.edge_top = cls.scale_image(edge, EDGE_TOP_SIZE[0], EDGE_TOP_SIZE[1])

        #  button
        for tp in type_bt:
            cls.buttons_yellow[tp] = cls.load_scale(img_buttons_yellow[tp], BUTTON_WIDTH, BUTTON_HEIGHT)
            cls.buttons_orange[tp] = cls.load_scale(img_buttons_orange[tp], BUTTON_WIDTH, BUTTON_HEIGHT)

        #  colori briks e bricks
        for color in colors:
            cls.color_bricks[color] = cls.load_scale(img_brick_colors[color], BUTTON_COLOR_SIZE, BUTTON_COLOR_SIZE)
            cls.bricks[color] = cls.load_scale(img_bricks[color], BRICK_WIDTH, BRICK_HEIGHT)
            cls.bricks_break[color] = cls.load_scale(img_bricks_break[color], BRICK_WIDTH, BRICK_HEIGHT)

        cls.bricks[ID_GREY] = cls.load_scale(img_bricks[ID_GREY], BRICK_WIDTH, BRICK_HEIGHT)

    @staticmethod
    def load_scale(file, width, height):
        """
        Carica l'immagine da file e ne restitusce la Bitmap delle dimensioni richieste
        :param file: file immagine
        :param width:
        :param height:
        :return: bitmat delle dimensioni indicate
        """
        image = wx.Image(resource_path(file))
        return Immagini.scale_image(image, width, height)

    @staticmethod
    def scale_bitmap(bitmap, width, height):
        """
        Scala la bitmap
        :param bitmap: wx.Bitmap da scalare
        :param width: larghezza
        :param height: altezza
        :return: wx.Bitmap scalata
        """
        image = wx.ImageFromBitmap(bitmap)
        Immagini.scale_image(image, width, height)

    @staticmethod
    def scale_image(image, width, height):
        """
        Scala l'mmagine e restituisce la bitmap corrispondente
        :param image: wx.Image da scalare
        :param width: larghezza
        :param height: altezza
        :return: wx.Bitmap scalata
        """
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result


class Icone:
    quit = None
    new = None
    open = None
    save = None
    clear = None
    copy = None
    cut = None
    paste = None
    undo = None
    redo =None
    # icon_zoom_in = None
    # icon_zoom_out = None
    edit = None
    move = None
    delete = None
    select = None

    @classmethod
    def load(cls):
        tsize = (24, 24)
        w, h = tsize
        cls.quit = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, tsize)
        cls.new = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        cls.open = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        cls.save = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        cls.clear = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, tsize)
        cls.copy = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        cls.cut = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, tsize)
        cls.paste = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)
        cls.undo = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, tsize)
        cls.redo = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, tsize)
        # icon_zoom_in = get_bitmap(wx.ART_PLUS, wx.ART_TOOLBAR, tsize)
        # icon_zoom_out = get_bitmap(wx.ART_MINUS, wx.ART_TOOLBAR, tsize)
        cls.edit = Immagini.load_scale(img_pencil, w, h)
        cls.move = Immagini.load_scale(img_move, w, h)
        cls.delete = Immagini.load_scale(img_trash, w, h)
        cls.select = Immagini.load_scale(img_cursor, w, h)
