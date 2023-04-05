import unittest

from Projectionist.plugin.template import Template


class TemplateTestCase(unittest.TestCase):
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
