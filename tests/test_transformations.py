import unittest

from Projectionist.plugin import transformations


class TransformationsTestCase(unittest.TestCase):
    def test_dot(self):
        self.assertEqual(
            transformations.dot("foo/bar"),
            "foo.bar",
        )

    def test_underscore(self):
        self.assertEqual(
            transformations.underscore("foo/bar"),
            "foo_bar",
        )

    def test_backslash(self):
        self.assertEqual(
            transformations.backslash("foo/bar"),
            "foo\\bar",
        )

    def test_colons(self):
        self.assertEqual(
            transformations.colons("foo/bar"),
            "foo::bar",
        )

    def test_hyphenate(self):
        self.assertEqual(
            transformations.hyphenate("foo_bar"),
            "foo-bar",
        )

    def test_blank(self):
        self.assertEqual(
            transformations.blank("foo_bar"),
            "foo bar",
        )

    def test_uppercase(self):
        self.assertEqual(
            transformations.uppercase("foo/bar"),
            "FOO/BAR",
        )

    def test_camelcase(self):
        self.assertEqual(
            transformations.camelcase("foo-bar_baz"),
            "fooBarBaz",
        )

    def test_capitalize(self):
        self.assertEqual(
            transformations.capitalize("foo/bar"),
            "Foo/Bar",
        )

    def test_snakecase(self):
        self.assertEqual(
            transformations.snakecase("FooBar/bazQuux"),
            "foo_bar/baz_quux",
        )

    def test_dirname(self):
        self.assertEqual(
            transformations.dirname("foo/bar/baz"),
            "foo/bar",
        )

        self.assertEqual(
            transformations.dirname("foo\\bar\\baz"),
            "foo\\bar",
        )

    def test_basename(self):
        self.assertEqual(
            transformations.basename("foo/bar/baz"),
            "baz",
        )

        self.assertEqual(
            transformations.basename("foo\\bar\\baz"),
            "baz",
        )

    def test_singular(self):
        self.assertEqual(
            transformations.singular("posts"),
            "post",
        )

        self.assertEqual(
            transformations.singular("babies"),
            "baby",
        )

        self.assertEqual(
            transformations.singular("wolves"),
            "wolf",
        )

        self.assertEqual(
            transformations.singular("indices"),
            "index",
        )

        self.assertEqual(
            transformations.singular("statuses"),
            "status",
        )

    def test_plural(self):
        self.assertEqual(
            transformations.plural("post"),
            "posts",
        )

        self.assertEqual(
            transformations.plural("baby"),
            "babies",
        )

        self.assertEqual(
            transformations.plural("wolf"),
            "wolves",
        )

        self.assertEqual(
            transformations.plural("index"),
            "indices",
        )

        self.assertEqual(
            transformations.plural("status"),
            "statuses",
        )

    def test_open(self):
        self.assertEqual(
            transformations.open("foo/bar/baz"),
            "{",
        )

    def test_close(self):
        self.assertEqual(
            transformations.close("foo/bar/baz"),
            "}",
        )

    def test_nothing(self):
        self.assertEqual(
            transformations.nothing("foo/bar/baz"),
            "",
        )

    def test_vim(self):
        self.assertEqual(
            transformations.vim("foo/bar/baz"),
            "foo/bar/baz",
        )
