# isort:skip_file

import os

import sublime
from unittesting import DeferrableTestCase

from Projectionist.plugin import cache, settings
from Projectionist.plugin.utils import to_unpackable

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), "fixtures")


class SublimeWindowTestCase(DeferrableTestCase):
    settings = {}
    project_settings = {}

    @classmethod
    def setUpClass(cls):
        sublime.run_command("new_window")
        cls.window = sublime.active_window()
        cls.window.set_project_data(
            {"settings": {settings.PROJECT_SETTINGS_KEY: cls.project_settings}}
        )

        sublime.load_settings("Preferences.sublime-settings").set(
            "close_windows_when_empty", False
        )

        cache.clear()

    @classmethod
    def tearDownClass(cls):
        cls.window.run_command("close_window")

    def setUp(self):
        self._settings = sublime.load_settings(settings.BASE_NAME)
        self._setting_keys = set()

        self.setSettings(self.settings)

    def tearDown(self):
        for key in self._setting_keys:
            self._settings.erase(key)

    def setSettings(self, pairs):
        self._setting_keys |= set(pairs.keys())

        for key, value in pairs.items():
            self._settings.set(key, value)


class SublimeViewTestCase(SublimeWindowTestCase):
    new_file = True

    def setUp(self):
        super().setUp()

        self.view = self.window.new_file() if self.new_file else None

    def focusView(self):
        if not self.view:
            return

        self.window.focus_view(self.view)

    def isViewLoaded(self):
        if not self.view:
            return True

        return not self.view.is_loading()

    def tearDown(self):
        super().tearDown()

        if not self.view:
            return

        self.view.set_scratch(True)
        self.view.close()

    def gotoLine(self, line):
        if not self.view:
            return

        self.focusView()
        self.view.run_command("goto_line", {"line": line})

        return line


class SublimeProjectTestCase(SublimeViewTestCase):
    new_file = False
    folder = None

    _currentFolder = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.folder is None:
            raise ValueError("folder is missing")

        cls._currentFolder = os.path.join(FIXTURES_PATH, *to_unpackable(cls.folder))
        cls.window.set_project_data({"folders": [{"path": cls._currentFolder}]})
