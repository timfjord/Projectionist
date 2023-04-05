import re

from .transformations import apply_chain as apply_transformations


class Template:
    PLACEHOLDER_PATTERN = r"\{(.*?)\}"
    TRANSFORMATIONS_SEPARATOR = "|"

    def __init__(self, source):
        self.source = str(source)

    def render(self, value):
        return re.sub(
            self.PLACEHOLDER_PATTERN,
            lambda m: apply_transformations(
                m.group(1).split(self.TRANSFORMATIONS_SEPARATOR), value
            ),
            self.source,
        )
