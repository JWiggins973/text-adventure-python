# Player class for the game

import room  # Import the Room class from the room module


class Player:
    def __init__(self, current_room, inventory=None):
        """Initialize a Player object with a current room and an inventory."""
        self.current_room = current_room
        if inventory is None:
            self.inventory = []
        else:
            self.inventory = inventory

    # Add item to the player's inventory
    def add_to_inventory(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)

    # Check valid moves for the player based on the current room's exits
    def get_valid_moves(self):
        """Return a list of valid moves based on the current room's exits."""
        return list(self.current_room.get_exits().keys())

    # Move the player to a new room based on the chosen direction
    def move(self, direction):
        """Move the player to a new room based on the chosen direction."""
        if direction in self.current_room.get_exits():
            self.current_room = self.current_room.get_exits()[direction]
        else:
            raise ValueError(
                "Invalid move: No exit in that direction."
            )  # Invalid direction raises ValueError, caught by try/except in Game to prevent crash
