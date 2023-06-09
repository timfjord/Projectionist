import os
from collections import OrderedDict
from unittest.mock import DEFAULT, Mock, call, patch

from Projectionist.plugin.errors import Error
from Projectionist.plugin.root import Root
from Projectionist.plugin.storage import Storage
from Projectionist.tests import FIXTURES_PATH, SublimeWindowTestCase


class ProjectionTestCase(SublimeWindowTestCase):
    settings = {
        "heuristic_projections": {
            "folder2/file2.py": {
                "folder2/file2.py": {
                    "alternate": "folder3/file3.py",
                },
            },
            "folder5/file5/py": {
                "folder5/file5.py": {
                    "alternate": "folder6/file6.py",
                },
            },
        },
        "builtin_heuristic_projections": {
            "folder1/file1.py": {
                "folder1/file1.py": {
                    "alternate": "folder2/file2.py",
                },
            },
            "folder4/file4/py": {
                "folder4/file4.py": {
                    "alternate": "folder5/file5.py",
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

    def test_get_builtin_projections_includes_only_matched(self):
        self.assertEqual(
            self.storage.get_builtin_projections(),
            OrderedDict(
                (("folder1/file1.py", {"alternate": "folder2/file2.py"}),),
            ),
        )

    def test_get_global_projections_includes_only_matched(self):
        self.assertEqual(
            self.storage.get_global_projections(),
            OrderedDict(
                (("folder2/file2.py", {"alternate": "folder3/file3.py"}),),
            ),
        )

    def test_get_file_projections(self):
        self.assertEqual(
            self.storage.get_file_projections(),
            {"file*.py": {"alternate": "alternate_file{}.py"}},
        )

    def test_get_file_projections_no_projections_json_file(self):
        self.storage.root = Root(FIXTURES_PATH)

        self.assertEqual(
            self.storage.get_file_projections(),
            {},
        )

    def test_get_projections_invalid_lookup_order_item(self):
        self.setSettings({"lookup_order": ["invalid"]})

        with self.assertRaises(Error, msg="Invalid lookup name: 'invalid'"):
            self.storage.get_projections()

    def test_get_projections_lookup_order(self):
        self.setSettings({"lookup_order": ["builtin", "global", "file", "local"]})

        with patch.multiple(
            self.storage,
            get_builtin_projections=DEFAULT,
            get_global_projections=DEFAULT,
            get_file_projections=DEFAULT,
            get_local_projections=DEFAULT,
        ) as mocks:
            manager = Mock()
            manager.attach_mock(
                mocks["get_builtin_projections"], "get_builtin_projections"
            )
            manager.attach_mock(
                mocks["get_global_projections"], "get_global_projections"
            )
            manager.attach_mock(mocks["get_file_projections"], "get_file_projections")
            manager.attach_mock(mocks["get_local_projections"], "get_local_projections")

            self.storage.get_projections()

            self.assertTrue(
                # call `get_local_projections` first
                manager.mock_calls.index(call.get_local_projections())
                # then `get_file_projections` first
                < manager.mock_calls.index(call.get_file_projections())
                # then `get_global_projections` first
                < manager.mock_calls.index(call.get_global_projections())
                # and finally `get_builtin_projections` first
                < manager.mock_calls.index(call.get_builtin_projections())
            )
