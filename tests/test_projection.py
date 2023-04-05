import unittest
from types import GeneratorType

from Projectionist.plugin.projection import MatchedProjection, Projection
from Projectionist.plugin.root import Root


class ProjectionTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Root("~")

    def test_init_options_not_dict(self):
        with self.assertRaises(TypeError):
            Projection("foo", "bar")

    def test_init_single_globstar_replacement(self):
        self.assertEqual(
            Projection("*", {}).pattern,
            "**/*",
        )

        self.assertEqual(
            Projection("foo/*", {}).pattern,
            "foo/**/*",
        )

        self.assertEqual(
            Projection("foo/**/*", {}).pattern,
            "foo/**/*",
        )

        self.assertEqual(
            Projection("foo/**/bar/*", {}).pattern,
            "foo/**/bar/*",
        )

    def test_alternate(self):
        self.assertEqual(
            Projection("*", {}).alternate,
            (),
        )

        self.assertEqual(
            Projection("*", {"alternate": "foo"}).alternate,
            ("foo",),
        )

        self.assertEqual(
            Projection("*", {"alternate": ["foo", "bar"]}).alternate,
            ["foo", "bar"],
        )

    def test_template(self):
        self.assertEqual(
            Projection("*", {}).template,
            "",
        )

        self.assertEqual(
            Projection("*", {"template": "foo"}).template,
            "foo",
        )

        self.assertEqual(
            Projection("*", {"template": ["foo", "bar"]}).template,
            "foo\nbar",
        )

    def test_match(self):
        projection = Projection("*", {})
        match = projection.match(self.root.file("foo.py"))

        self.assertIsInstance(match, MatchedProjection)
        self.assertEqual(match.root, self.root)
        self.assertEqual(match.projection, projection)
        self.assertEqual(
            match.match,
            "foo.py",
        )

        self.assertEqual(
            Projection("**/*.py", {}).match(self.root.file("foo.py")).match,
            "foo",
        )

        self.assertEqual(
            Projection("foo/**/*.py", {})
            .match(self.root.file("foo", "bar", "baz.py"))
            .match,
            "bar/baz",
        )

        self.assertEqual(
            Projection("foo/**/baz/*.py", {})
            .match(self.root.file("foo", "bar", "baz", "qux.py"))
            .match,
            "bar/qux",
        )

        self.assertEqual(
            Projection("foo/**/baz/*.py", {})
            .match(self.root.file("foo", "bar", "baz", "baz", "baz", "baz.py"))
            .match,
            "bar/baz/baz/baz",
        )

        self.assertEqual(
            Projection("*", {}).match(self.root.file("/")).match,
            "/",
        )

    def test_match_no_globstar(self):
        self.assertEqual(
            Projection("foo.py", {}).match(self.root.file("foo.py")).match,
            "",
        )


class TestMatchedProjection(unittest.TestCase):
    def setUp(self):
        self.root = Root("~")

    def test_alternate(self):
        alternate = MatchedProjection(
            self.root,
            Projection("foo/**/baz/*.py", {"alternate": ["dir1/{}.py", "dir2/{}.py"]}),
            "bar/qux",
        ).alternate

        self.assertIsInstance(alternate, GeneratorType)
        self.assertEqual(
            list(alternate),
            [
                self.root.file("dir1", "bar", "qux.py"),
                self.root.file("dir2", "bar", "qux.py"),
            ],
        )

    def test_template(self):
        template = MatchedProjection(
            self.root,
            Projection(
                "foo/**/baz/*.py", {"template": ["class {capitalize}:", "    pass"]}
            ),
            "bar/qux",
        ).template
        self.assertEqual(template, "class BarQux:\n    pass")
