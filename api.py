from resources.teams import ns as ns_teams
from resources.players import ns as ns_players

def init_api(api):
  api.add_namespace(ns_teams)
  api.add_namespace(ns_players)