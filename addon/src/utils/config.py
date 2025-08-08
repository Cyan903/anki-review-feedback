from aqt import mw
from aqt.qt import QMessageBox


class FeedbackItem:
    def __init__(self, html: str, css: str):
        self.html = html
        self.css = css


class FeedbackConfig:
    def __init__(self):
        self.all = FeedbackItem("defaults", "")
        self.again = FeedbackItem("", "")
        self.hard = FeedbackItem("", "")
        self.good = FeedbackItem("", "")
        self.easy = FeedbackItem("", "")

    def json(self):
        return {
            k: {"html": f.html, "css": f.css}
            for k, f in vars(self).items()
            if isinstance(f, FeedbackItem)
        }

    def set(self, name: str, html: str, css: str) -> bool:
        if not hasattr(self, name):
            return False

        setattr(self, name, FeedbackItem(html, css))
        return True

    def get(self, name: str) -> FeedbackItem | None:
        feedback = getattr(self, name, None)
        return feedback if isinstance(feedback, FeedbackItem) else None


class Config:
    PLUGIN_NAME = None

    def __init__(self):
        if not Config.PLUGIN_NAME:
            return

        self._config = mw.addonManager.getConfig(Config.PLUGIN_NAME)
        self.feedback = FeedbackConfig()

        if not self._config or not self.parse():
            QMessageBox.information(
                mw,
                "Review Feedback",
                "Invalid config! Config will be reverted to defaults.",
            )

            # Reset config
            self.feedback = FeedbackConfig()
            self.write()

    def parse(self) -> bool:
        for name in ["all", "again", "hard", "good", "easy"]:
            try:
                if not self.feedback.set(
                    name, self._config[name]["html"], self._config[name]["css"]
                ):
                    return False
            except KeyError:
                print(f"[review-feedback] {name} is invalid -> {self._config}")
                return False

        return True

    def write(self):
        mw.addonManager.writeConfig(Config.PLUGIN_NAME, self.feedback.json())
        self._config = mw.addonManager.getConfig(Config.PLUGIN_NAME)
