from endstone.plugin import Plugin
from endstone.event import PlayerChatEvent, event_handler
from endstone import Player
from endstone import ColorFormat as cf
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from typing import cast

class GlobalAndLocalChat(Plugin):
    api_version = "0.11"

    def install(self):
        folder = Path(self.data_folder)
        folder.mkdir(parents=True, exist_ok=True)
        cfg_path = folder / "config.yml"
        self.yml = YAML()
        self.yml.version = (1, 2)
        self.yml.preserve_quotes = True
        
        defaults = [
            ("local_chat_radius", 100, "Radius in blocks for local chat"),
            ("colors.global_label", "GREEN", "Color for GLOBAL label (ColorFormat enum name https://endstone.dev/latest/reference/python/misc/#endstone.ColorFormat)"),
            ("colors.local_label", "YELLOW", "Color for LOCAL label (ColorFormat enum name https://endstone.dev/latest/reference/python/misc/#endstone.ColorFormat)"),
            ("labels.global", "GLOBAL", "Label for global chat"),
            ("labels.local", "LOCAL", "Label for local chat"),
            ("messages.no_one_heard", "No one heard you...", "Message when no players in radius"),
        ]
        
        if cfg_path.exists():
            with open(cfg_path, "r", encoding="utf-8") as f:
                existing = self.yml.load(f)
            if not isinstance(existing, CommentedMap):
                existing = CommentedMap(existing or {})
        else:
            existing = CommentedMap()

        for key, default, comment in defaults:
            keys = key.split(".")
            current = existing
            for i, k in enumerate(keys[:-1]):
                if k not in current:
                    current[k] = CommentedMap()
                current = current[k]
            
            if keys[-1] not in current:
                current[keys[-1]] = default
                current.yaml_add_eol_comment(comment, keys[-1])

        with open(cfg_path, "w", encoding="utf-8") as f:
            self.yml.dump(existing, f)

        self.yaml_config = dict(existing)

    def on_enable(self):
        self.install()
        
        self.local_chat_radius = cast(int, self.yaml_config.get("local_chat_radius", 100))
        
        colors = cast(dict, self.yaml_config.get("colors", {}))
        self.global_color = getattr(cf, colors.get("global_label", "GREEN"), cf.GREEN)
        self.local_color = getattr(cf, colors.get("local_label", "YELLOW"), cf.YELLOW)
        
        labels = cast(dict, self.yaml_config.get("labels", {}))
        self.global_label = labels.get("global", "GLOBAL")
        self.local_label = labels.get("local", "LOCAL")
        
        messages = cast(dict, self.yaml_config.get("messages", {}))
        self.no_one_heard_msg = messages.get("no_one_heard", "No one heard you...")
        
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
            message = f"[{self.global_color}{self.global_label}{cf.RESET}] <{event.player.name}> {message}"
            if event.message == "!":
                return
            self.server.broadcast_message(message.strip())
        else:
            recipients = self.get_players_in_radius(event.player, self.local_chat_radius)
            if len(recipients) == 0:
                event.player.send_message(f"{cf.ITALIC}{cf.GRAY}{self.no_one_heard_msg}")
                return
            message = f"[{self.local_color}{self.local_label}{cf.RESET}] <{event.player.name}> {event.message}"
            for recipient in recipients:
                recipient.send_message(message)
            event.player.send_message(message)