import unittest
from snhu_apocalypse.room import Room
from snhu_apocalypse.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.library = Room("Library", {"N": "Gym"})
        self.gym = Room("Gym", {"S": "Library"})
        self.library.set_exits({"N": self.gym})
        self.gym.set_exits({"S": self.library})
        self.player = Player(self.library)

    def test_initial_room(self):
        self.assertEqual(self.player.current_room, self.library)

    def test_initial_inventory_empty(self):
        self.assertEqual(self.player.inventory, [])

    def test_add_to_inventory(self):
        self.player.add_to_inventory("Baseball bat")
        self.assertIn("Baseball bat", self.player.inventory)

    def test_move_valid_direction(self):
        self.player.move("N")
        self.assertEqual(self.player.current_room, self.gym)

    def test_move_valid_returns_true(self):
        result = self.player.move("N")
        self.assertTrue(result)

    def test_move_invalid_direction(self):
        self.player.move("E")
        self.assertEqual(self.player.current_room, self.library)

    def test_move_invalid_returns_false(self):
        result = self.player.move("E")
        self.assertFalse(result)

    def test_move_back_and_forth(self):
        self.player.move("N")
        self.player.move("S")
        self.assertEqual(self.player.current_room, self.library)

    def test_inventory_not_shared_between_instances(self):
        other = Player(self.library)
        self.player.add_to_inventory("Radio")
        self.assertNotIn("Radio", other.inventory)


if __name__ == "__main__":
    unittest.main()
