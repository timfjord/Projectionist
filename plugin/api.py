"""Public API for the Projectionist package.
Can be used for finding alternate files.
See README.md for more information.
"""

from .errors import Error
from .root import Root
from .storage import Storage

__all__ = ["find_alternate_file"]


def find_alternate_file(root, file_name):
    """Finds an alternate file for a given file and root directory.

    Parameters
    ----------
    root : str
        Project directory where the file is located.
    file_name : str
        Absolute path to the file.

    Raises
    ------
    TypeError
        If root or file_name are empty or None.
    ValueError
        If file_name doesn't belong to root.

    Returns
    -------
    tuple
        a tuple of (exists, alternate) where exists is a boolean indicating whether
        the alternate file exists and alternate is the path to the alternate file
        or `None` if no alternate file is defined.
    """

    if not root or not file_name:
        raise TypeError("Invalid arguments")

    try:
        root, file = Root.find([str(root)], str(file_name))
    except Error:
        raise ValueError("'{}' doesn't belong to '{}'".format(file_name, root))

    exists, alternate = Storage(root).find_alternate_file(file)

    return exists, (alternate and alternate.path)
