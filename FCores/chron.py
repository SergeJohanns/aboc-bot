import time
from threading import Timer
from FunctionalityCore import FCore

class chron(FCore):
    """Provide basic time-based functionality."""

    def get_commands(self) -> dict:
        return {"time":self.send_time, "timer":self.set_timer}
    
    def send_time(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"It has been {hex(int(time.time()))} seconds since the epoch.")
    
    def set_timer(self, update, context):
        try:
            Timer(
                int(update.effective_message.text.split(" ", 1)[1]),
                context.bot.send_message,
                kwargs={
                    "chat_id":update.effective_chat.id,
                    "text":"Your counter is up!",
                    "reply_to_message_id":update.effective_message.message_id
                }
            ).start()
        except IndexError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="How many seconds?")