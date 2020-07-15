import importlib
import functools
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

CORE_PACKAGE = "functionality_cores."

class Bot:
    """Encodes a telegram bot with api connection and personality/functionality cores."""

    def __init__(self, persCore: dict):
        self.updater = Updater(persCore["token"], use_context=True)
        self.cores = dict()
        self.commands = dict()
        for core in persCore["fcores"]:
            self.add_core(core)
        for (mFilter, func) in [(Filters.command, "not_command"), (Filters.text, "message")]:
            self.updater.dispatcher.add_handler(MessageHandler(mFilter, functools.partial(self.catch_all, func)))
        self.updater.start_polling(clean=True)

    def add_core(self, core: str):
        print(f"Loading core {core}...", end='\r')
        try:
            self.cores[core] = getattr(importlib.import_module(CORE_PACKAGE + core), core)(self)
            for (command, callback) in self.cores[core].get_commands().items():
                self.updater.dispatcher.add_handler(CommandHandler(command, callback))
            print(f"Successfully loaded core '{core}'")
        except Exception as e:
            print(f"Failed to load core '{core}': {e}")

    def catch_all(self, func: str, update, context):
        for core in self.cores.values():
            getattr(core, func)(update, context)