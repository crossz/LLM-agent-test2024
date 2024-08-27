from flask_restx import Namespace, Resource
from app.models import Player

player_namespace = Namespace('player', description='NBA player operations')

@player_namespace.route('/')
class PlayerList(Resource):
    def get(self):
        players = Player.query.all()
        return [{'id': player.id, 'name': player.name, 'city': player.city} for player in players]


