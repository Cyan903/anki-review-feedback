from aqt import main, mw
from aqt.qt import QAction, QDialog

from .utils.consts import QT_VER
from .utils.config import Config

if QT_VER == 6:
    from ..res.Qt6.config import Ui_feedbackDialog
else:
    from ..res.Qt5.config import Ui_feedbackDialog


class ReviewPage:
    def __init__(self, name, textEditHTML, textEditCSS):
        self.name = name
        self.textEditHTML = textEditHTML
        self.textEditCSS = textEditCSS

    def load(self, config):
        self.textEditHTML.setPlainText(config.snacks[self.name].html)
        self.textEditCSS.setPlainText(config.snacks[self.name].css)


class ReviewFeedback:
    def __init__(self, mw: main.AnkiQt) -> None:
        if not mw:
            return

        self.menuAction = QAction(
            "Configure Review Feedback", mw, triggered=self.clicked
        )

        mw.form.menuTools.addSeparator()
        mw.form.menuTools.addAction(self.menuAction)
        mw.addonManager.setConfigAction(__name__, self.clicked)

    def clicked(self) -> None:
        dialog = QDialog(mw)
        ui = Ui_feedbackDialog()

        # Setup UI
        ui.setupUi(dialog)

        # Setup config
        self.config = Config()
        self.elements = [
            ReviewPage("all", ui.textEditAllHTML, ui.textEditAllCSS),
            ReviewPage("again", ui.textEditAgainHTML, ui.textEditAgainCSS),
            ReviewPage("hard", ui.textEditHardHTML, ui.textEditHardCSS),
            ReviewPage("good", ui.textEditGoodHTML, ui.textEditGoodCSS),
            ReviewPage("easy", ui.textEditEasyHTML, ui.textEditEasyCSS),
        ]

        for elm in self.elements:
            elm.load(config=self.config)

        dialog.exec()
