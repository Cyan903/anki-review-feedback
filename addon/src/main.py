from aqt import main, mw
from aqt.qt import QAction, QDialog, QTextEdit

from .utils.consts import QT_VER
from .utils.config import Config

if QT_VER == 6:
    from ..res.Qt6.config import Ui_feedbackDialog
else:
    from ..res.Qt5.config import Ui_feedbackDialog


class ReviewPage:
    def __init__(self, name: str, textEditHTML: QTextEdit, textEditCSS: QTextEdit):
        self.name = name
        self.textEditHTML = textEditHTML
        self.textEditCSS = textEditCSS

    def load(self, config):
        res = config.feedback.get(self.name)

        if res:
            self.textEditHTML.setPlainText(res.html)
            self.textEditCSS.setPlainText(res.css)


class ReviewFeedback:
    def __init__(self, mw: main.AnkiQt) -> None:
        if not mw:
            return

        self.menuAction = QAction(
            "Configure Review Feedback", mw, triggered=self.clicked
        )

        self.config = None
        self.elements = None

        mw.form.menuTools.addAction(self.menuAction)
        # mw.addonManager.setConfigAction(__name__, self.clicked)

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

        # Load content
        for elm in self.elements:
            elm.load(config=self.config)

        ui.buttonBox.accepted.connect(self.save)
        dialog.exec()

    def save(self):
        if not self.config or not self.elements:
            return

        for elm in self.elements:
            self.config.feedback.set(
                elm.name, elm.textEditHTML.toPlainText(), elm.textEditCSS.toPlainText()
            )

        self.config.write()
