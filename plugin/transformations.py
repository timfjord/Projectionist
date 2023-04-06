import re


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


# function! g:projectionist_transformations.snakecase(input, o) abort
#   let str = a:input
#   let str = substitute(str, '\v(\u+)(\u\l)', '\1_\2', 'g')
#   let str = substitute(str, '\v(\l|\d)(\u)', '\1_\2', 'g')
#   let str = tolower(str)
#   return str
# endfunction


def snakecase(value):
    return re.sub(
        r"(\u+)(\u\l)",
        r"\1_\2",
        re.sub(
            r"(\l|\d)(\u)",
            r"\1_\2",
            value,
        ),
    ).lower()


def dirname(value):
    return re.sub(r".[^/\\]*$", "", value)


def basename(value):
    return re.sub(r".*[/\\]", "", value)


# function! g:projectionist_transformations.singular(input, o) abort
#   let input = a:input
#   let input = s:sub(input, '%([Mm]ov|[aeio])@<!ies$', 'ys')
#   let input = s:sub(input, '[rl]@<=ves$', 'fs')
#   let input = s:sub(input, '%(nd|rt)@<=ices$', 'exs')
#   let input = s:sub(input, 's@<!s$', '')
#   let input = s:sub(input, '%([nrt]ch|tatus|lias|ss)@<=e$', '')
#   return input
# endfunction


def singular(value):
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


def plural(value):
    return re.sub(r"[aeio]@<!y$", "ie", re.sub(r"[rl]@<=f$", "ve", value))


def open(_):
    return "{"


def close(_):
    return "}"


def nothing(_):
    return ""


def vim(value):
    return value
