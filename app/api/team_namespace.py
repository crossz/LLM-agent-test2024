from flask_restx import Namespace, Resource
from app.models import Team

team_namespace = Namespace('team', description='NBA Team operations')

@team_namespace.route('/')
class TeamList(Resource):
    def get(self):
        teams = Team.query.all()
        return [{'id': team.id, 'name': team.name, 'city': team.city} for team in teams]
