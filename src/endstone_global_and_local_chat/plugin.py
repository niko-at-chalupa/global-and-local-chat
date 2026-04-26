from endstone.plugin import Plugin
from endstone.event import PlayerChatEvent, event_handler
from endstone import Player
from endstone import ColorFormat as cf

class GlobalAndLocalChat(Plugin):
    api_version = "0.11"

    def on_enable(self):
        self.register_events(self)

    def get_players_in_radius(self, player: Player, radius: int) -> list[Player]:
        nearby_players = []
        
        for other_player in self.server.online_players:
            if other_player == player:
                continue
            
            if (abs(other_player.location.x - player.location.x) <= radius and
                abs(other_player.location.y - player.location.y) <= radius and
                abs(other_player.location.z - player.location.z) <= radius):
                nearby_players.append(other_player)
        
        return nearby_players

    @event_handler
    def on_player_chat(self, event: PlayerChatEvent):
        event.cancel()
        
        message = event.message

        if message[0] == "!":
            message = message[1:]
            message = f"[{cf.GREEN}GLOBAL{cf.RESET}] <{event.player.name}> {message}"
            self.server.broadcast_message(message)
        else:
            recipients = self.get_players_in_radius(event.player, 100)
            if len(recipients) == 0:
                event.player.send_message(f"{cf.ITALIC}{cf.GRAY}No one heard you...")
                return
            message = f"[{cf.YELLOW}LOCAL{cf.RESET}] <{event.player.name}> {event.message}"
            for recipient in recipients:
                recipient.send_message(message)