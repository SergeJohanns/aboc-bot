from functionality_core import FCore

class puppet(FCore):
    """Add controlled messaging capability."""

    def terminal_control(self):
        """Repeatedly ask for targets and messages."""
        while True:
            try:
                target = input("> ")
                if target == ":q":
                    return
                elif target[:3] == "-c ":
                    chat_id = self.bot.cores["prism"].by_chat_title(target[3:])["id"]
                else:
                    chat_id = self.bot.cores["prism"].by_username(target)["id"]
                message = input("$ ")
                self.bot.updater.bot.send_message(chat_id=chat_id, text=message)
            except KeyError:
                print("Target not found.")
            except Exception as e:
                print(e)