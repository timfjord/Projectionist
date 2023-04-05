from collections import OrderedDict


def to_unpackable(val):
    return val if isinstance(val, list) or isinstance(val, tuple) else (val,)


def to_list(val):
    return val if isinstance(val, list) else [val]


SKIP = "skip"
SPECIAL_KEYS = ("alternate",)


def _handle_nested(dict1, dict2):
    if dict1 == SKIP:
        dict1 = {}

    if dict2 == SKIP:
        return {}

    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError("both arguments must be dicts")

    result = dict1.copy()

    result = dict(result, **dict2)

    for key in SPECIAL_KEYS:
        to_prepend_key = "prepend_" + key
        to_prepend = result.pop(to_prepend_key, None)
        to_append_key = "append_" + key
        to_append = result.pop(to_append_key, None)

        if key not in result:
            continue

        if to_prepend and to_prepend_key in dict2:
            result[key] = to_list(to_prepend) + to_list(result[key])

        if to_append and to_append_key in dict2:
            result[key] = to_list(result[key]) + to_list(to_append)

    return result


def merge(dict1, dict2):
    result = OrderedDict(dict1)

    for key, val in dict2.items():
        result[key] = _handle_nested(dict1.get(key, {}), val)

    return result
