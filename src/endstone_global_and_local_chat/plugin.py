from endstone.plugin import Plugin
from endstone.event import PlayerChatEvent, event_handler
from endstone import ColorFormat as cf

class GlobalAndLocalChat(Plugin):
    api_version = "0.11"

    def on_enable(self):
        self.register_events(self)