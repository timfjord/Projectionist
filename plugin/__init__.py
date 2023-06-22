import logging
from functools import partial

import sublime

from . import cache, settings, status
from .errors import handle_errors
from .root import Root
from .storage import Storage

logger = logging.getLogger(__name__)


class Plugin:
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
    def open_alternate(self, file_name, folders=[], focus=None):
        root, file = Root.find(
            folders or self.window_folders,
            file_name,
            settings.get("subprojects", type=list, default=[]),
        )
        storage = Storage(root)
        to_open = to_create = None

        for projection in storage.get_projections():
            alternate_files = projection.find_alternate_file(file)

            if alternate_files is None:
                continue

            for alternate_file in alternate_files:
                if alternate_file.exists():
                    to_open = alternate_file
                    break
                elif to_create is None:
                    to_create = alternate_file
            else:
                continue

            break  # this will be executing, only when the loop above breaks

        if (
            to_open is None
            and to_create is not None
            and settings.get(
                "create_alternate_file_if_missing", type=bool, default=False
            )
            and sublime.ok_cancel_dialog(
                "Do you really want to create '{}'?".format(to_create.relpath), "Create"
            )
        ):
            template = ""

            for projection in storage.get_projections():
                template = projection.find_template(to_create)

                if template is not None:
                    break
            else:
                template = ""

            to_create.create(template)
            to_open = to_create

        if to_open is None:
            status.update("No alternate file defined")
        else:
            view = self.window.open_file(to_open.path)
            if focus is True:
                sublime.set_timeout(partial(self._focus_on_view, view), 0)

    def output_projections(self):
        storage = Storage(Root(self.window.folders()[0]))

        print("\nProjections for '{}':\n".format(storage.root))

        for projection in storage.get_projections():
            print("  -> {}".format(projection.pattern))
            print("     {}".format(projection.options))

    def _focus_on_view(self, view):
        while view.is_loading():
            pass
        self.window.focus_view(view)
