import os
import time
import random
from FunctionalityCore import FCore
from FCores.utilcore import asynctimeout
from FCores.kerberos import require_ring

STORM_COUNT = 6
MEME_FOLDER = "Data/Memes/"

class meme(FCore):
    """Sends memes from a folder."""

    def get_commands(self) -> dict:
        return {"meme":self.meme, "storm":self.storm}
    
    def meme(self, update, context):
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(self.rand_meme(), 'rb'))

    @require_ring(2)
    @asynctimeout()
    def storm(self, update, context):
        for _ in range(STORM_COUNT):
            self.meme(update, context)
            time.sleep(1)
    
    def rand_meme(self):
        return MEME_FOLDER + random.choice(os.listdir(MEME_FOLDER))