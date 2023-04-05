import logging

import sublime

from .cache import lru_cache

BASE_NAME = "Projectionist.sublime-settings"
PROJECT_SETTINGS_KEY = "Projectionist"

logger = logging.getLogger(__name__)


def _ensure_dict(d):
    return d if isinstance(d, dict) else {}


@lru_cache
def project_settings():
    # fmt: off
    return _ensure_dict(
        _ensure_dict(
            _ensure_dict(
                sublime.active_window().project_data()
            ).get('settings', {}),
        ).get(PROJECT_SETTINGS_KEY, {})
    )
    # fmt: on


def settings():
    return sublime.load_settings(BASE_NAME)


def get(key, type=None, default=None, scope=None):
    if not isinstance(key, str):
        key = ".".join(key)

    if scope == "project" or scope is None and key in project_settings():
        value = project_settings().get(key, default)
    elif scope == "global" or scope is None:
        value = settings().get(key, default=default)
    else:
        logger.error("Unknown scope: '%s'", scope)
        return None

    if type is not None and not isinstance(value, type):
        logger.info(
            "type doesn't match: key: '%s', value: '%s', expected type: '%s'",
            key,
            value,
            type.__name__,
        )
        return None

    return value
