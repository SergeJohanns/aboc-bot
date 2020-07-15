from threading import Timer
from functionality_core import FCore

PROMPT = "$ "

class terminus(FCore):
    """Take control of the terminal after core loading and allow the user to defer it to the other cores."""

    def __init__(self, bot):
        super().__init__(bot)
        terminus = Timer(0.1, self.terminal_control)
        terminus.daemon = True
        terminus.start()

    def terminal_control(self):
        print("\nTERMINUS CONTROL CORE")
        while True:
            try:
                self.bot.cores[input(PROMPT)].terminal_control()
                print("Core released terminal control, returning to terminus.")
            except KeyError:
                print("No such core is loaded.")