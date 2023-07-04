import unittest

from Projectionist.plugin import cache, settings
from Projectionist.plugin.utils import ST3
from Projectionist.tests import SublimeWindowTestCase


class SettingsTestCase(SublimeWindowTestCase):
    def test_unknown(self):
        self.assertIsNone(settings.get("unknown"))

    def test_settings(self):
        self.setSettings({"key.subkey": "value"})

        self.assertEqual(settings.get("key.subkey"), "value")

    def test_passing_an_iterator(self):
        self.setSettings({"key.subkey": "value"})

        self.assertEqual(settings.get(("key", "subkey")), "value")

    def test_default(self):
        self.assertEqual(settings.get("unknown", default="value"), "value")

    def test_typing(self):
        self.setSettings({"key": "value"})

        self.assertEqual(settings.get("key", type=str), "value")
        self.assertIsNone(settings.get("key", type=bool))

    def test_invalid_scope(self):
        self.assertIsNone(settings.get("key", scope="__1nv@Lid__"))


class ProjectSettingsTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data(
            {"settings": {settings.PROJECT_SETTINGS_KEY: {"key": "value2"}}}
        )

    def setUp(self):
        super().setUp()

        self.setSettings({"key": "value1", "another_key": "value3"})

    def test_get(self):
        self.assertEqual(settings.get("key"), "value2")

    def test_get_fallback(self):
        self.assertEqual(settings.get("another_key"), "value3")

    def test_get_project_scope(self):
        self.assertIsNone(settings.get("another_key", scope="project"))

    def test_get_global_scope(self):
        self.assertEqual(settings.get("key", scope="global"), "value1")

    @unittest.skipIf(
        ST3,
        "It looks like setting project data during a test is not supported in Sublime Text 3",
    )
    def test_project_settings_cache(self):
        self.window.set_project_data(
            {"settings": {settings.PROJECT_SETTINGS_KEY: {"key": "value3"}}}
        )
        self.assertEqual(settings.get("key"), "value2")

        cache.clear()
        self.assertEqual(settings.get("key"), "value3")


class InvalidProjectDataTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data("invalid_data")

    def test_get(self):
        self.setSettings({"key": "value"})

        self.assertEqual(settings.get("key"), "value")


class InvalidProjectSettingsTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data({"settings": "settings"})

    def test_get(self):
        self.setSettings({"key": "value"})

        self.assertEqual(settings.get("key"), "value")


class InvalidProjectPluginSettingsTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data(
            {"settings": {settings.PROJECT_SETTINGS_KEY: "settings"}}
        )

    def test_get(self):
        self.setSettings({"key": "value"})

        self.assertEqual(settings.get("key"), "value")
