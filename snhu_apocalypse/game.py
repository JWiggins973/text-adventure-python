# Game class to manage the game state and logic
from .room import Room
from .player import Player


LINE_WIDTH = 60   # Controls the width of centered text in the instructions screen
START_ROOM = "Library"  # The room the player begins in
EXIT_ROOM = "Exit"      # The final room that triggers the win/lose check


class Game:
    def __init__(self):
        """Initialize the Game class."""
        self.rooms = self.create_rooms()
        self.player = Player(self.rooms[START_ROOM])
        # Count collectible items at game start — excludes Exit since Principal X is not a pickup
        self.total_items = sum(
            1 for room in self.rooms.values()
            if room.name != EXIT_ROOM and room.has_item()
        )

    def create_rooms(self):
        """Create the rooms for the game and return a dictionary of Room objects."""
        # Room layout: keys are cardinal directions (N/S/E/W) and optional item
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
            "Security Room": {"W": "Library", "N": EXIT_ROOM, "item": "Radio"},
            "Maintenance Room": {"W": "Gym", "item": "Glove"},
            EXIT_ROOM: {"S": "Security Room", "item": "Principal X"},
        }

        # First pass: create Room objects with string-based exit names
        rooms = {
            room_name: Room(room_name, room_info)
            for room_name, room_info in room_dict.items()
        }

        # Second pass: replace string exit names with actual Room object references
        # This allows rooms to reference each other directly for navigation
        for room in rooms.values():
            room.set_exits({
                direction: rooms[destination]
                for direction, destination in room.get_exits().items()
            })

        return rooms

    # --- Facade methods ---
    # These give GameGUI a clean interface so it never needs to reach into
    # game.player or game.player.current_room directly.

    def is_game_over(self):
        """Return True if the player has reached the Exit room."""
        return self.player.current_room.name == EXIT_ROOM

    def move(self, direction):
        """Move the player in the given direction."""
        self.player.move(direction)

    def pick_up_item(self):
        """Pick up the item in the current room and add it to the player's inventory."""
        if self.player.current_room.has_item():
            item = self.player.current_room.get_item()
            self.player.add_to_inventory(item)
            self.player.current_room.remove_item()

    def current_room_has_item(self):
        """Return True if the current room contains an item."""
        return self.player.current_room.has_item()

    def get_current_room_exits(self):
        """Return the exits dictionary for the current room."""
        return self.player.current_room.get_exits()

    def get_current_room_name(self):
        """Return the name of the current room."""
        return self.player.current_room.name

    def reset(self):
        """Reset all game state back to the beginning."""
        self.rooms = self.create_rooms()
        self.player = Player(self.rooms[START_ROOM])

    # --- Status and display methods ---

    def game_instructions(self):
        """Return the game instructions as a centered, formatted string."""
        line = "-" * LINE_WIDTH
        main_menu = [
            line,
            "Welcome to SNHU Apocalypse",
            "Main Menu",
            line,
            "To Defeat Principal X and Escape",
            f"**Collect all {self.total_items} items**",
            "Click a room button to move",
            "Click Pick Up Item to collect items",
            "Good Luck!",
            line,
        ]
        # Center each line within LINE_WIDTH for a clean menu appearance
        return "\n".join("{:^{}}".format(item, LINE_WIDTH) for item in main_menu) + "\n"

    def player_status(self):
        """Return the player's current status as a string."""
        if self.is_game_over():
            # Exit room gets a special narrative message instead of normal status
            lines = [
                "You made it to the Exit",
                "You see Principal X",
                "He charges at you",
            ]
        else:
            lines = [
                f"You are in the {self.player.current_room.name}",
                f"Items in Backpack: {self.player.inventory}",
                f"You see a {self.player.current_room.get_item()}"
                if self.player.current_room.has_item()
                else "No items in this room",
            ]
        return "\n".join(lines) + "\n"

    def check_win_lose(self):
        """Return a win or lose message based on the player's inventory at the Exit."""
        # Win condition: player collected every item before reaching the Exit
        if len(self.player.inventory) == self.total_items:
            return (
                f"You have all {self.total_items} items,\n"
                "you were able to defeat Principal X and escape!"
            )
        return "\n".join([
            f"You do not have all {self.total_items} items,",
            "Principal X overpowers you",
            "and you lose!",
        ])
