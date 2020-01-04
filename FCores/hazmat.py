# This core is pretty stupid, use at your own risk

import os
from FunctionalityCore import FCore
<<<<<<< HEAD
from FCores.kerberos import require_ring
=======
from kerberos import require_ring
>>>>>>> d9058d754b0e97c45eedbb7e0ca1298baf777e40

class hazmat(FCore):
    """Provide stupidly insecure functionality, including eval and direct terminal commands."""

    def get_commands(self) -> dict:
        return {"eval":self.eval_message, "os":self.os_command}
    
    @require_ring(-1)
    def eval_message(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(
            eval(update.effective_message.text.split(" ", 1)[1])
        ))
    
    @require_ring(-1)
    def os_command(self, update, context):
        os.system(update.effective_message.text.split(" ", 1)[1])