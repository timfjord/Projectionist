"""
Public API for the Projectionist package.
Can be used for finding alternate files.
See README.md for more information.
"""
from .root import Root
from .storage import Storage

__all__ = ["find_alternate_file"]


def find_alternate_file(root, file_name):
    root, file = Root.find([str(root)], str(file_name))
    exists, alternate = Storage(root).find_alternate_file(file)

    return exists, (alternate and alternate.path)
