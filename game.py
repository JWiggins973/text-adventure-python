# Game class to manage the game state and interactions
from room import Room  # Import the Room class from the room module
from player import Player  # Import the Player class from the player module
import tkinter as tk  # Import tkinter for GUI elements


LINE_WIDTH = 60  # Constant for line width in print statements


class Game:
    def __init__(self):
        """Initialize the Game class."""
        self.rooms = self.create_rooms()
        self.player = Player(self.rooms["Library"])  # Start in the Library

    def create_rooms(self):
        """Create the rooms for the game and return a dictionary of Room objects."""
        # Define the room structure with exits and items
        room_dict = {
            "Library": {
                "N": "Gym",
                "S": "Cafeteria",
                "W": "Science Lab",
                "E": "Security Room",
            },
            "Gym": {"E": "Maintenance Room", "S": "Library", "item": "Baseball bat"},
            "Science Lab": {"E": "Library", "item": "Chemical"},
            "Cafeteria": {"N": "Library", "E": "Health Center", "item": "Apron"},
            "Health Center": {"W": "Cafeteria", "item": "Bandages"},
            "Security Room": {"W": "Library", "N": "Exit", "item": "Radio"},
            "Maintenance Room": {"W": "Gym", "item": "Glove"},
            "Exit": {"S": "Security Room", "item": "Principal X"},
        }
        # Create Room objects for each room in the room_dict
        rooms = {
            room_name: Room(room_name, room_info)
            for room_name, room_info in room_dict.items()
        }
        # Update the exits in each Room object to reference the actual Room objects instead of just the room names
        for room in rooms.values():
            room.exits = {
                direction: rooms[destination]
                for direction, destination in room.exits.items()
            }

        return rooms

    # Print game instructions
    def game_instructions(self):
        """Print the game instructions to the player."""
        line = "-" * LINE_WIDTH
        main_menu = [
            line,
            "Welcome to SNHU Apocalypse",
            "Main Menu",
            line,
            "To Defeat Principal X and Escape",
            "**Collect all 6 items**",
            "Click a room button to move",
            "Click Pick Up Item to collect items",
            "Good Luck!",
            line,
        ]

        # Build String to display in GUI
        result = ""
        for item in main_menu:
            result += "{:^{}}".format(item, LINE_WIDTH) + "\n"
        return result

    # Print the player's current status
    def player_status(self):
        """Displays the player's current status, including location,  and inventory"""
        status = ""
        if self.player.current_room.name == "Exit":
            status += "You made it to the Exit\n"
            status += "You see Principal X\n"
            status += "He charges at you\n"
        else:
            status += f"You are in the {self.player.current_room.name}\n"
            status += f"Items in Backpack: {self.player.inventory}\n"
            if self.player.current_room.has_item():
                status += f"You see a {self.player.current_room.get_item()}\n"
            else:
                status += "No items in this room\n"
        return status

    # Get and validate user input for item pickup
    def get_and_validate_get_item(self):
        """Get and validate user input for picking up an item."""
        get = input("Pick up item? ").capitalize()
        valid_input_get_item = ["Y", "N"]
        while get not in valid_input_get_item:
            get = input(
                "Invalid input, please enter Y / N to pick up or leave item? "
            ).capitalize()
        return get

    # Get and validate user input for moves
    def get_and_validate_moves(self):
        """Get and validate user input for moving to a new room."""
        valid_moves = self.player.get_valid_moves()
        moves = input("Enter move: ").capitalize()
        while moves not in valid_moves:
            print("Nice try, you can not escape out the window")
            print(f"Valid moves for {self.player.current_room.name} are: {valid_moves}")
            moves = input("Enter a valid move: ").capitalize()
        return moves

    # Win lose logic when player reaches the Exit, checks if player has all 6 items to determine outcome of game
    def check_win_lose(self):
        if len(self.player.inventory) == 6:
            status = (
                "You have all 6 items,\n"
                + "you were able to defeat Principal X and escape!"
            )
        else:
            status = "You do not have all 6 items, \n"
            status += "Principal X overpowers you \n"
            status += "and you lose!"
        return status

    # Run the main game loop
    def main_loop(self):
        """Run the main game loop, handling player input and game interactions."""

        # Call games instructions at the start of the game
        self.game_instructions()

        # start the game loop, continue until player reaches the Exit
        while self.player.current_room.name != "Exit":

            # Print the player's current status at the start of each loop iteration
            self.player_status()

            # If the current room has an item, ask the player if they want to pick it up
            if self.player.current_room.has_item():
                get_item = self.get_and_validate_get_item()
                if get_item == "Y":
                    # Add the item to the player's inventory and remove it from the room
                    self.player.add_to_inventory(self.player.current_room.get_item())
                    self.player.current_room.remove_item()

            # Move the player to a new room based on their input
            get_move = self.get_and_validate_moves()
            self.player.move(get_move)

        # Final status when player reaches the Exit
        self.player_status()
        # Check if the player has all 6 items to determine the outcome of the game
        print(self.check_win_lose())
