import importlib
from telegram.ext import Updater, CommandHandler

CORE_PACKAGE = "FCores."

class Bot:
    """Encodes a telegram bot with api connection and personality/functionality cores."""

    def __init__(self, persCore: dict):
        self.updater = Updater(persCore["token"], use_context=True)
        self.cores = dict()
        self.commands = dict()
        for core in persCore["fcores"]:
            self.add_core(core)
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

    def catch_all(self, update, context):
        for core in self.cores.values():
            core.catch_all(update, context)