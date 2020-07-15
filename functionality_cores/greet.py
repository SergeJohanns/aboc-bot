from functionality_core import FCore

class greet(FCore):
    """Testing core."""

    def get_commands(self) -> dict:
        return {"hi":self.hi}
    
    def hi(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello there {update.effective_user.first_name}!")