import logging

logger = logging.getLogger(__name__)


class Room:
    def __init__(self, name: str, room_dict: dict) -> None:
        """Initialize a Room object with a name and a dictionary of exits and items."""
        self.name = name
        # Filter out the "item" key so exits only contain directional keys (N/S/E/W)
        self.exits: dict[str, Room] = {k: room_dict[k] for k in room_dict if k != "item"}
        # Store the item if the room has one, otherwise None means the room is empty
        self.item: str | None = room_dict.get("item", None)

    def has_item(self) -> bool:
        """Return True if the room has an item, False otherwise."""
        return self.item is not None

    def get_item(self) -> str | None:
        """Return the item in the room, or None if there is no item."""
        return self.item

    def remove_item(self) -> None:
        """Remove the item from the room after the player picks it up."""
        self.item = None

    def get_exits(self) -> dict[str, Room]:
        """Return the exits from the room as a dictionary of direction to Room."""
        return self.exits

    def set_exits(self, exits: dict[str, Room]) -> None:
        """Set the exits for the room as a dictionary of direction to Room mappings."""
        self.exits = exits
