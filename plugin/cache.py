import functools
from collections import defaultdict

import sublime

_cache = []
_window_cache = defaultdict(dict)


def lru_cache(func):
    func = functools.lru_cache(maxsize=None)(func)
    _cache.append(func)

    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper_cache


def _get_window_id():
    return getattr(sublime.active_window(), "id", None)


def window_cache(key):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            window_id = _get_window_id()
            cache_key = "-".join(
                (
                    key,
                    str(getattr(args[0], "window_cache_key", None))
                    if bool(args)
                    else "",
                )
            )

            if cache_key not in _window_cache[window_id]:
                _window_cache[window_id][cache_key] = func(*args, **kwargs)

            return _window_cache[window_id][cache_key]

        return wrapper

    return decorator


def clear():
    for func in _cache:
        func.cache_clear()

    del _window_cache[_get_window_id()]
