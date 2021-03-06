import time
import functools
from functionality_core import FCore
from functionality_cores.kerberos import require_ring

class democracy(FCore):
    """Allow for arbitrary polling in group chats."""

    def __init__(self, bot):
        super().__init__(bot)
        self.polls = dict()
    
    def get_commands(self) -> dict:
        return {"poll":self.poll, "yay":functools.partial(self.vote, "yay"), "nay":functools.partial(self.vote, "nay"), "closepoll":self.closepoll}
    
    @require_ring(2)
    def poll(self, update, context):
        if update.effective_chat.id in self.polls:
            context.bot.send_message(chat_id=update.effective_chat.id, text="This chat already has a poll running: " + self.polls[update.effective_chat.id]["poll"])
        else:
            poll = update.effective_message.text.split(' ', 1)[1]
            self.polls[update.effective_chat.id] = {"poll":poll, "voters":set(), "yay":0, "nay":0}
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"New poll: {poll} Vote in favour or against with /yay or /nay respectively.")
        
    def closepoll(self, update, context):
        if not update.effective_chat.id in self.polls:
            context.bot.send_message(chat_id=update.effective_chat.id, text="There is no running poll in this chat.")
        result = self.polls[update.effective_chat.id]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The results are in on the poll: {result['poll']}")
        time.sleep(0.2)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"For the yays, {result['yay']}. For the nays, {result['nay']}.")
        del self.polls[update.effective_chat.id]

    def vote(self, result:str, update, context):
        if update.effective_chat.id in self.polls:
            chat_id = update.effective_chat.id
        elif (chat := self.bot.cores["prism"].by_chat_title(update.effective_message.text.split(' ', 1)[1]))["id"] in self.polls:
            chat_id = chat["id"]
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="There is no ongoing poll in this chat.", reply_to_message_id=update.effective_message.message_id)
            return
        if update.effective_user.id not in self.polls[chat_id]["voters"]:
            self.polls[chat_id]["voters"].add(update.effective_user.id)
            self.polls[chat_id][result] += 1
            context.bot.send_message(chat_id=update.effective_chat.id, text="Registered " + result + " vote.", reply_to_message_id=update.effective_message.message_id)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You have already voted in this poll.", reply_to_message_id=update.effective_message.message_id)