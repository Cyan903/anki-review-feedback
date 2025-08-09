from aqt import mw
from aqt.qt import QMessageBox


class ReviewerItem:
    def __init__(self, html: str, css: str):
        self.html = html
        self.css = css


class ReviewerConfig:
    def __init__(self):
        self.all = ReviewerItem("<div id=\"feedback-container\">...</div>", "#feedback-container {\n    font-weight: bolder !important;\n    font-size: 20px !important;\n    letter-spacing: 0.4ch !important;\n    position: fixed !important;\n    top: 0 !important;\n    left: 0 !important;\n    right: 0 !important;\n    margin: 0 auto !important;\n    text-align: center !important;\n}")
        self.again = ReviewerItem("", "#feedback-container { color: red; }")
        self.hard = ReviewerItem("", "#feedback-container { color: white; }")
        self.good = ReviewerItem("", "#feedback-container { color: green; }")
        self.easy = ReviewerItem("", "#feedback-container { color: blue; }")

    def json(self):
        return {
            k: {"html": f.html, "css": f.css}
            for k, f in vars(self).items()
            if isinstance(f, ReviewerItem)
        }

    def set(self, name: str, html: str, css: str) -> bool:
        if not hasattr(self, name):
            return False

        setattr(self, name, ReviewerItem(html, css))
        return True

    def get(self, name: str) -> ReviewerItem | None:
        feedback = getattr(self, name, None)
        return feedback if isinstance(feedback, ReviewerItem) else None


class Config:
    PLUGIN_NAME = None
    REVIEWER_ITEMS = ["all", "again", "hard", "good", "easy"]
    LOCATION_ITEMS = ["beforebegin", "afterbegin", "beforeend", "afterend"]

    def __init__(self):
        if not Config.PLUGIN_NAME:
            return

        self._config = mw.addonManager.getConfig(Config.PLUGIN_NAME)
        self.reset()

        if not self._config or not self.parse():
            QMessageBox.information(
                mw,
                "Review Feedback",
                "Invalid config! Config will be reverted to defaults.",
            )

            # Reset config
            self.reset()
            self.write()

    def reset(self):
        self.id = "review-feedback-container"
        self.location = "afterbegin"
        self.delay = 1000
        self.reviewer = ReviewerConfig()

    def parse(self) -> bool:
        self.id = self.read("id")
        self.location = self.read("location")
        self.delay = self.read("delay")

        if (
            # Validate ID and None
            None in [self.id, self.location, self.delay]
            or len(self.id) <= 1
            # Validate delay
            or not isinstance(self.delay, int)
            or self.delay < 5
            or self.delay > 9999
            # Validate location
            or self.location not in Config.LOCATION_ITEMS
        ):
            return False

        # Validate reviewer
        for name in Config.REVIEWER_ITEMS:
            try:
                if not self.reviewer.set(
                    name,
                    self._config["reviewer"][name]["html"],
                    self._config["reviewer"][name]["css"],
                ):
                    return False
            except KeyError:
                print(f"[review-feedback] {name} is invalid -> {self._config}")
                return False

        return True

    def read(self, name: str) -> str | int | None:
        try:
            return self._config[name]
        except KeyError:
            print(f"[review-feedback] {name} is invalid -> {self._config}")
            return None

    def write(self):
        mw.addonManager.writeConfig(
            Config.PLUGIN_NAME,
            {
                "id": self.id,
                "location": self.location,
                "delay": self.delay,
                "reviewer": self.reviewer.json(),
            },
        )

        self._config = mw.addonManager.getConfig(Config.PLUGIN_NAME)
