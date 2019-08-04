import arcade
from costanti.images_names import *


class Immagini:
    background = None
    img_ball = None
    img_edge = None
    img_paddle = []
    img_paddle_shoot = []

    img_brick = dict()
    img_brick_break = dict()

    img_button_orange = None
    img_button_yellow = None

    @classmethod
    def load_img(cls):
        #  backgound
        cls.img_edge = arcade.load_texture(resource_path(img_edge))
        cls.background = arcade.load_texture(resource_path(img_background_0))

        #  ball
        cls.img_ball = arcade.load_texture(resource_path(img_ball))

        #  paddle
        for i in range(0, 2):
            cls.img_paddle.append(arcade.load_texture(resource_path(img_paddle[i])))
            cls.img_paddle_shoot.append(arcade.load_texture(resource_path(img_paddle_shoot[i])))

        #  Bricks
        for color in colors:
            cls.img_brick[color] = arcade.load_texture(resource_path(img_bricks[color]))
            cls.img_brick_break[color] = arcade.load_texture(resource_path(img_bricks_break[color]))

        cls.img_brick[ID_GREY] = arcade.load_texture(resource_path(img_bricks_break[ID_GREY]))

        #  button
        cls.img_button_orange = arcade.load_texture(resource_path(img_button_orange))
        cls.img_button_yellow = arcade.load_texture(resource_path(img_button_yellow))
