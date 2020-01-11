from threading import Thread
from functools import wraps
from FunctionalityCore import FCore

def safelog(func):
    """Version of prism.log that has prism as an optional dependency.
    This prevents the sql database, which may not be available, from becoming a strict dependency."""
    @wraps(func)
    def inner(self, update, context):
        try:
            self.bot.cores["prism"].log_user(update.effective_user)
            if update.effective_user.id != update.effective_chat.id: # If the chat is not a one-to-one chat with the user.
                self.bot.cores["prism"].log_chat(update.effective_chat)
            func(self, update, context)
        except Exception as e:
            print(e)
    return inner

def asynced(func):
    """Executes the command in a seperate thread."""
    @wraps(func)
    def inner(self, update, context):
        Thread(target=func, args=(self, update, context), daemon=True).start()
    return inner

class utilcore(FCore):
    pass