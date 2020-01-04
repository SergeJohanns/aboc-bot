from FunctionalityCore import FCore

class hi(FCore):
    """Testing core."""

    def get_commands(self) -> dict:
        return {"hi":self.hi}
    
    def hi(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello there {update.effective_user.first_name}!")