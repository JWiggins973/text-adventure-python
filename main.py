from game import Game  # Import the Game class from the game module
from gameGui import GameGUI  # Import the GameGUI class from the gameGui module

if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    gui = GameGUI(
        game
    )  # Create an instance of the GameGUI class, passing the game instance
    gui.update_gui()  # Update the GUI with the initial game state
    gui.main_loop()  # Start the main game loop
