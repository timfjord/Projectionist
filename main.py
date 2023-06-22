# --- Clear module cache ---
# Clear module cache to force reloading all modules of this package.
# See https://github.com/emmetio/sublime-text-plugin/issues/35
import sys

prefix = __package__ + "."  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
# --- Clear module cache ---

import sublime_plugin  # noqa: E402

from .plugin import Plugin  # noqa: E402


class ProjectionistOpenAlternateCommand(sublime_plugin.TextCommand):
    def run(self, _):
        Plugin(self.view.window()).open_alternate(self.view.file_name())


class ProjectionistOutputProjectionsCommand(sublime_plugin.TextCommand):
    def run(self, _):
        Plugin(self.view.window()).output_projections()


class ProjectionistClearCacheCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        Plugin.clear_cache()


class ProjectionistSidebarOpenAlternateCommand(sublime_plugin.WindowCommand):
    def run(self, files=[], reveal=False):
        if not files:
            return

        Plugin(self.window).open_alternate(files[0], focus=not reveal)
