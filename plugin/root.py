import os.path

from . import glob2
from .errors import Error
from .utils import to_unpackable


class Root:
    OR = "|"
    AND = "&"

    @classmethod
    def find(cls, folders, file, subprojects=[]):
        if not bool(file) or not bool(folders):
            raise Error("No file or folders provided")

        root = cls(folders[0])
        for subproject in subprojects:
            folders.append(
                root.join(*to_unpackable(subproject)),
            )

        for folder in sorted(folders, key=len, reverse=True):
            # Since Sublime returns expanded path so it should be fine to use `startswith`,
            # but more future-proof solution would be using `pathlib.Path`
            if file.startswith(folder):
                root = cls(folder)
                relpath = root.relpath(file)

                return (root, root.file(relpath))
        else:
            raise Error("File '{}' is outside of the project".format(file))

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return "Root('{}')".format(self.path)

    def __eq__(self, other):
        return str(self) == str(other)

    def join(self, *paths):
        return os.path.join(self.path, *paths)

    def relpath(self, file):
        return os.path.relpath(file, self.path)

    def file(self, *paths):
        return File(self, *paths)

    def glob(self, *paths):
        return Glob(self, *paths)

    def contains(self, patterns):
        for pattern in patterns.split(self.OR):
            for glob in pattern.split(self.AND):
                if not any(self.glob(*glob.split("/"))):
                    break
            else:
                return True

        return False


class RelativePath:
    def __init__(self, root, *paths):
        if not bool(paths):
            raise ValueError("Path is required")

        self.root = root
        self.relpath = os.path.join(*paths)
        self.path = self.root.join(self.relpath)

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return "{}('{}', '{}')".format(self.__class__.__name__, self.root, self.relpath)

    def __eq__(self, other):
        return str(self) == str(other)

    def exists(self):
        return os.path.exists(self.path)

    def create(self, content):
        raise NotImplementedError()


class File(RelativePath):
    def exists(self):
        return os.path.isfile(self.path)

    def create(self, content):
        with open(self.path, "x") as file:
            file.write(content)


class Glob:
    def __init__(self, root, *paths):
        if not bool(paths):
            raise ValueError("Path is required")

        self.root = root
        self.pattern = self.root.join(*paths)

    def __iter__(self):
        return glob2.iglob(self.pattern)
