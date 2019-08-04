from Editor_v1_pygame.editor import Editor
import tkinter as Tk
from costanti.game_v1_arcade_costanti import WINDOW_WIDTH, WINDOW_HEIGHT

if __name__ == '__main__':

    ROOT = Tk.Tk()
    ROOT.withdraw()

    editor = Editor(WINDOW_WIDTH, WINDOW_HEIGHT)
    editor.setup()
    editor.run()
   

