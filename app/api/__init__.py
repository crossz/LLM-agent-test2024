from .team_namespace import team_namespace
from .player_namespace import player_namespace
from .your_api import api as helloapi

def init_api(api):
    api.add_namespace(team_namespace)
    api.add_namespace(player_namespace)
    api.add_namespace(helloapi)