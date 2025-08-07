if __name__ != "__main__":
    from aqt import mw
    from .src import main
    from .src.utils.config import Config

    # https://addon-docs.ankiweb.net/qt.html#garbage-collection
    if mw:
        Config.PLUGIN_NAME = __name__
        mw.review = main.ReviewFeedback(mw)
else:
    print("This is an anki plugin.")
