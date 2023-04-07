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

    def test_to_list(self):
        self.assertEqual(
            utils.to_list("foo"),
            ["foo"],
        )

        self.assertEqual(
            utils.to_list(["foo"]),
            ["foo"],
        )

        self.assertEqual(
            utils.to_list(None),
            [None],
        )

        self.assertEqual(
            utils.to_list(None, wrap_none=False),
            [],
        )

    def test_merge(self):
        self.assertEqual(
            utils.merge(
                OrderedDict((("key1", {"foo": 1}), ("key2", {"foo": 1, "bar": 2}))),
                OrderedDict((("key2", {"bar": 3}), ("key3", {"foo": 1}))),
            ),
            OrderedDict(
                (
                    ("key2", {"foo": 1, "bar": 3}),
                    ("key3", {"foo": 1}),
                    ("key1", {"foo": 1}),
                )
            ),
        )

    def test_merge_nested_keys_not_dicts(self):
        self.assertEqual(
            utils.merge(
                {"foo": {"bar": 1}},
                {"baz": "quux"},
            ),
            OrderedDict(
                (
                    ("baz", "quux"),
                    ("foo", {"bar": 1}),
                )
            ),
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
            ),
            OrderedDict((("key", {"alternate": ["a0", "a1", "a2"]}),)),
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
            ),
            OrderedDict((("key", {"alternate": "alternate"}),)),
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
            ),
            OrderedDict((("key", {"alternate": "alternate", "key": "value"}),)),
        )

    def test_merge_alternate_key_not_present(self):
        self.assertEqual(
            utils.merge(
                {"key": {}},
                {
                    "key": {
                        "prepend_alternate": "a1",
                        "append_alternate": "a2",
                    }
                },
            ),
            OrderedDict((("key", {"alternate": ["a1", "a2"]}),)),
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
            ),
            OrderedDict((("key", {}),)),
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
            ),
            OrderedDict((("key", {"alternate": "alternate"}),)),
        )
