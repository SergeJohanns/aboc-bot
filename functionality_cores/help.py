from functionality_core import FCore
from functionality_cores.utilcore import safelog

class help(FCore):
    """Give an overview of available commands."""

    def get_commands(self) -> dict:
        return {"start":self.start, "help":self.help}

    @safelog
    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello there {update.effective_user.first_name}, use /help for a full list of commands.")

    def help(self, update, context):
        commands = ', '.join(sorted(['/' + command for core in self.bot.cores.values() for command in core.get_commands().keys()]))
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"I have the following commands: {commands}")

    def not_command(self, update, context):
        command = update.effective_message.text.split(" ")[0]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"I'm sorry Dave, I'm afraid I can't do {command}.")