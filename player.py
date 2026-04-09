# Player class — tracks current room and collected items


class Player:
    def __init__(self, current_room, inventory=None):
        """Initialize a Player object with a current room and an inventory."""
        self.current_room = current_room
        # Use None as default instead of [] to avoid the mutable default argument pitfall
        # where all Player instances would share the same list
        self.inventory = inventory if inventory is not None else []

    def add_to_inventory(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)

    def move(self, direction):
        """Move the player to a new room based on the chosen direction."""
        exits = self.current_room.get_exits()
        if direction in exits:
            self.current_room = exits[direction]
