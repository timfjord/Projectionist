import re

from . import utils


def dot(value):
    return value.replace("/", ".")


def underscore(value):
    return value.replace("/", "_")


def backslash(value):
    return value.replace("/", "\\")


def colons(value):
    return value.replace("/", "::")


def hyphenate(value):
    return value.replace("_", "-")


def blank(value):
    return re.sub(r"[_-]", " ", value)


def uppercase(value):
    return value.upper()


def camelcase(value):
    return re.sub(r"[_-](.)", lambda m: m.group(1).upper(), value)


def capitalize(value):
    return re.sub(r"(^|/)(.)", lambda m: m.group(1) + m.group(2).upper(), value)


def snakecase(value):
    return utils.replace(
        value,
        (r"([A-Z]+)([A-Z][a-z])", r"\1_\2"),
        (r"([a-z]|\d)([A-Z])", r"\1_\2"),
    ).lower()


def dirname(value):
    return re.sub(r".[^/\\]*$", "", value)


def basename(value):
    return re.sub(r".*[/\\]", "", value)


def singular(value):
    return utils.replace(
        value,
        (r"(?:(?<![Mm]ov)|(?<![aeio]))ies$", "ys"),
        (r"(?<=[rl])ves$", "fs"),
        (r"(?<=nd|rt)ices$", "exs"),
        (r"(?<!s)s$", ""),
        (r"(?:(?<=[nrt]ch)|(?<=tatus)|(?<=lias)|(?<=ss))e$", ""),
    )


def plural(value):
    return (
        utils.replace(
            value,
            (r"(?<![aeio])y$", "ie"),
            (r"(?<=[rl])f$", "ve"),
            (r"(?<=nd|rt)ex$", "ice"),
            (r"([osxz]|[cs]h)$", r"\1e"),
        )
        + "s"
    )


def open(_):
    return "{"


def close(_):
    return "}"


def nothing(_):
    return ""


def vim(value):
    return value
