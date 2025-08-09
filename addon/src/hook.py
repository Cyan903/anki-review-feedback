from aqt import main, gui_hooks
from aqt.qt import QMessageBox

from .utils.config import Config


class Hook:
    def __init__(self, mw: main.AnkiQt):
        if not mw:
            return

        self.mw = mw
        self.error = False

        gui_hooks.reviewer_did_answer_card.append(self.show)

    def insert(self, config: Config, html: str, css: str) -> str:
        return f"""
            (() => {{
                if (document.getElementById("{config.id}")) {{
                    const f = document.getElementById("{config.id}");
                    f.parentNode.removeChild(f);
                }}

                const feedback = document.createElement("div");

                feedback.id = "{config.id}";
                document.body.insertAdjacentElement(
                    "{config.location}", feedback
                );

                feedback.insertAdjacentHTML("beforeend", `
                    <style>{css}</style> {html}
                `);

                setTimeout(() => feedback.parentNode.removeChild(feedback), {
                    config.delay
                });
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
            # 5: "undo"
        }

        # Get data
        all = config.reviewer.get("all")
        selected = config.reviewer.get(response[res])

        # Create web
        feedback = self.insert(config, all.html + selected.html, all.css + selected.css)

        try:
            self.mw.web.eval(feedback)
        except Exception as e:
            if not self.error:
                QMessageBox.information(
                    self.mw,
                    "Review Feedback",
                    "The review feedback config has an error."
                    + " This message will only display once."
                    + " Please check your config and ensure it is valid."
                    + f"\n\n-> {str(e)}",
                )

                self.error = True

            print("[review-feedback] web error!", e)
