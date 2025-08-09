from aqt.qt import QT_VERSION_STR

CURRENT_VERSION = "0.0.0"

SOURCE_URL = "https://github.com/Cyan903/anki-review-feedback"
HELP_URL = f"{SOURCE_URL}/issues"
PRESETS_URL = f"{SOURCE_URL}/blob/main/docs/presets.md"

# https://addon-docs.ankiweb.net/qt.html#qt-versions
QT_VER = int(QT_VERSION_STR.split(".")[0])
