# Might not conform to privacy legislation, do not use in production environment before verifying with a legal expert.

import re
import json
from functools import wraps
import mysql.connector
from functionality_core import FCore

CREDENTIALS = "Data/dbcredentials.json"
USERS = "users"
CHATS = "chats"
PREFIX = "d" # To prevent collisions between column fields and object attributes.

def log(func):
    """Decorator for command functions. When applied, any user that uses the command, as well as any chat the command is used in, will be logged."""
    @wraps(func)
    def inner(self, update, context):
        self.bot.cores["prism"].log_user(update.effective_user)
        if update.effective_user.id != update.effective_chat.id: # If the chat is not a one-to-one chat with the user.
            self.bot.cores["prism"].log_chat(update.effective_chat)
        func(self, update, context)
    return inner

class prism(FCore):
    """Provides user identity persistence through an sql database."""

    def __init__(self, bot):
        super().__init__(bot)
        with open(CREDENTIALS, 'r') as credFile:
            creds = json.loads(credFile.read())
        self.db = mysql.connector.connect(host=creds["host"], user=creds["user"], database=creds["database"], passwd=creds["passwd"])
        self.cursor = self.db.cursor(dictionary=True)
    
    def get_commands(self) -> dict:
        return {"hello":self.identify}
    
    @log
    def identify(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello there {update.effective_user.first_name}, I'm a bot.")

    def log_user(self, user):
        attributes = ["id", "username", "first_name", "last_name"]
        values = [("\"{}\"" if isinstance(attribute, str) else "{}").format(self.clean(str(getattr(user, attribute)))) for attribute in attributes]
        self.cursor.execute(f"REPLACE INTO {USERS} ({', '.join([PREFIX + attr for attr in attributes])}) VALUES ({', '.join(values)});")
        self.db.commit()
    
    def log_chat(self, chat):
        attributes = ["id", "type", "title", "description"]
        values = [("\"{}\"" if isinstance(attribute, str) else "{}").format(self.clean(str(getattr(chat, attribute)))) for attribute in attributes]
        self.cursor.execute(f"REPLACE INTO {CHATS} ({', '.join([PREFIX + attr for attr in attributes])}) VALUES ({', '.join(values)});")
        self.db.commit()
    
    def by_userid(self, id: int) -> tuple:
        """Return the row corresponding to the user id, or None if the id is not registered."""
        return self.get_one(f"SELECT * FROM {USERS} WHERE {PREFIX}id = {id};")
    
    def by_username(self, username: str) -> tuple:
        """Return the row corresponding to the username, or None if the username is not registered."""
        return self.get_one(f"SELECT * FROM {USERS} WHERE {PREFIX}username = \"{self.clean(username)}\";")
    
    def by_chatid(self, id: int) -> tuple:
        """Return the row corresponding to the chat id, or None if the id is not registered."""
        return self.get_one(f"SELECT * FROM {CHATS} WHERE {PREFIX}id = {id};")
    
    def by_chat_title(self, title: str) -> tuple:
        """Return the row corresponding to the chat title, or None if the chat title is not registered."""
        return self.get_one(f"SELECT * FROM {CHATS} WHERE {PREFIX}title = \"{self.clean(title)}\";")
    
    # Utility
    def get_one(self, query: str) -> dict:
        """Return the first result of a query."""
        self.cursor.execute(query)
        return self.strip_prefix(self.cursor.fetchone())

    def strip_prefix(self, data: dict) -> dict:
        """Return a dictionary with every key stripped of its prefix."""
        return {key[len(PREFIX):]:val for (key, val) in data.items()} if data else data
    
    def clean(self, target: str) -> str:
        """Escape a string to be ready for use in an sql query.
        WARNING: not fit for LIKE statements, since wildcards remain unaffected. Add a seperate escape for those."""
        return re.sub(r"([\\\"'])", r"\\\1", target)