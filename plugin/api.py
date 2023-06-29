"""
Public API for the Projectionist package.
Can be used for finding alternate files.
See README.md for more information.
"""
from .errors import Error
from .root import Root
from .storage import Storage

__all__ = ["find_alternate_file"]


def find_alternate_file(root, file_name):
    if not root or not file_name:
        raise TypeError("Invalid arguments")

    try:
        root, file = Root.find([str(root)], str(file_name))
    except Error:
        raise ValueError("'{}' doesn't belong to '{}'".format(file_name, root))

    exists, alternate = Storage(root).find_alternate_file(file)

    return exists, (alternate and alternate.path)
