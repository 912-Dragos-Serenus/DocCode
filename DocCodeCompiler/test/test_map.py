from unittest import TestCase
from super_hash_map.map import SuperHashMap


class TestSuperHashMap(TestCase):
    def test_put(self):
        data = SuperHashMap()
        for i in range(100):
            self.assertFalse(data.has(i))

        for i in range(100):
            data.put(i, i)
        for i in range(100):
            self.assertTrue(data.has(i))

        for i in range(100):
            data.put(i, i * 2)
        for i in range(100):
            self.assertEqual(data.get(i).key, i)
            self.assertEqual(data.get(i).value, i * 2)

    def test_has(self):
        data = SuperHashMap()
        for i in range(1000):
            self.assertFalse(data.has(i))
        for i in range(1000):
            data.put(i, i)
        for i in range(1000):
            self.assertTrue(data.has(i))
        for i in range(1001, 2000):
            self.assertFalse(data.has(i))

    def test_get(self):
        data = SuperHashMap()
        for i in range(1000):
            data.put(i, i)
        for i in range(1000):
            self.assertEqual(data.get(i).key, i)
            self.assertEqual(data.get(i).value, i)
