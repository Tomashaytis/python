import os
from unittest import TestCase
from find import next_instance
from iterator import InstanceIterator


class TestInstanceIterator(TestCase):

    def setUp(self):
        self.iter = InstanceIterator(os.path.join('dataset1', 'tiger_1107.jpg'))

    def test___iter__(self):
        self.assertEqual(self.iter.__iter__(), self.iter)

    def test___next__(self):
        self.assertEqual(self.iter.__next__(), os.path.join('dataset1', 'tiger_1108.jpg'))
        self.assertRaises(StopIteration, self.iter.__next__)


class TestFind(TestCase):

    def test_next_instance(self):
        self.assertEqual(next_instance(os.path.join('dataset1', 'tiger_1107.jpg')),
                         os.path.join('dataset1', 'tiger_1108.jpg'))
        self.assertIsNone(next_instance(os.path.join('dataset1', 'tiger_1108.jpg')))


if __name__ == "__main__":
    TestCase()
