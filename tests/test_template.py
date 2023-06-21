import unittest

from Projectionist.plugin import errors
from Projectionist.plugin.template import Template


class TemplateTestCase(unittest.TestCase):
    def setUp(self):
        self.template = Template("source")

    def test_apply_transformation(self):
        self.assertEqual(
            self.template.apply_transformation("dot", "foo/bar"),
            "foo.bar",
        )

    def test_apply_transformation_with_spaces(self):
        self.assertEqual(
            self.template.apply_transformation("  dot  ", "foo/bar"),
            "foo.bar",
        )

    def test_apply_transformation_no_filter(self):
        self.assertEqual(
            self.template.apply_transformation("", "foo/bar"),
            "foo/bar",
        )

    def test_apply_transformation_invalid_filter(self):
        with self.assertRaises(errors.Error):
            self.assertEqual(
                self.template.apply_transformation("__unKn0wn__", "foo/bar"),
                "foo/bar",
            )

    def test_apply_transformation_dynamic_transformations(self):
        template = Template("source", transformations={"dosmth": lambda x: x + " bar"})
        self.assertEqual(
            template.apply_transformation("dosmth", "foo"),
            "foo bar",
        )

    def test_apply_transformation_override_default(self):
        template = Template("source", transformations={"dot": lambda x: x + "."})
        self.assertEqual(
            template.apply_transformation("dot", "foo"),
            "foo.",
        )

    def test_apply_transformations(self):
        self.assertEqual(
            self.template.apply_transformations(["dot", "uppercase"], "foo/bar"),
            "FOO.BAR",
        )

    def test_apply_transformations_with_spaces(self):
        self.assertEqual(
            self.template.apply_transformations(
                ["  dot  ", "  uppercase  "], "foo/bar"
            ),
            "FOO.BAR",
        )

    def test_apply_transformations_no_transformations(self):
        self.assertEqual(
            self.template.apply_transformations([], "foo"),
            "foo",
        )

    def test_apply_transformations_post_split(self):
        self.assertEqual(
            self.template.apply_transformations([""], "foo"),
            "foo",
        )

    def test_apply_transformations_invalid_filter(self):
        with self.assertRaises(errors.Error):
            self.assertEqual(
                self.template.apply_transformations(["dot", "__unKn0wn__"], "foo/bar"),
                "foo/bar",
            )

    def test_render(self):
        self.assertEqual(
            Template("foo: {}").render("bar/baz.py"),
            "foo: bar/baz.py",
        )

    def test_render_multiple(self):
        self.assertEqual(
            Template("foo: {}, {}, {}").render("bar/baz.py"),
            "foo: bar/baz.py, bar/baz.py, bar/baz.py",
        )

    def test_render_filter(self):
        self.assertEqual(
            Template("foo: {dot|uppercase}").render("bar/baz.py"),
            "foo: BAR.BAZ.PY",
        )

    def test_render_filter_with_spaces(self):
        self.assertEqual(
            Template("foo: { dot | uppercase }").render("bar/baz.py"),
            "foo: BAR.BAZ.PY",
        )

    def test_render_multiple_filter(self):
        self.assertEqual(
            Template("foo: {underscore}, {dot|uppercase}").render("bar/baz.py"),
            "foo: bar_baz.py, BAR.BAZ.PY",
        )
