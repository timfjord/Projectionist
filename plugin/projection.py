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
            return MatchedProjection(file, self, "")

        try:
            prefix, infix, suffix = re.split(r"\*\*?", self.pattern)
        except ValueError:
            return None

        if not path.startswith(prefix) or not path.endswith(suffix):
            return None

        to = -len(suffix) or None
        match = path[len(prefix) : to]

        if infix != "/":
            clean = "/{}".format(match).replace(infix, "/", 1)[1:]

            if clean != match:
                match = clean

        return MatchedProjection(file, self, match)

    def get(self, type, file):
        if not bool(getattr(self, type)):
            return None

        match = self.match(file)

        return getattr(match, type) if match else None


class MatchedProjection:
    def __init__(self, file, projection, match):
        self.file = file
        self.projection = projection
        self.match = match

    def render_template(self, source):
        return Template(
            source,
            {
                "file": lambda _: self.file.path,
                "project": lambda _: self.file.root.path,
            },
        ).render(self.match)

    @property
    def alternate(self):
        return (
            self.file.root.file(*self.render_template(alternate).split("/"))
            for alternate in self.projection.alternate
        )

    @property
    def template(self):
        return self.render_template(self.projection.template)
