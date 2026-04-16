import logging
from .room import Room
from .player import Player
from .constants import Direction, RoomName, Item, LINE_WIDTH

logger = logging.getLogger(__name__)

# Room layout as a module-level constant
ROOM_DATA: dict[str, dict] = {
    RoomName.LIBRARY: {
        Direction.NORTH: RoomName.GYM,
        Direction.SOUTH: RoomName.CAFETERIA,
        Direction.WEST: RoomName.SCIENCE_LAB,
        Direction.EAST: RoomName.SECURITY_ROOM,
    },
    RoomName.GYM: {
        Direction.EAST: RoomName.MAINTENANCE_ROOM,
        Direction.SOUTH: RoomName.LIBRARY,
        "item": Item.BASEBALL_BAT,
    },
    RoomName.SCIENCE_LAB: {
        Direction.EAST: RoomName.LIBRARY,
        "item": Item.CHEMICAL,
    },
    RoomName.CAFETERIA: {
        Direction.NORTH: RoomName.LIBRARY,
        Direction.EAST: RoomName.HEALTH_CENTER,
        "item": Item.APRON,
    },
    RoomName.HEALTH_CENTER: {
        Direction.WEST: RoomName.CAFETERIA,
        "item": Item.BANDAGES,
    },
    RoomName.SECURITY_ROOM: {
        Direction.WEST: RoomName.LIBRARY,
        Direction.NORTH: RoomName.EXIT,
        "item": Item.RADIO,
    },
    RoomName.MAINTENANCE_ROOM: {
        Direction.WEST: RoomName.GYM,
        "item": Item.GLOVE,
    },
    RoomName.EXIT: {
        Direction.SOUTH: RoomName.SECURITY_ROOM,
        "item": Item.PRINCIPAL_X,
    },
}


class Game:
    def __init__(self) -> None:
        """Initialize the Game class."""
        self.rooms = self._create_rooms()
        self.player = Player(self.rooms[RoomName.LIBRARY])
        # Count collectible items at game start, excludes Exit since Principal X is not a pickup
        self.total_items: int = sum(
            1 for room in self.rooms.values()
            if room.name != RoomName.EXIT and room.has_item()
        )

    def _create_rooms(self) -> dict[str, Room]:
        """Create Room objects from ROOM_DATA and wire up exit references."""
        # First pass: create Room objects with string-based exit names
        rooms = {
            room_name: Room(room_name, room_info)
            for room_name, room_info in ROOM_DATA.items()
        }
        # Second pass: replace string exit names with actual Room object references
        for room in rooms.values():
            room.set_exits({
                direction: rooms[destination]
                for direction, destination in room.get_exits().items()
            })
        return rooms

    # Public methods for GameGUI

    def is_game_over(self) -> bool:
        """Return True if the player has reached the Exit room."""
        return self.player.current_room.name == RoomName.EXIT

    def move(self, direction: str) -> bool:
        """Move the player in the given direction. Returns True if the move succeeded."""
        result = self.player.move(direction)
        if not result:
            logger.info("Move blocked: no exit '%s' from '%s'", direction, self.player.current_room.name)
        return result

    def pick_up_item(self) -> bool:
        """Pick up the item in the current room. Returns True if an item was picked up."""
        if self.player.current_room.has_item():
            item = self.player.current_room.get_item()
            self.player.add_to_inventory(item)
            self.player.current_room.remove_item()
            logger.info("Picked up '%s' in '%s'", item, self.player.current_room.name)
            return True
        logger.debug("No item to pick up in '%s'", self.player.current_room.name)
        return False

    def current_room_has_item(self) -> bool:
        """Return True if the current room contains an item."""
        return self.player.current_room.has_item()

    def get_current_room_exits(self) -> dict[str, Room]:
        """Return the exits dictionary for the current room."""
        return self.player.current_room.get_exits()

    def get_current_room_name(self) -> str:
        """Return the name of the current room."""
        return self.player.current_room.name

    def get_inventory(self) -> list[str]:
        """Return a copy of the player's current inventory."""
        return list(self.player.inventory)

    def reset(self) -> None:
        """Reset all game state back to the beginning."""
        self.rooms = self._create_rooms()
        self.player = Player(self.rooms[RoomName.LIBRARY])

    # Status and display methods

    def game_instructions(self) -> str:
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

    def player_status(self) -> str:
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
                f"Items in Backpack: {self.get_inventory()}",
                f"You see a {self.player.current_room.get_item()}"
                if self.player.current_room.has_item()
                else "No items in this room",
            ]
        return "\n".join(lines) + "\n"

    def check_win_lose(self) -> str:
        """Return a win or lose message based on the player's inventory at the Exit."""
        # Win condition: player collected every item before reaching the Exit
        if len(self.get_inventory()) == self.total_items:
            return (
                f"You have all {self.total_items} items,\n"
                "you were able to defeat Principal X and escape!"
            )
        return "\n".join([
            f"You do not have all {self.total_items} items,",
            "Principal X overpowers you",
            "and you lose!",
        ])
