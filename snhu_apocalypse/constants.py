# Author: Jermaine Wiggins
# Date: 2026-04-19
# Purpose: Shared enums and constants - Direction, RoomName, Item, and layout settings

from enum import StrEnum


LINE_WIDTH = 60


class Direction(StrEnum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class RoomName(StrEnum):
    LIBRARY = "Library"
    GYM = "Gym"
    SCIENCE_LAB = "Science Lab"
    CAFETERIA = "Cafeteria"
    HEALTH_CENTER = "Health Center"
    SECURITY_ROOM = "Security Room"
    MAINTENANCE_ROOM = "Maintenance Room"
    EXIT = "Exit"


class Item(StrEnum):
    BASEBALL_BAT = "Baseball bat"
    CHEMICAL = "Chemical"
    APRON = "Apron"
    BANDAGES = "Bandages"
    RADIO = "Radio"
    GLOVE = "Glove"
    PRINCIPAL_X = "Principal X"
