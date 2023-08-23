# isort:skip_file

import os
import tempfile
import unittest

import sublime

from Projectionist.plugin import errors
from Projectionist.plugin.root import File, Glob, RelativePath, Root
from Projectionist.tests import FIXTURES_PATH

IS_WINDOWS = sublime.platform() == "windows"


DIR = "C:\\st" if IS_WINDOWS else "~"


def path(*parts):
    return os.path.join(DIR, *parts)


class RootTestCase(unittest.TestCase):
    def test_find_handles_invalid_files(self):
        with self.assertRaises(errors.Error):
            Root.find([], None)

    def test_find_handles_empty_folders(self):
        with self.assertRaises(errors.Error):
            Root.find([], path("code", "another_project", "file.py"))

    def test_find_handles_files_outside_the_folder(self):
        with self.assertRaises(errors.Error):
            Root.find(
                [path("code", "project")], path("code", "another_project", "file.py")
            )

    def test_find_returns_the_root_and_the_file(self):
        root_path = path("code", "project")
        file_path = path("code", "project", "file.py")
        root, file = Root.find([root_path], file_path)

        self.assertIsInstance(root, Root)
        self.assertEqual(root.path, root_path)
        self.assertIsInstance(file, File)
        self.assertEqual(file.path, file_path)

    def test_find_tests_the_longest_folders_first(self):
        root_path1 = path("code", "project")
        root_path2 = path("code", "project", "folder")
        file_path = path("code", "project", "folder", "file.py")
        root, file = Root.find([root_path1, root_path2], file_path)

        self.assertEqual(root.path, root_path2)
        self.assertEqual(file.path, file_path)

    def test_find_supports_subprojects(self):
        root_path = path("code", "project")
        subproject1 = os.path.join("folder", "subfolder1")
        subproject2 = ("folder", "subfolder2")
        file_path = path("code", "project", "folder", "subfolder2", "file.py")
        root, file = Root.find([root_path], file_path, [subproject1, subproject2])

        self.assertEqual(
            root.path, os.path.join(root_path, subproject2[0], subproject2[1])
        )
        self.assertEqual(file.path, file_path)

    def test_find_projects_and_subprojects_longest_folder_first(self):
        root_path1 = path("code", "project")
        root_path2 = path("code", "project", "folder", "subfolder1", "subfolder1_1")
        subproject1 = os.path.join("folder", "subfolder1")
        subproject2 = ("folder", "subfolder2")
        file_path = path(
            "code", "project", "folder", "subfolder1", "subfolder1_1", "file.py"
        )
        root, file = Root.find(
            [root_path1, root_path2], file_path, [subproject1, subproject2]
        )

        self.assertEqual(root.path, root_path2)
        self.assertEqual(file.path, file_path)

    def test_str(self):
        root = Root(path("code", "project"))

        self.assertEqual(str(root), root.path)

    def test_repr(self):
        root = Root(path("code", "project"))

        self.assertEqual(repr(root), "Root('{}')".format(root.path))

    def test_eq(self):
        root1 = Root(path("code", "project1"))
        root2 = Root(path("code", "project1"))
        root3 = Root(path("code", "project2"))

        self.assertEqual(root1, root2)
        self.assertNotEqual(root1, root3)
        self.assertNotEqual(root2, root3)

    def test_join_joins_files_to_the_root(self):
        root_path = path("code", "project")
        root = Root(root_path)

        self.assertEqual(
            root.join("folder", "file.py"), os.path.join(root_path, "folder", "file.py")
        )

    def test_relpath_returns_relative_path(self):
        root = Root(path("code", "project"))

        self.assertEqual(root.relpath(path("code", "project", "file.py")), "file.py")

    def test_file_instantiates_a_file_instance(self):
        file = Root(path("code", "project")).file("folder", "file.py")

        self.assertIsInstance(file, File)
        self.assertEqual(file.path, path("code", "project", "folder", "file.py"))

    def test_glob(self):
        root = Root(path("code"))
        glob = root.glob("cucumber", "**", "*.rb")

        self.assertIsInstance(glob, Glob)
        self.assertEqual(glob.pattern, path("code", "cucumber", "**", "*.rb"))

    def test_contains(self):
        root = Root(os.path.join(FIXTURES_PATH, "dummy"))

        self.assertTrue(root.contains("folder1/file1.py"))
        self.assertTrue(root.contains("folder5/file5.py|folder1/file1.py"))
        self.assertTrue(root.contains("folder2/file2.py&folder1/file1.py"))
        self.assertTrue(
            root.contains("folder1/file1.py&folder3/file3.py|folder5/file5.py")
        )

        self.assertFalse(root.contains("folder1/file1.py&folder5/file5.py"))

        self.assertTrue(root.contains("**/*.py"))
        self.assertTrue(root.contains("*.py|folder3/file3.py"))
        self.assertTrue(root.contains("**/*.py&folder3/file3.py"))
        self.assertTrue(root.contains("**/*.rb|**/*.py"))

        self.assertFalse(
            root.contains("**/*.py&__init__.py|**/*_test.py&folder1/__init__.py")
        )

        self.assertTrue(root.contains("!folder1/*.rb"))
        self.assertTrue(root.contains("folder2/*.py&!folder1/*.rb"))


