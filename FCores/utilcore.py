from threading import Timer
from functools import wraps
from multiprocessing import Process
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
        except KeyError: # If the prism core is not loaded.
            pass
        func(self, update, context)
    return inner

def asynced(timeout: float = 0):
    """Executes the command in a seperate thread."""
    def outer(func):
        @wraps(func)
        def inner(self, update, context):
            def kill_process():
                """Kill the proces if it takes too long, depending on the timeout given."""
                if p.is_alive():
                    p.terminate()
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Operation timed out.",
                        reply_to_message_id=update.effective_message.message_id
                    )
            p = Process(target=func, args=(self, update, context), daemon=True)
            p.start()
            if timeout:
                Timer(timeout, kill_process).start()
        return inner
    return outer

class utilcore(FCore):
    pass