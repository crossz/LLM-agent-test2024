from flask_restx import Namespace, Resource, fields
from sqlalchemy.orm import Session
from models import db, Team

ns = Namespace('teams', description='NBA 球队相关操作')

team_model = ns.model('Team', {
    'name': fields.String(required=True),
    'points_scored': fields.Integer(required=True),
    'rebounds': fields.Integer(required=True),
    'assists': fields.Integer(required=True)
})

@ns.route('/', strict_slashes=False)
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



@ns.route('/<int:team_id>')
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
                ns.abort(404, "Team not found")

    """
    此接口用于根据 ID 更新单个球队的信息
    """
    @ns.doc('update_team_by_id')
    def put(self, team_id):
        with Session(db.engine) as session:
            team = session.get(Team, team_id)
            if not team:
                ns.abort(404, "Team not found")
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
                ns.abort(404, "Team not found")
            session.delete(team)
            session.commit()
            return {'message': 'Team deleted successfully'}
