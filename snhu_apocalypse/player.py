# Author: Jermaine Wiggins
# Date: 2026-04-19
# Purpose: Player model - tracks inventory, current room, and health state

from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from .room import Room

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, current_room: Room, inventory: list[str] | None = None) -> None:
        """Initialize a Player object with a current room and an inventory."""
        self.current_room = current_room
        # Use None as default instead of [] to avoid the mutable default argument pitfall
        # where all Player instances would share the same list
        self.inventory: list[str] = inventory if inventory is not None else []

    def add_to_inventory(self, item: str) -> None:
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        logger.debug("Added '%s' to inventory", item)

    def move(self, direction: str) -> bool:
        """Move the player in the given direction. Returns True if the move succeeded."""
        exits = self.current_room.get_exits()
        if direction in exits:
            self.current_room = exits[direction]
            logger.debug("Moved %s to '%s'", direction, self.current_room.name)
            return True
        logger.debug(
            "Invalid move: no exit '%s' from '%s'", direction, self.current_room.name
        )
        return False
