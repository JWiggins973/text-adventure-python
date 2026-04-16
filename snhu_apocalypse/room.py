# Room class — represents a single location in the game world


class Room:
    def __init__(self, name, room_dict):
        """Initialize a Room object with a name and a dictionary of exits and items."""
        self.name = name
        # Filter out the "item" key so exits only contain directional keys (N/S/E/W)
        self.exits = {k: room_dict[k] for k in room_dict if k != "item"}
        # Store the item if the room has one, otherwise None means the room is empty
        self.item = room_dict.get("item", None)

    def has_item(self):
        """Return True if the room has an item, False otherwise."""
        return self.item is not None

    def get_item(self):
        """Return the item in the room, or None if there is no item."""
        return self.item

    def remove_item(self):
        """Remove the item from the room after the player picks it up."""
        self.item = None

    def get_exits(self):
        """Return the exits from the room as a dictionary of direction to Room."""
        return self.exits

    def set_exits(self, exits):
        """Set the exits for the room as a dictionary of direction to Room mappings."""
        self.exits = exits