def build_temp_files(tmpfile):
    existing_file = os.path.basename(tmpfile.name)
    root = Root(os.path.dirname(tmpfile.name))
    existing_dir = os.path.basename(root.path)
    subfolder = Root(os.path.dirname(root.path))

    return existing_file, root, existing_dir, subfolder


class RelativePathTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Root(path("code", "project"))

    def test_relative_path_calculation_on_init(self):
        relative_path = RelativePath(self.root, "folder", "file.py")

        self.assertEqual(relative_path.relpath, os.path.join("folder", "file.py"))
        self.assertEqual(
            relative_path.path, path("code", "project", "folder", "file.py")
        )

    def test_str(self):
        relative_path = RelativePath(self.root, "folder", "file.py")

        self.assertEqual(str(relative_path), relative_path.path)

    def test_repr(self):
        relative_path = RelativePath(self.root, "folder", "file.py")

        self.assertEqual(
            repr(relative_path),
            "RelativePath('{}', '{}')".format(
                self.root, os.path.join("folder", "file.py")
            ),
        )

    def test_eq(self):
        path1 = RelativePath(self.root, "folder", "file1.py")
        path2 = RelativePath(self.root, "folder", "file1.py")
        path3 = RelativePath(self.root, "folder", "file2.py")

        self.assertEqual(path1, path2)
        self.assertNotEqual(path1, path3)
        self.assertNotEqual(path2, path3)

    def test_exists_checks_if_path_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file, root, existing_dir, subfolder = build_temp_files(tmpfile)

            self.assertTrue(RelativePath(root, existing_file).exists())
            self.assertFalse(RelativePath(root, "uNkn0wn.py").exists())
            self.assertTrue(RelativePath(subfolder, existing_dir).exists())


class FileTestCase(unittest.TestCase):
    def test_repr(self):
        root = Root(path("code", "project"))
        relative_path = File(root, "folder", "file.py")

        self.assertEqual(
            repr(relative_path),
            "File('{}', '{}')".format(root, os.path.join("folder", "file.py")),
        )

    def test_exists_checks_if_file_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file, root, existing_dir, subfolder = build_temp_files(tmpfile)

            self.assertTrue(File(root, existing_file).exists())
            self.assertFalse(File(root, "uNkn0wn.py").exists())
            self.assertFalse(File(subfolder, existing_dir).exists())

    def test_create(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Root(tmpdir)
            file = root.file("folder", "subfolder", "file.txt")
            file.create("content")

            with open(str(file)) as file:
                self.assertIn("content", file.read())


class GlobTestCase(unittest.TestCase):
    def test_iter(self):
        root = Root(FIXTURES_PATH)
        glob = Glob(root, "dummy", "**", "*.py")
        iter = glob.__iter__()
        items = list(iter)

        self.assertIsInstance(iter, map)
        self.assertIn(root.join("dummy", "folder1", "file1.py"), items)
        self.assertIn(root.join("dummy", "folder2", "file2.py"), items)
        self.assertIn(root.join("dummy", "folder3", "file3.py"), items)
        self.assertTrue(any(glob))
