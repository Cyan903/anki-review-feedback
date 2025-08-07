from aqt import mw


class Snackbar:
    def __init__(self, html, css):
        self.html = html
        self.css = css


class Config:
    PLUGIN_NAME = None

    def __init__(self):
        if not Config.PLUGIN_NAME:
            return

        self.config = mw.addonManager.getConfig(Config.PLUGIN_NAME)

        # TODO: This
        if not self.validate():
            self.fallback()

        self.snacks = {
            "all": Snackbar(
                self.config["all"]["html"],
                self.config["all"]["css"]
            ),

            "again": Snackbar(
                self.config["again"]["html"], self.config["again"]["css"]
            ),

            "hard": Snackbar(
                self.config["hard"]["html"],
                self.config["hard"]["css"]
            ),

            "good": Snackbar(
                self.config["good"]["html"],
                self.config["good"]["css"]
            ),

            "easy": Snackbar(
                self.config["easy"]["html"],
                self.config["easy"]["css"]
            ),
        }

    def save(self):
        mw.addonManager.writeConfig(__name__, self.snacks)

    def validate(self) -> bool:
        return True

    def fallback(self):
        pass
