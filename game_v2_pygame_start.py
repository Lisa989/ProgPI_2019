from Game_v2_pygame.game import Game
from costanti.game_v2_pygame_costanti import WINDOW_WIDTH, WINDOW_HEIGHT

if __name__ == '__main__':
    game = Game(WINDOW_WIDTH, WINDOW_HEIGHT)
    game.setup()
    game.run()

