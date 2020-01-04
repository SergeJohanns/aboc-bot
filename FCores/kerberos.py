from FunctionalityCore import FCore
import json
import traceback

RING_FILE = "Data/UserRings.json"
DEFAULT_RING = 3

class kerberos(FCore):
    """Provide a security ring system, allowing for distinction between privileged and regular users."""

    def get_commands(self) -> dict:
        return {"ring":self.send_ring, "grant":self.grant}

    def send_ring(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your ring is {self.get_ring(update.effective_user.username)}")

    def grant(self, update, context):
        if self.get_ring(update.effective_user.username) <= -1:
            target, ring = (args := update.effective_message.text.split())[1], args[2]
            self.give_ring(target, ring)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Successfully updated {target}'s security ring to {ring}.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Your security ring is unsufficient to use /grant.")

    def get_ring(self, userName: str):
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