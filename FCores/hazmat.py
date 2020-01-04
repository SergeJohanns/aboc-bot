# REQUIRES: kerberos.py
# This core is pretty stupid, use at your own risk

import os
from FunctionalityCore import FCore

class hazmat(FCore):
    """Provide stupidly insecure functionality, including eval and direct terminal commands."""

    def get_commands(self) -> dict:
        return {"eval":self.eval_message, "os":self.os_command}
    
    def eval_message(self, update, context):
        if self.bot.cores["kerberos"].get_ring(update.effective_user.username) <= -1:
            context.bot.send_message(chat_id=update.effective_chat.id, text=str(
                eval(update.effective_message.text.split(" ", 1)[1])
            ))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your security ring is unsufficient to use /eval.")
    
    def os_command(self, update, context):
        if self.bot.cores["kerberos"].get_ring(update.effective_user.username) <= -1:
            os.system(update.effective_message.text.split(" ", 1)[1])
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your security ring is unsufficient to use /os.")