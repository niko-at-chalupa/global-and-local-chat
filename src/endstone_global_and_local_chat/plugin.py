from endstone.plugin import Plugin
from endstone.event import PlayerChatEvent, event_handler
from endstone import ColorFormat as cf

class GlobalAndLocalChat(Plugin):
    api_version = "0.11"

    def on_enable(self):
        self.register_events(self)

    @event_handler
    def on_player_chat(self, event: PlayerChatEvent):
        event.cancel()
        
        message = event.message

        if message[0] == "!":
            message = message[1:]
            message = f"[{cf.GREEN}GLOBAL{cf.RESET}] <{event.player.name}> {message}"
            self.server.broadcast_message(message)
        else:
            event.player.send_message(f"{cf.ITALIC}{cf.GRAY}No one heard you...")