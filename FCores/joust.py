import time
import functools
from typing import Dict, Counter
from collections import Counter as colCounter

from FunctionalityCore import FCore
from FCores.utilcore import asynced
import FCores.dependencies.bfjoust

class joust(FCore):
    """Core for running bfjoust tournaments."""

    def __init__(self, bot):
        super().__init__(bot)
        self.reset()

    def reset(self):
        self.listening = False # Indicates whether the bot is listening for new warriors.
        self.warriors = {} # Dictionary that maps uid to warrior string.

    def get_commands(self):
        return {"tournament":self.tournament, "warrior":self.add_warrior}
    
    def add_warrior(self, update, context):
        if self.listening:
            self.warriors[(update.effective_user.id, update.effective_user.first_name)] = update.effective_message.text
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="There is no ongoing tournament.")

    @asynced
    def tournament(self, update, context, timeout=10):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Let the bfjoust tournament commence!")
        self.listening = True
        time.sleep(timeout)
        warriors = self.warriors
        self.reset()
        if len(warriors) < 2:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Noone joined :(")
            return
        context.bot.send_message(chat_id=update.effective_chat.id, text="The tourney is now closed for entry. Initiating battles...")
        results = self.all_fights(warriors).most_common(5)
        names = [name for ((_, name), _) in results]
        scores = [f"{name} with {points} points" for ((_, name), points) in results]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"The results are in! The winners are {', '.join(names[:-2])}, and {names[-1]}. The scores are as follows: {', '.join(scores)}.")
        self.reset()
    
    def all_fights(self, warriors: Dict[int, str]) -> Counter[str]:
        scores = colCounter({player:0 for player in warriors})
        pairs = warriors.items()
        for ((player_1, warrior_1), (player_2, warrior_2)) in [(pairs[i], pairs[j]) for i in range(len(pairs)) for j in range(i + 1, len(pairs))]:
            (res1, res2) = bfjoust.run_fight(warrior_1, warrior_2)
            scores[player_1] += res1
            scores[player_2] += res2
        return scores