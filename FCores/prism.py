# Might not conform to privacy legislation, do not use in production environment before verifying with a legal expert.

import json
from functools import wraps
import mysql.connector
from FunctionalityCore import FCore

CREDENTIALS = "Data/dbcredentials.json"
USERS = "users"
CHATS = "chats"
PREFIX = "d" # To prevent collisions between column fields and object attributes.

def log(func):
    """Decorator for command functions. When applied, any user that uses the command, as well as any chat the command is used in, will be logged."""
    @wraps(func)
    def inner(self, update, context):
        self.cores["prism"].log_user(update.effective_user)
        if update.effective_user.id != update.effective_chat.id: # If the chat is not a one-to-one chat with the user.
            self.cores["prism"].log_chat(update.effective_chat)
        func(self, update, context)
    return inner

class prism(FCore):
    """Provides user identity persistence through an sql database."""

    def __init__(self, bot):
        super().__init__(bot)
        with open(CREDENTIALS, 'r') as credFile:
            creds = json.loads(credFile.read())
        self.db = mysql.connector.connect(host=creds["host"], user=creds["user"], database=creds["database"], passwd=creds["passwd"])
        self.cursor = self.db.cursor()

    def log_user(self, user):
        attributes = ["id", "username", "first_name", "last_name"]
        values = [("\"{}\"" if isinstance(attribute, str) else "{}").format(getattr(user, attribute)) for attribute in attributes]
        self.cursor.execute(f"REPLACE INTO {USERS} ({', '.join([PREFIX + attr for attr in attributes])}) VALUES ({', '.join(values)});")
        self.db.commit()
    
    def log_chat(self, chat):
        attributes = ["id", "type", "title", "description"]
        values = [("\"{}\"" if isinstance(attribute, str) else "{}").format(getattr(chat, attribute)) for attribute in attributes]
        self.cursor.execute(f"REPLACE INTO {CHATS} ({', '.join([PREFIX + attr for attr in attributes])}) VALUES ({', '.join(values)});")
        self.db.commit()
    
    def by_userid(self, id: int) -> tuple:
        """Return the row corresponding to the user id, or None if the id is not registered."""
        self.cursor.execute(f"SELECT * FROM {USERS} WHERE {PREFIX}id = {id};")
        return self.cursor.fetchone()
    
    def by_username(self, username: str) -> tuple:
        """Return the row corresponding to the username, or None if the username is not registered."""
        self.cursor.execute(f"SELECT * FROM {USERS} WHERE {PREFIX}username = {username};")
        return self.cursor.fetchone()
    
    def by_chatid(self, id: int) -> tuple:
        """Return the row corresponding to the chat id, or None if the id is not registered."""
        self.cursor.execute(f"SELECT * FROM {CHATS} WHERE {PREFIX}id = {id};")
        return self.cursor.fetchone()
    
    def by_chat_title(self, title: str) -> tuple:
        """Return the row corresponding to the chat title, or None if the chat title is not registered."""
        self.cursor.execute(f"SELECT * FROM {CHATS} WHERE {PREFIX}title = {title};")
        return self.cursor.fetchone()