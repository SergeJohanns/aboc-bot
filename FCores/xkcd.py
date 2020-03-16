import random
import FCores.dependencies.xkcdserve as xkcdserve
from FCores.utilcore import asynced
from FunctionalityCore import FCore

class xkcd(FCore):
    def get_commands(self):
        return {"xkcd":self.get_comic}
    
    def send_comic(self, number: int, update, context):
        url, alt_text = xkcdserve.fetch_comic(number)
        if url:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=alt_text)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="That's not a valid xkcd number.")
    
    @asynced
    def get_comic(self, update, context):
        try:
            param = update.effective_message.text.split(' ', 1)[1]
        except IndexError:
            self.send_comic("", update, context)
            return
        if param == "rand":
            self.send_comic(random.randint(1, xkcdserve.latest_comic_number()), update, context)
            return
        try:
            number = int(param)
        except ValueError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Comic ids should be numbers.")
        else:
            self.send_comic(number, update, context)