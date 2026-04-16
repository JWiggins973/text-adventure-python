import unittest
from snhu_apocalypse.game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_starts_in_library(self):
        self.assertEqual(self.game.get_current_room_name(), "Library")

    def test_not_game_over_at_start(self):
        self.assertFalse(self.game.is_game_over())

    def test_move_valid(self):
        self.game.move("N")
        self.assertEqual(self.game.get_current_room_name(), "Gym")

    def test_move_invalid_stays_in_room(self):
        # Maintenance Room only has W — moving N is invalid
        self.game.move("N")   # Library -> Gym
        self.game.move("E")   # Gym -> Maintenance Room
        self.game.move("N")   # invalid — no N exit
        self.assertEqual(self.game.get_current_room_name(), "Maintenance Room")

    def test_pick_up_item(self):
        self.game.move("N")  # Gym has Baseball bat
        self.assertTrue(self.game.current_room_has_item())
        self.game.pick_up_item()
        self.assertFalse(self.game.current_room_has_item())

    def test_pick_up_adds_to_inventory(self):
        self.game.move("N")
        self.game.pick_up_item()
        self.assertIn("Baseball bat", self.game.player.inventory)

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
        self.assertEqual(self.game.get_current_room_name(), "Library")
        self.assertEqual(self.game.player.inventory, [])


if __name__ == "__main__":
    unittest.main()
