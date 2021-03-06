class FCore:
    """Provides the basis for a functionality core with default implementations."""

    def __init__(self, bot):
        self.bot = bot
    
    def get_commands(self) -> dict:
        """Return a dictionary of all commands and their corresponding callbacks."""
        return dict()

    def terminal_control(self):
        """Provide in-terminal functionality after being given control."""
        print("This core does not have terminal functionality.")
    
    def not_command(self, update, context):
        """Called if the bot recieves an unrecognised command."""
        pass
    
    def message(self, update, context):
        """Called if the bot recieves a message."""
        pass