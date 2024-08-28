from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from models import db, Player

ns = Namespace('players', description='NBA 球员相关操作')

player_model = ns.model('Player', {
    'name': fields.String(required=True),
    'team_id': fields.Integer(required=True),
    'points': fields.Integer(required=True),
    'rebounds': fields.Integer(required=True),
    'assists': fields.Integer(required=True)
})

@ns.route('/', strict_slashes=False)
class PlayerList(Resource):
    """
    此接口用于获取所有球员的列表
    """
    @ns.doc('get_all_players')
    def get(self):
        # players = db.session.scalars(db.select(Player)).all()
        players = Player.query.all()
        return [{'id': player.id, 'name': player.name, 'team_id': player.team_id, 'points': player.points, 'rebounds': player.rebounds, 'assists': player.assists} for player in players]
        # with Session(db.engine) as session:
        #     players = session.scalars(db.select(Player)).all()
        #     return [{'id': player.id, 'name': player.name, 'team_id': player.team_id, 'points': player.points, 'rebounds': player.rebounds, 'assists': player.assists} for player in players]

    """
    此接口用于创建新的球员
    """
    @ns.doc('create_player')
    @ns.expect(player_model)
    def post(self):
        data = ns.payload
        # player = Player(name=data['name'], team_id=data['team_id'], points=data['points'], rebounds=data['rebounds'], assists=data['assists'])
        player = Player(**data)
        db.session.add(player)
        db.session.commit()
        return {'message': 'Player created successfully', 'player_id': player.id}, 201
        # with Session(db.engine) as session:
        #     player = Player(name=data['name'], team_id=data['team_id'], points=data['points'], rebounds=data['rebounds'], assists=data['assists'])
        #     session.add(player)
        #     session.commit()
        #     return {'message': 'Player created successfully', 'player_id': player.id}, 201


@ns.route('/<int:player_id>')
class PlayerDetail(Resource):
    """
    此接口用于根据 ID 获取单个球员的详细信息
    """
    @ns.doc('get_player_by_id')
    def get(self, player_id):
        # player = Player.query.get(player_id)
        player = db.session.get(Player, player_id)
        if player:
            return {'id': player.id, 'name': player.name, 'team_id': player.team_id, 'points': player.points, 'rebounds': player.rebounds, 'assists': player.assists}
        else:
            ns.abort(404, "Player not found")

        # with Session(db.engine) as session:
        #     player = session.get(Player, player_id)
        #     if player:
        #         return {'id': player.id, 'name': player.name, 'team_id': player.team_id, 'points': player.points, 'rebounds': player.rebounds, 'assists': player.assists}
        #     else:
        #         ns.abort(404, "Player not found")

    """
    此接口用于根据 ID 更新单个球员的信息
    """
    @ns.doc('update_player_by_id')
    def put(self, player_id):
        # player = Player.query.get(player_id)
        player = db.session.get(Player, player_id)
        if not player:
            ns.abort(404, "Player not found")
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
        db.session.commit()
        return {'message': 'Player updated successfully'}
        # with Session(db.engine) as session:
        #     player = session.get(Player, player_id)
        #     if not player:
        #         ns.abort(404, "Player not found")
        #     data = ns.payload
        #     if data.get('name'):
        #         player.name = data['name']
        #     if data.get('team_id'):
        #         player.team_id = data['team_id']
        #     if data.get('points'):
        #         player.points = data['points']
        #     if data.get('rebounds'):
        #         player.rebounds = data['rebounds']
        #     if data.get('assists'):
        #         player.assists = data['assists']
        #     session.commit()
        #     return {'message': 'Player updated successfully'}

    """
    此接口用于根据 ID 删除球员
    """
    @ns.doc('delete_player_by_id')
    def delete(self, player_id):
        # player = Player.query.get(player_id)
        player = db.session.get(Player, player_id)
        if not player:
            ns.abort(404, "Player not found")
        db.session.delete(player)
        db.session.commit()
        return {'message': 'Player deleted successfully'}
        # with Session(db.engine) as session:
        #     player = session.get(Player, player_id)
        #     if not player:
        #         ns.abort(404, "Player not found")
        #     session.delete(player)
        #     session.commit()
        #     return {'message': 'Player deleted successfully'}
