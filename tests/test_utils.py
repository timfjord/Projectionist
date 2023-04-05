import unittest
from collections import OrderedDict

from Projectionist.plugin import utils


class UtilsTestCase(unittest.TestCase):
    def test_to_unpackable(self):
        self.assertEqual(
            utils.to_unpackable("foo"),
            ("foo",),
        )

        self.assertEqual(
            utils.to_unpackable(("foo",)),
            ("foo",),
        )

        self.assertEqual(
            utils.to_unpackable(["foo"]),
            ["foo"],
        )

    def test_merge(self):
        self.assertEqual(
            utils.merge(
                {"key1": {"foo": 1}, "key2": {"foo": 1, "bar": 2}},
                {"key2": {"bar": 3}, "key3": {"foo": 1}},
            ).items(),
            OrderedDict(
                key1={"foo": 1}, key2={"foo": 1, "bar": 3}, key3={"foo": 1}
            ).items(),
        )

    def test_merge_nested_keys_not_dicts(self):
        with self.assertRaises(TypeError):
            utils.merge(
                {"foo": {"bar": 1}},
                {"baz": "qux"},
            )

        with self.assertRaises(TypeError):
            utils.merge(
                {"foo": "bar"},
                {"foo": {"baz": 1}},
            )

    def test_merge_alternate_key(self):
        self.assertEqual(
            utils.merge(
                {
                    "key": {
                        "alternate": "a1",
                        "prepend_alternate": "smth",
                        "append_alternate": "smth",
                    }
                },
                {
                    "key": {
                        "prepend_alternate": "a0",
                        "append_alternate": "a2",
                    }
                },
            ).items(),
            OrderedDict(key={"alternate": ["a0", "a1", "a2"]}).items(),
        )

    def test_merge_alternate_key_remove_prepend_append(self):
        self.assertEqual(
            utils.merge(
                {
                    "key": {
                        "prepend_alternate": "a1",
                        "append_alternate": "a2",
                    }
                },
                {
                    "key": {
                        "alternate": "alternate",
                    }
                },
            ).items(),
            OrderedDict(key={"alternate": "alternate"}).items(),
        )

    def test_merge_alternate_key_not_array(self):
        self.assertEqual(
            utils.merge(
                {
                    "key": {
                        "alternate": "alternate",
                    }
                },
                {
                    "key": {
                        "key": "value",
                    }
                },
            ).items(),
            OrderedDict(key={"alternate": "alternate", "key": "value"}).items(),
        )

    def test_merge_skip(self):
        self.assertEqual(
            utils.merge(
                {
                    "key": {
                        "alternate": "alternate",
                    }
                },
                {
                    "key": "skip",
                },
            ).items(),
            OrderedDict(key={}).items(),
        )

        self.assertEqual(
            utils.merge(
                {
                    "key": "skip",
                },
                {
                    "key": {
                        "alternate": "alternate",
                    }
                },
            ).items(),
            OrderedDict(key={"alternate": "alternate"}).items(),
        )
