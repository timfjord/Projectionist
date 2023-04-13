import re
from functools import reduce

from . import transformations
from .errors import Error


class Template:
    PLACEHOLDER_PATTERN = r"\{([^\{\}]*)\}"
    TRANSFORMATIONS_SEPARATOR = "|"
    DEFAULT_TRANSFORMATIONS = {
        "dot": transformations.dot,
        "underscore": transformations.underscore,
        "backslash": transformations.backslash,
        "colons": transformations.colons,
        "hyphenate": transformations.hyphenate,
        "blank": transformations.blank,
        "uppercase": transformations.uppercase,
        "camelcase": transformations.camelcase,
        "capitalize": transformations.capitalize,
        "snakecase": transformations.snakecase,
        "dirname": transformations.dirname,
        "basename": transformations.basename,
        "singular": transformations.singular,
        "plural": transformations.plural,
        "open": transformations.open,
        "close": transformations.close,
        "nothing": transformations.nothing,
        "vim": transformations.vim,
    }

    def __init__(self, source, transformations={}):
        self.source = str(source)
        self.transformations = dict(self.DEFAULT_TRANSFORMATIONS, **transformations)

    def apply_transformation(self, name, value):
        if not bool(name):
            return value

        name = str(name).strip()

        try:
            return self.transformations[name](value)
        except KeyError:
            raise Error("Unknown transformation: '{}'".format(name))

    def apply_transformations(self, transformations, value):
        return reduce(
            lambda v, f: self.apply_transformation(f, v), transformations, value
        )

    def render(self, value):
        return re.sub(
            self.PLACEHOLDER_PATTERN,
            lambda m: self.apply_transformations(
                m.group(1).split(self.TRANSFORMATIONS_SEPARATOR), value
            ),
            self.source,
        )
