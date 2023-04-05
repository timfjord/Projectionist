import unittest

from Projectionist.plugin import errors, transformations


class TransformationsTestCase(unittest.TestCase):
    def test_apply(self):
        self.assertEqual(
            transformations.apply("dot", "foo/bar"),
            "foo.bar",
        )

    def test_apply_with_spaces(self):
        self.assertEqual(
            transformations.apply("  dot  ", "foo/bar"),
            "foo.bar",
        )

    def test_apply_no_filter(self):
        self.assertEqual(
            transformations.apply("", "foo/bar"),
            "foo/bar",
        )

    def test_apply_invalid_filter(self):
        with self.assertRaises(errors.Error):
            self.assertEqual(
                transformations.apply("__unKn0wn__", "foo/bar"),
                "foo/bar",
            )

    def test_apply_chain(self):
        self.assertEqual(
            transformations.apply_chain(["dot", "uppercase"], "foo/bar"),
            "FOO.BAR",
        )

    def test_apply_chain_with_spaces(self):
        self.assertEqual(
            transformations.apply_chain(["  dot  ", "  uppercase  "], "foo/bar"),
            "FOO.BAR",
        )

    def test_apply_chain_no_transformations(self):
        self.assertEqual(
            transformations.apply_chain([], "foo"),
            "foo",
        )

    def test_apply_chain_post_split(self):
        self.assertEqual(
            transformations.apply_chain([""], "foo"),
            "foo",
        )

    def test_apply_chain_invalid_filter(self):
        with self.assertRaises(errors.Error):
            self.assertEqual(
                transformations.apply_chain(["dot", "__unKn0wn__"], "foo/bar"),
                "foo/bar",
            )

    def test_dot_transformation(self):
        self.assertEqual(
            transformations.dot_transformation("foo/bar"),
            "foo.bar",
        )

    def test_underscore_transformation(self):
        self.assertEqual(
            transformations.underscore_transformation("foo/bar"),
            "foo_bar",
        )

    def test_backslash_transformation(self):
        self.assertEqual(
            transformations.backslash_transformation("foo/bar"),
            "foo\\bar",
        )

    def test_colons_transformation(self):
        self.assertEqual(
            transformations.colons_transformation("foo/bar"),
            "foo::bar",
        )

    def test_hyphenate_transformation(self):
        self.assertEqual(
            transformations.hyphenate_transformation("foo_bar"),
            "foo-bar",
        )

    def test_blank_transformation(self):
        self.assertEqual(
            transformations.blank_transformation("foo_bar"),
            "foo bar",
        )

    def test_uppercase_transformation(self):
        self.assertEqual(
            transformations.uppercase_transformation("foo/bar"),
            "FOO/BAR",
        )

    def test_camelcase_transformation(self):
        self.assertEqual(
            transformations.camelcase_transformation("foo-bar_baz"),
            "fooBarBaz",
        )

    def test_capitalize_transformation(self):
        self.assertEqual(
            transformations.capitalize_transformation("foo/bar"),
            "FooBar",
        )

    def test_snakecase_transformation(self):
        pass

    def test_dirname_transformation(self):
        self.assertEqual(
            transformations.dirname_transformation("foo/bar/baz"),
            "foo/bar",
        )

    def test_basename_transformation(self):
        self.assertEqual(
            transformations.basename_transformation("foo/bar/baz"),
            "baz",
        )

    def test_singular_transformation(self):
        pass

    def test_plural_transformation(self):
        pass

    def test_open_transformation(self):
        self.assertEqual(
            transformations.open_transformation("foo/bar/baz"),
            "{",
        )

    def test_close_transformation(self):
        self.assertEqual(
            transformations.close_transformation("foo/bar/baz"),
            "}",
        )

    def test_nothing_transformation(self):
        self.assertEqual(
            transformations.nothing_transformation("foo/bar/baz"),
            "",
        )

    def test_vim_transformation(self):
        self.assertEqual(
            transformations.vim_transformation("foo/bar/baz"),
            "foo/bar/baz",
        )
