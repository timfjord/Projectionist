import json

from . import settings
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

        for patterns, config in settings.items():
            if self.root.contains(patterns):
                result = merge(result, config)

        return result

    def get_builtin_projections(self):
        return self._find_matched_projections(
            settings.get(
                "builtin_heuristic_projections", type=dict, default={}, scope="global"
            ),
        )

    def get_global_projections(self):
        return self._find_matched_projections(
            settings.get(
                "heuristic_projections", type=dict, default={}, scope="global"
            ),
        )

    def get_file_projections(self):
        projections_json = self.root.file(PROJECTIONS_JSON)

        if not projections_json.exists():
            return {}

        with open(projections_json.path) as file:
            content = json.load(file)

            return content or {}

    def get_local_projections(self):
        return settings.get("projections", type=dict, default={}, scope="project")

    @property
    def lookup_order(self):
        return reversed(settings.get("lookup_order", type=list, default=[]) or [])

    def test(self):
        pass

    def get_projections(self):
        processed = set()
        result = {}

        for type in self.lookup_order:
            if type in processed:
                continue

            prop = "get_{}_projections".format(type)
            if hasattr(self, prop):
                result = merge(result, getattr(self, prop)())
                processed.add(type)
            else:
                raise Error("Invalid lookup name: '{}'".format(type))

        return [Projection(pattern, options) for pattern, options in result.items()]