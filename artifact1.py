# FIXME: Add module-level docstring (program name, author, date, purpose)
# Jermaine Wiggins
# FIXME: Add LINE_WIDTH = 40 constant here and replace all hardcoded 40s


def game_instructions():
    line = "-" * 40  # FIXME: Replace 40 with LINE_WIDTH constant
    main_menu = [
        line,
        "Welcome to SNHU Apocalypse",
        "Main Menu",
        line,
        "To Defeat Principal X and Escape",
        "**Collect all 6 items**",
        "Move Commands: N, S, E, W",
        "Add to Backpack: Type Y/N",
    ]
    for line in main_menu:  # FIXME: Add comment explaining this loop
        print("{:^40}".format(line))  # FIXME: Replace 40 with LINE_WIDTH constant
    print()


def player_status(current, backpack, room):
    # FIXME: Add comment explaining what this function does
    # FIXME: Split into two functions - one for normal rooms, one for exit/boss room
    if current == "Exit":
        print("You made it to the Exit")
        print("You see Principal X")
        print("He charges at you")
    else:
        print("You are in the", current)
        print("Items in Backpack:", backpack)
        if "item" in room[current]:
            print("You see a", room[current]["item"])


def get_and_validate_get_item():
    # FIXME: Add comment explaining what this function does
    get = input("Pick up item? ").capitalize()
    valid_input_get_item = ["Y", "N"]
    while get not in valid_input_get_item:  # FIXME: Add comment explaining this loop
        get = input(
            "Invalid input, please enter Y / N to pick up or leave item? "
        ).capitaliz
    return get


def get_and_validate_moves(valid_moves, current):
    # FIXME: Add comment explaining what this function does
    moves = input("Enter move: ").capitalize()
    while moves not in valid_moves:  # FIXME: Add comment explaining this loop
        print("Nice try, you can not escape out the window")
        print(f"Valid moves for {current} are: {valid_moves}")
        moves = input("Enter a valid move: ").capitalize()
    return moves


def main():
    current = "Library"
    backpack = []
    # FIXME: Rename to current_room or player_location
    line_seperator = (
        "-" * 40
    )  # FIXME: Fix spelling to line_separator, replace 40 with LINE_WIDTH
    # FIXME: Add comment explaining the room dictionary structure
    room = {
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

    game_instructions()

    while current != "Exit":
        player_status(current, backpack, room)
        if "item" in room[current]:  # FIXME: Add comment explaining this block
            get_item = get_and_validate_get_item()
            if get_item == "Y":
                print(f"You picked up the {room[current]['item']}")
                backpack.append(room[current]["item"])
                del room[current]["item"]
        valid_moves = [key for key in room[current] if key != "item"]
        move = get_and_validate_moves(valid_moves, current)
        current = room[current][move]
        print(line_seperator)
        print()

    player_status(current, backpack, room)

    if len(backpack) == 6:
        print("Congrats, it was a tough battle but you defeated Principal X")
    else:  # FIXME: BUG - mismatched quotes, 6 - len(backpack) never executes
        # Fix: print("You put up a good fight, but you lose. You missed", 6 - len(backpack), "items")
        print(
            "You put up a good fight, but You lose, you missed', 6 - len(backpack), 'item"
        )


main()
