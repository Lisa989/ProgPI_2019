import arcade
from Game_v1_arcade.game import Game

from costanti.game_v1_arcade_costanti import WINDOW_WIDTH, WINDOW_HEIGHT


if __name__ == '__main__':
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT)
    game.setup()
    arcade.run()
