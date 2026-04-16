import unittest
from snhu_apocalypse.game import Game
from snhu_apocalypse.constants import RoomName, Item


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_starts_in_library(self):
        self.assertEqual(self.game.get_current_room_name(), RoomName.LIBRARY)

    def test_not_game_over_at_start(self):
        self.assertFalse(self.game.is_game_over())

    def test_move_valid(self):
        self.game.move("N")
        self.assertEqual(self.game.get_current_room_name(), RoomName.GYM)

    def test_move_invalid_returns_false(self):
        result = self.game.move("U")
        self.assertFalse(result)

    def test_move_invalid_stays_in_room(self):
        # Maintenance Room only has W — moving N is invalid
        self.game.move("N")   # Library -> Gym
        self.game.move("E")   # Gym -> Maintenance Room
        self.game.move("N")   # invalid — no N exit
        self.assertEqual(self.game.get_current_room_name(), RoomName.MAINTENANCE_ROOM)

    def test_move_valid_returns_true(self):
        result = self.game.move("N")
        self.assertTrue(result)

    def test_pick_up_item(self):
        self.game.move("N")   # Gym has Baseball bat
        self.assertTrue(self.game.current_room_has_item())
        self.game.pick_up_item()
        self.assertFalse(self.game.current_room_has_item())

    def test_pick_up_returns_true_when_item_present(self):
        self.game.move("N")   # Gym has Baseball bat
        result = self.game.pick_up_item()
        self.assertTrue(result)

    def test_pick_up_returns_false_when_no_item(self):
        # Library has no item
        result = self.game.pick_up_item()
        self.assertFalse(result)

    def test_pick_up_adds_to_inventory(self):
        self.game.move("N")
        self.game.pick_up_item()
        self.assertIn(Item.BASEBALL_BAT, self.game.get_inventory())

    def test_pick_up_empty_room_does_not_change_inventory(self):
        before = self.game.get_inventory()
        self.game.pick_up_item()  # Library has no item
        self.assertEqual(self.game.get_inventory(), before)

    def test_get_inventory_returns_copy(self):
        inv = self.game.get_inventory()
        inv.append("hacked")
        self.assertNotIn("hacked", self.game.get_inventory())

    def test_win_condition(self):
        # Collect all 6 items then reach the Exit
        steps = [
            ("W", False), (None, True),   # Science Lab — Chemical
            ("E", False), ("N", False), (None, True),  # Gym — Baseball bat
            ("E", False), (None, True),   # Maintenance Room — Glove
            ("W", False), ("S", False), ("S", False), (None, True),  # Cafeteria — Apron
            ("E", False), (None, True),   # Health Center — Bandages
            ("W", False), ("N", False), ("E", False), (None, True),  # Security Room — Radio
            ("N", False),                 # Exit
        ]
        for move, pickup in steps:
            if move:
                self.game.move(move)
            if pickup:
                self.game.pick_up_item()
        self.assertTrue(self.game.is_game_over())
        result = self.game.check_win_lose()
        self.assertIn("defeat", result)

    def test_lose_condition(self):
        # Go straight to Exit without collecting items
        self.game.move("E")   # Security Room
        self.game.move("N")   # Exit
        self.assertTrue(self.game.is_game_over())
        result = self.game.check_win_lose()
        self.assertIn("lose", result)

    def test_reset(self):
        self.game.move("N")
        self.game.reset()
        self.assertEqual(self.game.get_current_room_name(), RoomName.LIBRARY)
        self.assertEqual(self.game.get_inventory(), [])

    def test_player_status_contains_room_name(self):
        status = self.game.player_status()
        self.assertIn(RoomName.LIBRARY, status)

    def test_player_status_at_exit(self):
        self.game.move("E")
        self.game.move("N")
        status = self.game.player_status()
        self.assertIn("Principal X", status)

    def test_game_instructions_contains_item_count(self):
        instructions = self.game.game_instructions()
        self.assertIn(str(self.game.total_items), instructions)


if __name__ == "__main__":
    unittest.main()
