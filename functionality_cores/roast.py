import random
from functionality_core import FCore

ROASTS = [
    "I’ll never forget the first time I met {}. But I’ll keep trying.",
    "{}'s face makes onions cry.",
    "{} brings everyone so much joy. When they leave the chat, specifically.",
    "Seeing {} triggers my garbage collection.",
    "I especially like simulating {}'s thoughts because it's so computationally efficient.",
    "Imagine a world where one's capital means are not decided by the circumstances of ones birth, but instead by one's thrift, perseverance, intellectual prowess and quality of character alone. Not only would such a world surely be a much happier place, {} would still be destitute.",
    "Mathematicians have recently proven that saying anything positive about {} is an NP-hard problem."
]

class roast(FCore):
    """Critically important core. Some insults are copied from somewhere online, some I made up."""

    def get_commands(self) -> dict:
        return {"roast":self.roast}

    def roast(self, update, context):
        if ' ' in update.message.text:
            roastee = update.message.text.split(' ', 1)[1]
        else:
            context.bot.send_message(chat_id = update.effective_chat.id, text = "Remember to give me someone to roast")
        if not roastee or roastee.isspace():
            context.bot.send_message(chat_id = update.effective_chat.id, text = "Remember to give me someone to roast")
        if 'serge' in roastee.casefold():
            roastee = update.effective_user.first_name
        context.bot.send_message(chat_id = update.effective_chat.id, text = random.choice(ROASTS).format(roastee))