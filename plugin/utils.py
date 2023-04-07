from collections import OrderedDict


def to_unpackable(val):
    return val if isinstance(val, list) or isinstance(val, tuple) else (val,)


def to_list(val, wrap_none=True):
    if not wrap_none and val is None:
        return []

    return val if isinstance(val, list) else [val]


SKIP = "skip"
SPECIAL_KEYS = ("alternate",)


def _merge_nested(dict1, dict2):
    if dict1 == SKIP:
        dict1 = {}

    if dict2 == SKIP:
        return {}

    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError("both arguments must be dicts")

    result = dict(dict1, **dict2)

    for key in SPECIAL_KEYS:
        to_prepend_key = "prepend_" + key
        to_prepend = result.pop(to_prepend_key, None)
        to_append_key = "append_" + key
        to_append = result.pop(to_append_key, None)

        if to_prepend and to_prepend_key in dict2:
            result[key] = to_list(to_prepend) + to_list(
                result.get(key), wrap_none=False
            )

        if to_append and to_append_key in dict2:
            result[key] = to_list(result.get(key), wrap_none=False) + to_list(to_append)

    return result


def merge(dict1, dict2):
    result = OrderedDict(dict2)

    for key, val in dict1.items():
        result[key] = _merge_nested(val, dict2.get(key, {}))

    return result
