import os.path
import unittest

from projectionist import find_alternate_file

from Projectionist.plugin import cache
from Projectionist.plugin.root import Root
from Projectionist.tests import FIXTURES_PATH


class PublicAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache.clear()

    def setUp(self):
        self.root = Root(os.path.join(FIXTURES_PATH, "dummy"))

    def test_find_alternate_file(self):
        exists, alternate = find_alternate_file(
            self.root.path, self.root.file("folder4", "file4.py").path
        )

        self.assertTrue(exists)
        self.assertIsInstance(alternate, str)
        # as per .projections.json
        self.assertEqual(alternate, self.root.file("folder2", "file2.py").path)

    def test_find_alternate_file_non_existing_alternate(self):
        exists, alternate = find_alternate_file(
            self.root.path, self.root.file("folder1", "file1.py").path
        )

        self.assertFalse(exists)
        self.assertIsInstance(alternate, str)
        # as per .projections.json
        self.assertEqual(alternate, self.root.file("folder10", "file10.py").path)

    def test_find_alternate_file_undefined_projection(self):
        exists, alternate = find_alternate_file(
            self.root.path, self.root.file("folder10", "file10.py").path
        )

        self.assertFalse(exists)
        self.assertIsNone(alternate)

    def test_find_alternate_file_errors(self):
        with self.assertRaises(TypeError):
            find_alternate_file(None, None)

        with self.assertRaises(TypeError):
            find_alternate_file(None, "smth")

        with self.assertRaises(TypeError):
            find_alternate_file("smth", None)

        with self.assertRaises(ValueError):
            find_alternate_file(
                self.root.join("subfolder1"), self.root.file("subfolder2", "file2.py")
            )
