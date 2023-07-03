import os
from unittest.mock import patch

from Projectionist.plugin import cache
from Projectionist.plugin.errors import Error
from Projectionist.plugin.projection import Projection
from Projectionist.plugin.root import Root
from Projectionist.plugin.storage import Storage
from Projectionist.tests import FIXTURES_PATH, SublimeWindowTestCase

_BUILTIN_PROJECTIONS = {
    "lang1": {
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
    "lang2": {
        "folder1/file1.py": {
            "folder1/file1.py": {
                "alternate": "folder3/file3.py",
            },
        },
    },
}


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
        "builtin_heuristic_projections": ["lang1"],
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

        cache.clear()

    def _get_projections(self):
        with patch(
            "Projectionist.plugin.storage.BUILTIN_PROJECTIONS", _BUILTIN_PROJECTIONS
        ):
            return self.storage.get_projections()

    def test_get_projections(self):
        projections = self._get_projections()

        self.assertEqual(len(projections), 4)
        self.assertIsInstance(projections[0], Projection)
        # as per the lookup order defined on line 36
        # built-in projections goes first
        self.assertEqual(projections[0].pattern, "folder1/file1.py")
        self.assertIsInstance(projections[1], Projection)
        # then global projections
        self.assertEqual(projections[1].pattern, "folder2/file2.py")
        self.assertIsInstance(projections[2], Projection)
        # then file projections
        self.assertEqual(projections[2].pattern, "folder4/file4.py")
        self.assertIsInstance(projections[3], Projection)
        # and finally local projections
        self.assertEqual(projections[3].pattern, "folder3/file3.py")

    def test_get_projections_cache(self):
        projections = self._get_projections()

        with patch.object(self.storage, "_get_builtin_projections", return_value={}):
            projections = self.storage.get_projections()

            self.assertEqual(len(projections), 4)

    def test_get_projections_invalid_lookup_order_item(self):
        self.setSettings({"lookup_order": ["invalid"]})

        with self.assertRaises(Error, msg="Invalid lookup name: 'invalid'"):
            self._get_projections()

    def test_get_projections_invalid_builtin_heuristic_projections_item(self):
        self.setSettings({"builtin_heuristic_projections": ["invalid"]})

        with self.assertRaises(
            Error, msg="Invalid built-in projection name: 'invalid'"
        ):
            self._get_projections()
