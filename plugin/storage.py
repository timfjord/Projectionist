import json
from collections import OrderedDict

from . import settings
from .builtin_projections import BUILTIN_PROJECTIONS
from .cache import window_cache
from .errors import Error
from .projection import Projection
from .utils import merge

PROJECTIONS_JSON = ".projections.json"


class Storage:
    def __init__(self, root):
        self.root = root
        self.window_cache_key = self.root.path

    def _find_matched_projections(self, settings):
        result = {}

        # the merge function written in a way that the second hash "overrides" the first hash keys,
        # so in order to obey the order of the heuristic projections they should be reversed
        for patterns, config in reversed(tuple(OrderedDict(settings).items())):
            if self.root.contains(patterns):
                result = merge(result, config)

        return result

    def _get_builtin_projections(self):
        result = {}

        for name in self.builtin_heuristic_projections:
            if name in BUILTIN_PROJECTIONS:
                matched_projections = self._find_matched_projections(
                    BUILTIN_PROJECTIONS[name]
                )
                result = dict(result, **matched_projections)
            else:
                raise Error("Invalid built-in projection name: '{}'".format(name))

        return result

    def _get_global_projections(self):
        return self._find_matched_projections(
            settings.get(
                "heuristic_projections", type=dict, default={}, scope="global"
            ),
        )

    def _get_file_projections(self):
        projections_json = self.root.file(PROJECTIONS_JSON)

        if not projections_json.exists():
            return {}

        with open(projections_json.path) as file:
            content = json.load(file)

            return content or {}

    def _get_local_projections(self):
        return settings.get("projections", type=dict, default={}, scope="project")

    @property
    def builtin_heuristic_projections(self):
        return (
            settings.get("builtin_heuristic_projections", type=list, default=[]) or []
        )

    @property
    def lookup_order(self):
        return reversed(settings.get("lookup_order", type=list, default=[]) or [])

    @window_cache("projections")
    def get_projections(self):
        processed = set()
        result = {}

        for type in self.lookup_order:
            if type in processed:
                continue

            prop = "_get_{}_projections".format(type)
            if hasattr(self, prop):
                result = merge(result, getattr(self, prop)())
                processed.add(type)
            else:
                raise Error("Invalid lookup name: '{}'".format(type))

        return [Projection(pattern, options) for pattern, options in result.items()]

    def find_alternate_file(self, file):
        first_match = None

        for projection in self.get_projections():
            alternate_files = projection.get("alternate", file)

            if alternate_files is None:
                continue

            for alternate_file in alternate_files:
                if alternate_file.exists():
                    return True, alternate_file
                elif first_match is None:
                    first_match = alternate_file

        return False, first_match
