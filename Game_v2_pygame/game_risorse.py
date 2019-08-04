#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from costanti.images_names import *
from costanti.game_v2_pygame_costanti import *
from costanti.color import WHITE, BLACK


def load_texture(img_file, size):
    """
    Carica l'immagine dal file e scalala a dimensioni size
    :param img_file: file immagine
    :param size: dimenzioni dell'immagine
    :return:
    """
    img = pygame.image.load(resource_path(img_file)).convert()
    img = pygame.transform.scale(img, size)
    img.set_colorkey(BLACK)
    if img_file == img_button_yellow or img_file == img_button_orange:
        img.set_colorkey(WHITE)
    return img


def load_background(img_file, size):
    """
    Carica l'immagine dal file e scalala a dimensioni size
    :param img_file: file immagine
    :param size: dimenzioni dell'immagine
    :return:
    """
    img = pygame.image.load(resource_path(img_file)).convert()
    img = pygame.transform.scale(img, size)
    return img


def load_texture_rotate(img_file, size, angle):
    """
    Carica l'immagine da file, la ruota di angle, la scala alle dimensioni size
    :param img_file: file dell'immagine
    :param size: dimensione dell'immagine
    :param angle: angolo di rotazione
    :return:
    """
    img = pygame.image.load(resource_path(img_file)).convert()
    img = pygame.transform.rotate(img, angle)
    img = pygame.transform.scale(img, size)
    img.set_colorkey(BLACK)
    img.set_colorkey(WHITE)
    return img


class MyFont:
    """
    pygame.font.SysFont
    """
    font60 = None
    font50 = None
    font40 = None
    font30 = None
    font20 = None

    def __init__(self):
        pass

    @staticmethod
    def init_font():
        MyFont.font60 = pygame.font.SysFont("algerian", 60)
        MyFont.font50 = pygame.font.SysFont("goudy stout", 50)
        MyFont.font40 = pygame.font.SysFont("impact", 40)
        MyFont.font30 = pygame.font.SysFont("impact", 30)
        MyFont.font20 = pygame.font.SysFont("impact", 20)


class Immagini:
    """
    pygame.image
    """
    background = None
    backgrounds = None
    img_ball = None
    img_edge_v = None
    img_edge_h = None
    img_life = None

    img_paddle = []

    img_brick = dict()
    img_brick_break = dict()

    img_button_orange = None
    img_button_yellow = None

    def __init__(self):
        pass

    @staticmethod
    def load_img():
        #  backgound
        Immagini.img_edge_v = load_texture(img_edge, (EDGE_SIZE, EDGE_V_HEIGHT))
        Immagini.img_edge_h = load_texture_rotate(img_edge, (EDGE_H_WIDTH, EDGE_SIZE), 90)

        Immagini.backgrounds = []
        Immagini.background = load_background(img_background_0, (SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT))
        Immagini.backgrounds.append(load_background(img_background_1, (SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT)))
        Immagini.backgrounds.append(load_background(img_background_2, (SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT)))
        Immagini.backgrounds.append(load_background(img_background_3, (SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT)))
        Immagini.backgrounds.append(load_background(img_background_4, (SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT)))
        Immagini.backgrounds.append(load_background(img_background_5, (SCREEN_LEVEL_WIDTH, SCREEN_LEVEL_HEIGHT)))

        #  ball
        Immagini.img_ball = load_texture(img_ball, (BALL_RADIUS * 2, BALL_RADIUS * 2))
        Immagini.img_life = load_texture(img_life, (LIFE_SIZE, LIFE_SIZE))

        #  paddle
        for i in range(0, 3):
            Immagini.img_paddle.append(load_texture(img_paddle[i], (PADDLE_WIDTH, PADDLE_HEIGHT)))

        #  Bricks
        for color in colors:
            Immagini.img_brick[color] = load_texture(img_bricks[color], (BRICK_WIDTH, BRICK_HEIGHT))
            Immagini.img_brick_break[color] = load_texture(img_bricks_break[color], (BRICK_WIDTH, BRICK_HEIGHT))

        Immagini.img_brick[ID_GREY] = load_texture(img_bricks[ID_GREY], (BRICK_WIDTH, BRICK_HEIGHT))

        #  button
        Immagini.img_button_orange = load_texture(img_button_orange, (BUTTON_WIDTH, BUTTON_HEIGHT))
        Immagini.img_button_yellow = load_texture(img_button_yellow, (BUTTON_WIDTH, BUTTON_HEIGHT))
