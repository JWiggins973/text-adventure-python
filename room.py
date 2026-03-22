# Room class


class Room:
    def __init__(self, name, room_dict):
        """Initialize a Room object with a name and a dictionary of exits and items."""
        self.name = name
        self.exits = {
            k: room_dict[k] for k in room_dict if k != "item"
        }  # access only direction keys
        if "item" in room_dict:
            self.item = room_dict["item"]  # the item exists
        else:
            self.item = None  # the item does not exist

    # Return whether the room has an item or not
    def has_item(self):
        """Return True if the room has an item, False otherwise."""
        return self.item is not None

    # Return item in room
    def get_item(self):
        """Return the item in the room, or None if there is no item."""
        return self.item

    # Remove item from room
    def remove_item(self):
        """Remove the item from the room. Set the item to None."""
        self.item = None

    # Return the exits from the room
    def get_exits(self):
        """Return the exits from the room as a dictionary."""
        return self.exits
