from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///nba.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 球队模型
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    points_scored = db.Column(db.Integer)
    rebounds = db.Column(db.Integer)
    assists = db.Column(db.Integer)

# 球员模型
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    points = db.Column(db.Integer)
    rebounds = db.Column(db.Integer)
    assists = db.Column(db.Integer)

api = Api(app)

# API 命名空间
ns = api.namespace('nba_stats', description='NBA 赛事统计相关操作')

# 球队模型的字段定义
team_model = ns.model('Team', {
    'name': fields.String(required=True),
    'points_scored': fields.Integer(required=True),
    'rebounds': fields.Integer(required=True),
    'assists': fields.Integer(required=True)
})

# 球员模型的字段定义
player_model = ns.model('Player', {
    'name': fields.String(required=True),
    'team_id': fields.Integer(required=True),
    'points': fields.Integer(required=True),
    'rebounds': fields.Integer(required=True),
    'assists': fields.Integer(required=True)
})

@ns.route('/teams')
class TeamList(Resource):
    """
    此接口用于获取所有球队的列表
    """
    @ns.doc('get_all_teams')
    def get(self):
        with Session(db.engine) as session:
            teams = session.scalars(db.select(Team)).all()
            return [{'id': team.id, 'name': team.name, 'points_scored': team.points_scored, 'rebounds': team.rebounds, 'assists': team.assists} for team in teams]

    """
    此接口用于创建新的球队
    """
    @ns.doc('create_team')
    @ns.expect(team_model)
    def post(self):
        data = ns.payload
        with Session(db.engine) as session:
            team = Team(name=data['name'], points_scored=data['points_scored'], rebounds=data['rebounds'], assists=data['assists'])
            session.add(team)
            session.commit()
            return {'message': 'Team created successfully', 'team_id': team.id}, 201

@ns.route('/teams/<int:team_id>')
class TeamDetail(Resource):
    """
    此接口用于根据 ID 获取单个球队的详细信息
    """
    @ns.doc('get_team_by_id')
    def get(self, team_id):
        with Session(db.engine) as session:
            team = session.get(Team, team_id)
            if team:
                return {'id': team.id, 'name': team.name, 'points_scored': team.points_scored, 'rebounds': team.rebounds, 'assists': team.assists}
            else:
                api.abort(404, "Team not found")

    """
    此接口用于根据 ID 更新单个球队的信息
    """
    @ns.doc('update_team_by_id')
    def put(self, team_id):
        with Session(db.engine) as session:
            team = session.get(Team, team_id)
            if not team:
                api.abort(404, "Team not found")
            data = ns.payload
            if data.get('name'):
                team.name = data['name']
            if data.get('points_scored'):
                team.points_scored = data['points_scored']
            if data.get('rebounds'):
                team.rebounds = data['rebounds']
            if data.get('assists'):
                team.assists = data['assists']
            session.commit()
            return {'message': 'Team updated successfully'}

    """
    此接口用于根据 ID 删除球队
    """
    @ns.doc('delete_team_by_id')
    def delete(self, team_id):
        with Session(db.engine) as session:
            team = session.get(Team, team_id)
            if not team:
                api.abort(404, "Team not found")
            session.delete(team)
            session.commit()
            return {'message': 'Team deleted successfully'}

@ns.route('/players')
class PlayerList(Resource):
    """
    此接口用于获取所有球员的列表
    """
    @ns.doc('get_all_players')
    def get(self):
        with Session(db.engine) as session:
            players = session.scalars(db.select(Player)).all()
            return [{'id': player.id, 'name': player.name, 'team_id': player.team_id, 'points': player.points, 'rebounds': player.rebounds, 'assists': player.assists} for player in players]

    """
    此接口用于创建新的球员
    """
    @ns.doc('create_player')
    @ns.expect(player_model)
    def post(self):
        data = ns.payload
        with Session(db.engine) as session:
            player = Player(name=data['name'], team_id=data['team_id'], points=data['points'], rebounds=data['rebounds'], assists=data['assists'])
            session.add(player)
            session.commit()
            return {'message': 'Player created successfully', 'player_id': player.id}, 201

@ns.route('/players/<int:player_id>')
class PlayerDetail(Resource):
    """
    此接口用于根据 ID 获取单个球员的详细信息
    """
    @ns.doc('get_player_by_id')
    def get(self, player_id):
        with Session(db.engine) as session:
            player = session.get(Player, player_id)
            if player:
                return {'id': player.id, 'name': player.name, 'team_id': player.team_id, 'points': player.points, 'rebounds': player.rebounds, 'assists': player.assists}
            else:
                api.abort(404, "Player not found")

    """
    此接口用于根据 ID 更新单个球员的信息
    """
    @ns.doc('update_player_by_id')
    def put(self, player_id):
        with Session(db.engine) as session:
            player = session.get(Player, player_id)
            if not player:
                api.abort(404, "Player not found")
            data = ns.payload
            if data.get('name'):
                player.name = data['name']
            if data.get('team_id'):
                player.team_id = data['team_id']
            if data.get('points'):
                player.points = data['points']
            if data.get('rebounds'):
                player.rebounds = data['rebounds']
            if data.get('assists'):
                player.assists = data['assists']
            session.commit()
            return {'message': 'Player updated successfully'}

    """
    此接口用于根据 ID 删除球员
    """
    @ns.doc('delete_player_by_id')
    def delete(self, player_id):
        with Session(db.engine) as session:
            player = session.get(Player, player_id)
            if not player:
                api.abort(404, "Player not found")
            session.delete(player)
            session.commit()
            return {'message': 'Player deleted successfully'}

if __name__ == '__main__':
    app.run(debug=True)
