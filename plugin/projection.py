import re
from functools import lru_cache

from . import utils
from .template import Template


class Projection:
    def __init__(self, pattern, options):
        if not isinstance(options, dict):
            raise TypeError("options must be a dict")

        self.pattern = (
            re.sub(r"\*", "**/*", pattern)
            # TODO: check me again
            if re.match(r"^[^*{}]*\*[^*{}]*$", pattern)
            else pattern
        )
        self.options = options

    @property
    @lru_cache(maxsize=None)
    def alternate(self):
        return utils.to_unpackable(self.options.get("alternate", ()))

    @property
    @lru_cache(maxsize=None)
    def template(self):
        return "\n".join(
            utils.to_unpackable(self.options.get("template", "")),
        )

    def match(self, file):
        path = file.relpath.replace("\\", "/")

        if self.pattern == path:
            return MatchedProjection(file.root, self, "")

        try:
            prefix, infix, suffix = re.split(r"\*\*?", self.pattern)
        except ValueError:
            return None

        if not path.startswith(prefix) or not path.endswith(suffix):
            return None

        to = -len(suffix) or None
        match = path[len(prefix) : to]

        if infix != "/":
            clean = match.replace(infix, "/", 1)

            if clean != match:
                match = clean

        return MatchedProjection(file.root, self, match)

    def find_alternate_file(self, path):
        if not bool(self.alternate):
            return None

        match = self.match(path)

        return match.alternate if match else None

    def find_template(self, path):
        if not bool(self.template):
            return None

        match = self.match(path)

        return match.template if match else None


class MatchedProjection:
    def __init__(self, root, projection, match):
        self.root = root
        self.projection = projection
        self.match = match

    @property
    def alternate(self):
        return (
            self.root.file(*Template(alternate).render(self.match).split("/"))
            for alternate in self.projection.alternate
        )

    @property
    def template(self):
        return Template(self.projection.template).render(self.match)
