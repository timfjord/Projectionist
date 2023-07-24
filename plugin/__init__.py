import logging
import time
from functools import partial

import sublime

from . import cache, settings, status
from .errors import handle_errors
from .root import Root
from .storage import Storage
from .utils import ST3

logger = logging.getLogger(__name__)


class Plugin:
    MODE_SIDE_BY_SIDE = "side_by_side"
    FOCUS_VIEW = "view"
    FOCUS_SIDEBAR = "sidebar"
    OPEN_VIEW_TIMEOUT = 3  # seconds
    OPEN_VIEW_WAIT_FOR = 0.2  # 200 ms
    OPEN_VIEW_MAX_ATTEMPTS = int(OPEN_VIEW_TIMEOUT / OPEN_VIEW_WAIT_FOR)

    @staticmethod
    def clear_cache():
        cache.clear()
        logger.info("Cache cleared")

    def __init__(self, window):
        self.window = window

    @property
    def window_folders(self):
        return self.window.folders()

    @handle_errors
    def open_alternate(self, file_name, folders=[], focus=None, mode=None):
        root, file = Root.find(
            folders or self.window_folders,
            file_name,
            settings.get("subprojects", type=list, default=[]),
        )
        storage = Storage(root)
        exists, alternate = storage.find_alternate_file(file)
        suffix = "defined" if alternate is None else "found"

        if (
            not exists
            and alternate is not None
            and settings.get(
                "create_alternate_file_if_missing", type=bool, default=False
            )
            and sublime.ok_cancel_dialog(
                "Do you really want to create '{}'?".format(alternate.relpath), "Create"
            )
        ):
            template = ""

            for projection in storage.get_projections():
                template = projection.find_template(alternate)

                if template is not None:
                    break
            else:
                template = ""

            alternate.create(template)
            exists = True

        if not exists:
            status.update("No alternate file {}".format(suffix))
        else:
            flags = 0
            if mode == self.MODE_SIDE_BY_SIDE and not ST3:
                flags |= sublime.ADD_TO_SELECTION

            view = self.window.open_file(alternate.path, flags=flags)
            if focus == self.FOCUS_VIEW:
                self._on_view_loaded(
                    view,
                    lambda view: self.window.focus_view(view),
                )
            elif focus == self.FOCUS_SIDEBAR:
                self._on_view_loaded(
                    view,
                    lambda _: sublime.set_timeout_async(
                        partial(self.window.run_command, "focus_side_bar"), 100
                    ),
                )

    def output_projections(self):
        storage = Storage(Root(self.window.folders()[0]))

        print("\nProjections for '{}':\n".format(storage.root))

        for projection in storage.get_projections():
            print("  -> {}".format(projection.pattern))
            print("     {}".format(projection.options))

    def _on_view_loaded(self, view, callback):
        def on_load(view, callback):
            i = 0

            while view.is_loading() and i < self.OPEN_VIEW_MAX_ATTEMPTS:
                i += 1
                time.sleep(self.OPEN_VIEW_WAIT_FOR)

            if view.is_loading():
                logger.error(
                    "{} is still loading after {}s".format(view, self.OPEN_VIEW_TIMEOUT)
                )
            else:
                callback(view)

        sublime.set_timeout_async(partial(on_load, view, callback), 0)
