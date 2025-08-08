from aqt import main, gui_hooks
from aqt.qt import QMessageBox

from .utils.config import Config

# TODO: Typing

class Hook:
    FEEDBACK_ID = "review-feedback-container"
    FEEDBACK_DELAY = 1000

    def __init__(self, mw: main.AnkiQt):
        if not mw:
            return

        self.mw = mw
        self.error = False

        gui_hooks.reviewer_did_answer_card.append(self.show)

    def insert(self, html: str, css: str) -> str:
        return f"""
            (() => {{
                if (document.getElementById("{Hook.FEEDBACK_ID}")) {{
                    const f = document.getElementById("{Hook.FEEDBACK_ID}");
                    f.parentNode.removeChild(f);
                }}

                const feedback = document.createElement("div");

                feedback.id = "{Hook.FEEDBACK_ID}";
                document.body.insertAdjacentElement("afterbegin", feedback);

                feedback.insertAdjacentHTML("beforeend", `
                    <style>{css}</style>
                    {html}
                `);

                setTimeout(() => feedback.parentNode.removeChild(feedback), {Hook.FEEDBACK_DELAY});
            }})();
        """


    def show(self, reviewer, card, res, *args, **kwargs):
        if res not in [1, 2, 3, 4]:
            return

        config = Config()
        response = {
            1: "again",
            2: "hard",
            3: "good",
            4: "easy",
            # 5: "Undo"
        }

        # Get data
        all = config.feedback.get("all")
        selected = config.feedback.get(response[res])

        # Create web
        feedback = self.insert(
            all.html + selected.html,
            all.css + selected.css
        )

        try:
            self.mw.web.eval(feedback)
        except Exception as e:
            if not self.error:
                QMessageBox.information(
                    mw,
                    "Review Feedback",
                    "The review feedback config has an error. This message will only display once. Please check your config and ensure it is valid HTML/CSS" +
                    str(e),
                )

                self.error = True

            print("[review-feedback] web error!", e)

