from aqt import main, mw
from aqt.qt import QAction, QDialog, QTextEdit, QMessageBox

from .utils.consts import CURRENT_VERSION, HELP_URL, PRESETS_URL, SOURCE_URL, QT_VER
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

    def load(self, config: Config):
        res = config.reviewer.get(self.name)

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
        self.advanced = None

        mw.form.menuTools.addAction(self.menuAction)
        # mw.addonManager.setConfigAction(__name__, self.clicked)

    def clicked(self) -> None:
        dialog = QDialog(mw)
        ui = Ui_feedbackDialog()

        # Setup UI
        ui.setupUi(dialog)

        # Setup help buttons
        ui.pushButtonAdvancedID.clicked.connect(
            ReviewFeedback.help(
                "Insert ID",
                "This is the ID of the container to insert the feedback item."
                + " Change this if you're facing issues with overlapping HTML.",
            )
        )

        ui.pushButtonAdvancedInsert.clicked.connect(
            ReviewFeedback.help(
                "Insert Location",
                "This determines where in the body you want the HTML to be inserted."
                + "\n\nhttps://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML#position",
            )
        )

        ui.pushButtonAdvancedTimer.clicked.connect(
            ReviewFeedback.help(
                "Duration",
                "How long you want the feedback item to be visible for in miliseconds.",
            )
        )

        # Setup links
        ui.labelAdvancedLinksSource.setText(
            f"<a href='{SOURCE_URL}'>Source Code ({CURRENT_VERSION})</a>"
        )

        ui.labelAdvancedLinksPresets.setText(f"<a href='{PRESETS_URL}'>Presets</a>")
        ui.labelAdvancedLinksHelp.setText(f"<a href='{HELP_URL}'>Help</a>")

        # Setup config
        self.config = Config()
        self.elements = [
            ReviewPage("all", ui.textEditAllHTML, ui.textEditAllCSS),
            ReviewPage("again", ui.textEditAgainHTML, ui.textEditAgainCSS),
            ReviewPage("hard", ui.textEditHardHTML, ui.textEditHardCSS),
            ReviewPage("good", ui.textEditGoodHTML, ui.textEditGoodCSS),
            ReviewPage("easy", ui.textEditEasyHTML, ui.textEditEasyCSS),
        ]

        self.advanced = {
            "id": ui.lineEditAdvancedID,
            "location": ui.comboBoxAdvancedInsert,
            "delay": ui.spinBoxAdvancedTimer,
        }

        # Load content
        for elm in self.elements:
            elm.load(config=self.config)

        self.advanced["id"].setText(self.config.id)
        self.advanced["location"].addItems(Config.LOCATION_ITEMS)
        self.advanced["delay"].setValue(self.config.delay)

        loc = self.advanced["location"].findText(self.config.location)

        if loc != -1:
            self.advanced["location"].setCurrentIndex(loc)

        ui.buttonBox.accepted.connect(self.save)
        dialog.exec()

    def save(self):
        if not self.config or not self.elements or not self.advanced:
            return

        # Set reviewer settings
        for elm in self.elements:
            self.config.reviewer.set(
                elm.name, elm.textEditHTML.toPlainText(), elm.textEditCSS.toPlainText()
            )

        # Set advanced settings
        self.config.id = self.advanced["id"].text()
        self.config.location = self.advanced["location"].currentText()
        self.config.delay = self.advanced["delay"].value()

        self.config.write()

        if not self.config.parse():
            QMessageBox.information(mw, "Review Feedback", "Invalid config!")

    def help(title: str, message: str):
        def _call():
            QMessageBox.information(mw, f"Review Feedback - {title}", message)

        return _call
