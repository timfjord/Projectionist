import os
from unittest.mock import patch

from Projectionist.plugin import cache
from Projectionist.plugin.errors import Error
from Projectionist.plugin.projection import Projection
from Projectionist.plugin.root import Root
from Projectionist.plugin.storage import Storage
from Projectionist.tests import FIXTURES_PATH, SublimeWindowTestCase


class ProjectionTestCase(SublimeWindowTestCase):
    settings = {
        "lookup_order": ["builtin", "global", "file", "local"],
        "heuristic_projections": {
            "folder2/file2.py&!folder5/file5.py": {
                "folder2/file2.py": {
                    "alternate": "folder3/file3.py",
                },
            },
            "folder6/file6/py": {
                "folder6/file6.py": {
                    "alternate": "folder6/file6.py",
                },
            },
        },
        "builtin_heuristic_projections": {
            "folder1/file1.py&folder4/file4.py": {
                "folder1/file1.py": {
                    "alternate": "folder2/file2.py",
                },
            },
            "folder5/file5/py": {
                "folder5/file5.py": {
                    "alternate": "folder6/file6.py",
                },
            },
        },
    }
    project_settings = {
        "projections": {
            "folder3/file3.py": {
                "alternate": "folder1/file1.py",
            },
        },
    }

    def setUp(self):
        super().setUp()

        root = Root(os.path.join(FIXTURES_PATH, "dummy"))
        self.storage = Storage(root)

    # this test should go first, otherwise other tests will fail
    def test_get_projections_1_invalid_lookup_order_item(self):
        self.setSettings({"lookup_order": ["invalid"]})

        with self.assertRaises(Error, msg="Invalid lookup name: 'invalid'"):
            self.storage.get_projections()

    def test_get_projections_2(self):
        projections = self.storage.get_projections()

        self.assertEqual(len(projections), 4)
        self.assertIsInstance(projections[0], Projection)
        # as per the lookup order defined on line 12
        # a built-in projection goes first
        self.assertEqual(projections[0].pattern, "folder1/file1.py")
        self.assertIsInstance(projections[1], Projection)
        # then a global projection
        self.assertEqual(projections[1].pattern, "folder2/file2.py")
        self.assertIsInstance(projections[2], Projection)
        # then a file projection
        self.assertEqual(projections[2].pattern, "folder4/file4.py")
        self.assertIsInstance(projections[3], Projection)
        # and finally a local projection
        self.assertEqual(projections[3].pattern, "folder3/file3.py")

    def test_get_projections_3_cache(self):
        cache.clear()
        self.storage.get_projections()

        with patch.object(self.storage, "_get_builtin_projections", return_value={}):
            projections = self.storage.get_projections()

            self.assertEqual(len(projections), 4)
