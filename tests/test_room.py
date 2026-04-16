import unittest
from snhu_apocalypse.room import Room


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = Room("Library", {"N": "Gym", "item": "Baseball bat"})

    def test_name(self):
        self.assertEqual(self.room.name, "Library")

    def test_has_item_true(self):
        self.assertTrue(self.room.has_item())

    def test_get_item(self):
        self.assertEqual(self.room.get_item(), "Baseball bat")

    def test_remove_item(self):
        self.room.remove_item()
        self.assertFalse(self.room.has_item())
        self.assertIsNone(self.room.get_item())

    def test_no_item(self):
        room = Room("Empty Room", {"N": "Somewhere"})
        self.assertFalse(room.has_item())

    def test_exits_exclude_item_key(self):
        self.assertNotIn("item", self.room.get_exits())

    def test_set_exits(self):
        other = Room("Gym", {})
        self.room.set_exits({"N": other})
        self.assertEqual(self.room.get_exits()["N"], other)


if __name__ == "__main__":
    unittest.main()
