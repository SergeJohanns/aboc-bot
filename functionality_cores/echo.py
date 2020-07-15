from functionality_core import FCore

class echo(FCore):
    """Echo a direct message back to the user."""

    def message(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_message.text)