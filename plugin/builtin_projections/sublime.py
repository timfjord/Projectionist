BUILTIN_PROJECTIONS = {
    "*.sublime-settings": {
        "sublime-package.json": {
            "alternate": "{project|basename}.sublime-settings",
        },
        "*.sublime-settings": {
            "alternate": "sublime-package.json",
        },
        "messages/*.txt": {
            "alternate": "messages.json",
        },
    },
}
