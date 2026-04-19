# Author: Jermaine Wiggins
# Date: 2026-04-19
# Purpose: Entry point -- initializes game state and launches the GUI

from snhu_apocalypse.game import Game
from snhu_apocalypse.gui import GameGUI

if __name__ == "__main__":
    # Create the game state first, then pass it to the GUI
    # This keeps game logic separate from the display layer
    game = Game()
    gui = GameGUI(game)
    gui.main_loop()
