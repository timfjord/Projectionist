import functools
from collections import defaultdict

import sublime

_lru_cache = []
_window_cache = defaultdict(dict)


def lru_cache(func):
    func = functools.lru_cache(maxsize=None)(func)
    _lru_cache.append(func)

    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper_cache


def _get_window_id():
    try:
        return sublime.active_window().id()
    except (AttributeError, TypeError):
        pass


def window_cache(key):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            window_id = _get_window_id()
            cache_key = "-".join(
                (
                    key,
                    str(getattr(args[0], "window_cache_key", "")) if bool(args) else "",
                )
            )

            if cache_key not in _window_cache[window_id]:
                _window_cache[window_id][cache_key] = func(*args, **kwargs)

            return _window_cache[window_id][cache_key]

        return wrapper

    return decorator


def clear():
    for func in _lru_cache:
        func.cache_clear()

    _window_cache.pop(_get_window_id(), None)
