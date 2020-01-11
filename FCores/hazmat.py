# This core is pretty stupid, use at your own risk

import os
from FunctionalityCore import FCore
from FCores.utilcore import asynced
from FCores.kerberos import require_ring

class hazmat(FCore):
    """Provide stupidly insecure functionality, including eval and direct terminal commands."""

    def get_commands(self) -> dict:
        return {"eval":self.eval_message, "os":self.os_command}
    
    @require_ring(-1)
    @asynced(5)
    def eval_message(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(
            eval(update.effective_message.text.split(" ", 1)[1])
        ),
        reply_to_message_id=update.effective_message.message_id)
    
    @require_ring(-2)
    def os_command(self, update, context):
        os.system(update.effective_message.text.split(" ", 1)[1])