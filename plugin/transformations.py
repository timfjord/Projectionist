import re
from functools import reduce

from .errors import Error


def apply(name, value):
    if not bool(name):
        return value

    name = str(name).strip()

    try:
        return globals()["{}_transformation".format(name)](value)
    except KeyError:
        raise Error("Unknown transformation: '{}'".format(name))


def apply_chain(transformations, value):
    return reduce(lambda v, f: apply(f, v), transformations, value)


def dot_transformation(value):
    return value.replace("/", ".")


def underscore_transformation(value):
    return value.replace("/", "_")


def backslash_transformation(value):
    return value.replace("/", "\\")


def colons_transformation(value):
    return value.replace("/", "::")


def hyphenate_transformation(value):
    return value.replace("_", "-")


def blank_transformation(value):
    return re.sub(r"[_-]", " ", value)


def uppercase_transformation(value):
    return value.upper()


def camelcase_transformation(value):
    return re.sub(r"[_-](.)", lambda m: m.group(1).upper(), value)


# function! g:projectionist_transformations.capitalize(input, o) abort
#   return substitute(a:input, '\%(^\|/\)\zs\(.\)', '\u\1', 'g')
# endfunction


def capitalize_transformation(value):
    return re.sub(r"(?:^|/)(.)", lambda m: m.group(1).upper(), value)


# function! g:projectionist_transformations.snakecase(input, o) abort
#   let str = a:input
#   let str = substitute(str, '\v(\u+)(\u\l)', '\1_\2', 'g')
#   let str = substitute(str, '\v(\l|\d)(\u)', '\1_\2', 'g')
#   let str = tolower(str)
#   return str
# endfunction


def snakecase_transformation(value):
    return re.sub(
        r"(\u+)(\u\l)",
        r"\1_\2",
        re.sub(
            r"(\l|\d)(\u)",
            r"\1_\2",
            value,
        ),
    ).lower()


# function! g:projectionist_transformations.dirname(input, o) abort
#   return substitute(a:input, '.[^'.projectionist#slash().'/]*$', '', '')
# endfunction


def dirname_transformation(value):
    return re.sub(r".[^/]*$", "", value)


# function! g:projectionist_transformations.basename(input, o) abort
#   return substitute(a:input, '.*['.projectionist#slash().'/]', '', '')
# endfunction


def basename_transformation(value):
    return re.sub(r".*/", "", value)


# function! g:projectionist_transformations.singular(input, o) abort
#   let input = a:input
#   let input = s:sub(input, '%([Mm]ov|[aeio])@<!ies$', 'ys')
#   let input = s:sub(input, '[rl]@<=ves$', 'fs')
#   let input = s:sub(input, '%(nd|rt)@<=ices$', 'exs')
#   let input = s:sub(input, 's@<!s$', '')
#   let input = s:sub(input, '%([nrt]ch|tatus|lias|ss)@<=e$', '')
#   return input
# endfunction


def singular_transformation(value):
    return re.sub(r"([Mm]ov|[aeio])@<!ies$", "ys", re.sub(r"[rl]@<=ves$", "fs", value))


# function! g:projectionist_transformations.plural(input, o) abort
#   let input = a:input
#   let input = s:sub(input, '[aeio]@<!y$', 'ie')
#   let input = s:sub(input, '[rl]@<=f$', 've')
#   let input = s:sub(input, '%(nd|rt)@<=ex$', 'ice')
#   let input = s:sub(input, '%([osxz]|[cs]h)$', '&e')
#   let input .= 's'
#   return input
# endfunction


def plural_transformation(value):
    return re.sub(r"[aeio]@<!y$", "ie", re.sub(r"[rl]@<=f$", "ve", value))


def open_transformation(value):
    return "{"


def close_transformation(value):
    return "}"


def nothing_transformation(value):
    return ""


def vim_transformation(value):
    return value
