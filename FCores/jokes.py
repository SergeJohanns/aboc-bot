import time
from FunctionalityCore import FCore
from FCores.utilcore import asynced
from FCores.kerberos import require_ring

class jokes(FCore):
    """Collection of joke commands."""

    def get_commands(self):
        return {"recursion":self.recursion, "bee":self.bee}
    
    @asynced
    def recursion(self, update, context):
        for _ in range(3):
            context.bot.send_message(chat_id=update.effective_chat.id, text="/recursion")
            time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id, text="jk")
    
    @require_ring(2)
    @asynced
    def bee(self, update, context):
        DELAY = 1 if update.effective_chat.type == "private" else 3
        def blocks(sentences: list):
            out = []
            i, j = 0, 0
            while j < len(sentences):
                while j < len(sentences) and len(". ".join(sentences[i:j]) + ".") < 2048:
                    j += 1
                out.append(". ".join(sentences[i:j-1]) + ".")
                i = j
            return out
        with open("Data/bee.txt", 'r') as bee:
            for block in blocks(bee.read().split(". ")):
                context.bot.send_message(chat_id=update.effective_chat.id, text=block)
                time.sleep(DELAY)