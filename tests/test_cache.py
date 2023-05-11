import unittest
from contextlib import contextmanager
from unittest.mock import Mock, patch

from Projectionist.plugin import cache

_seed = 0


@cache.lru_cache
def _lru_cached(arg):
    return _seed + arg


@cache.window_cache("key1")
def _window_cached1(arg):
    return _seed + arg


@cache.window_cache("key1")
def _window_cached2(arg):
    return _seed + arg


@cache.window_cache("key2")
def _window_cached3(arg):
    return _seed + arg


class _Dummy:
    def __init__(self, key=""):
        self.window_cache_key = key

    @cache.window_cache("key2")
    def window_cached4(self, arg):
        return _seed + arg


@contextmanager
def mock_active_window(id=-1):
    active_window = Mock()
    active_window.id = Mock(return_value=id)

    with patch("sublime.active_window", return_value=active_window):
        yield active_window


class CacheTestCase(unittest.TestCase):
    def setUp(self):
        cache.clear()

    def test_lru_cache(self):
        global _seed

        for index in range(3):
            _seed = index
            self.assertEqual(_lru_cached(1), 1)

        _seed = 0
        self.assertEqual(_lru_cached(2), 2)

    def test_window_cache(self):
        global _seed

        _seed = 0
        self.assertEqual(_window_cached1(1), 1)
        self.assertEqual(_window_cached1(2), 1)

        _seed = 10
        self.assertEqual(_window_cached2(1), 1)
        self.assertEqual(_window_cached2(2), 1)

        _seed = 100
        self.assertEqual(_window_cached3(1), 101)
        self.assertEqual(_window_cached3(2), 101)

        _seed = 1000
        self.assertEqual(_Dummy().window_cached4(1), 101)
        self.assertEqual(_Dummy().window_cached4(2), 101)

    def test_window_cache_cache_key(self):
        global _seed

        _seed = 0
        self.assertEqual(_Dummy("prefix1").window_cached4(1), 1)
        self.assertEqual(_Dummy("prefix1").window_cached4(2), 1)
        _seed = 10
        self.assertEqual(_window_cached3(1), 11)

        _seed = 100
        self.assertEqual(_Dummy("prefix2").window_cached4(1), 101)
        self.assertEqual(_Dummy("prefix2").window_cached4(2), 101)

    def test_window_cache_multiple_windows(self):
        global _seed

        _seed = 0
        self.assertEqual(_window_cached1(1), 1)

        with mock_active_window():
            _seed = 10
            self.assertEqual(_window_cached1(1), 11)

    def test_clear_cache_lru_cache(self):
        global _seed

        for index in range(3):
            _seed = index
            self.assertEqual(_lru_cached(0), index)
            cache.clear()

    def test_clear_cache_window_cache(self):
        global _seed

        for index in range(3):
            _seed = index
            self.assertEqual(_window_cached1(0), index)
            cache.clear()

    def test_clear_cache_window_cache_multiple_windows(self):
        global _seed

        with mock_active_window(1000):
            cache.clear()
            _seed = 0
            self.assertEqual(_window_cached1(1), 1)

        with mock_active_window(1001):
            cache.clear()

        with mock_active_window(1000):
            _seed = 10
            self.assertEqual(_window_cached1(1), 1)
