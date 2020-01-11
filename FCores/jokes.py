import time
from FunctionalityCore import FCore
from FCores.utilcore import asynced

class jokes(FCore):
    """Collection of joke commands."""

    def get_commands(self):
        return {"recursion":self.recursion, "bee":self.bee}
    
    @asynced()
    def recursion(self, update, context):
        for _ in range(3):
            context.bot.send_message(chat_id=update.effective_chat.id, text="/recursion")
            time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id, text="jk")
    
    def bee(self, update, context):
        DELAY = 1 if update.effective_chat.type == "private" else 3
        with open("Data/bee.txt", 'r') as bee:
            sentences = bee.read().split(". ")
            i, j = 0, 0
            while j < len(sentences):
                while j < len(sentences) and len(message := ". ".join(sentences[i:j]) + ".") < 2048:
                    j += 1
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
                i = j
                time.sleep(DELAY)