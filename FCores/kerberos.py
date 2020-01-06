from FunctionalityCore import FCore
import json
from functools import wraps

RING_FILE = "Data/UserRings.json"
DEFAULT_RING = 3

def require_ring(min_ring: int):
    def outer(func):
        @wraps(func)
        def inner(self, update, context):
            if (ring := self.bot.cores["kerberos"].get_ring(update.effective_user.username)) <= min_ring:
                func(self, update, context)
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Your security ring ({ring}) is insufficient for {update.effective_message.text.split(' ')[0]}, which requires ring {min_ring} or lower.",
                    reply_to_message_id=update.effective_message.message_id
                )
        return inner
    return outer

class kerberos(FCore):
    """Provide a security ring system, allowing for distinction between privileged and regular users."""

    def get_commands(self) -> dict:
        return {"ring":self.send_ring, "grant":self.grant}

    def send_ring(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your ring is {self.get_ring(update.effective_user.username)}")

    @require_ring(-1)
    def grant(self, update, context):
        target, ring = update.effective_message.text.split()[1:3]
        self.give_ring(target, ring)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Successfully updated {target}'s security ring to {ring}.")

    def get_ring(self, userName: str) -> int:
        try:
            with open(RING_FILE, 'r') as rings:
                return json.loads(rings.read())[userName]
        except:
            return DEFAULT_RING

    def give_ring(self, userName: str, ring: int):
        try:
            with open(RING_FILE, 'r') as file:
                rings = json.loads(file.read())
        except:
            rings = dict()
        finally:
            rings[userName] = int(ring)
            with open(RING_FILE, 'w') as file:
                file.write(json.dumps(rings, indent=4, sort_keys=True))