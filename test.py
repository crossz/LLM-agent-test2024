import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app import app, db, Team, Player
from flask_restx import inputs

class TestNBAStatsAPI(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试会话
        self.session = Session(db.engine)

    def tearDown(self):
        self.session.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_teams(self):
        # 在测试会话中添加球队数据
        team1 = Team(name='Team 1', points_scored=100, rebounds=50, assists=30)
        team2 = Team(name='Team 2', points_scored=90, rebounds=45, assists=25)
        self.session.add_all([team1, team2])
        self.session.commit()

        with app.test_client() as client:
            response = client.get('/nba_stats/teams')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], 'Team 1')
            self.assertEqual(data[0]['points_scored'], 100)
            self.assertEqual(data[1]['name'], 'Team 2')
            self.assertEqual(data[1]['points_scored'], 90)

    def test_get_team_detail(self):
        # 在测试会话中添加球队数据
        team = Team(name='Team 3', points_scored=80, rebounds=40, assists=20)
        self.session.add(team)
        self.session.commit()

        with app.test_client() as client:
            response = client.get('/nba_stats/teams/1')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['name'], 'Team 3')
            self.assertEqual(data['points_scored'], 80)
            self.assertEqual(data['rebounds'], 40)
            self.assertEqual(data['assists'], 20)

    def test_get_players(self):
        # 在测试会话中添加球队和球员数据
        team = Team(name='Team 4')
        player1 = Player(name='Player 1', team_id=team.id, points=20, rebounds=10, assists=5)
        player2 = Player(name='Player 2', team_id=team.id, points=15, rebounds=8, assists=3)
        self.session.add_all([team, player1, player2])
        self.session.commit()

        with app.test_client() as client:
            response = client.get('/nba_stats/players')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], 'Player 1')
            self.assertEqual(data[0]['points'], 20)
            self.assertEqual(data[1]['name'], 'Player 2')
            self.assertEqual(data[1]['points'], 15)

    def test_get_player_detail(self):
        # 在测试会话中添加球队和球员数据
        team = Team(name='Team 5')
        player = Player(name='Player 3', team_id=team.id, points=25, rebounds=12, assists=6)
        self.session.add_all([team, player])
        self.session.commit()

        with app.test_client() as client:
            response = client.get('/nba_stats/players/1')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['name'], 'Player 3')
            self.assertEqual(data['points'], 25)
            self.assertEqual(data['rebounds'], 12)
            self.assertEqual(data['assists'], 6)

    def test_create_team(self):
        with app.test_client() as client:
            data = {
                'name': 'New Team',
                'points_scored': 70,
                'rebounds': 35,
                'assists': 15
            }
            response = client.post('/nba_stats/teams', json=data)
            self.assertEqual(response.status_code, 201)

            # 验证数据是否在测试会话中成功创建
            created_team = self.session.get(Team, response.json['team_id'])
            self.assertIsNotNone(created_team)
            self.assertEqual(created_team.name, 'New Team')
            self.assertEqual(created_team.points_scored, 70)
            self.assertEqual(created_team.rebounds, 35)
            self.assertEqual(created_team.assists, 15)

    def test_update_team(self):
        # 在测试会话中添加球队数据
        team = Team(name='Team to Update', points_scored=60, rebounds=30, assists=10)
        self.session.add(team)
        self.session.commit()

        with app.test_client() as client:
            data = {
                'name': 'Updated Team Name',
                'points_scored': 75,
                'rebounds': 38,
                'assists': 18
            }
            response = client.put('/nba_stats/teams/1', json=data)
            self.assertEqual(response.status_code, 200)

            # 验证数据在测试会话中是否成功更新
            updated_team = self.session.get(Team, 1)
            self.assertEqual(updated_team.name, 'Updated Team Name')
            self.assertEqual(updated_team.points_scored, 75)
            self.assertEqual(updated_team.rebounds, 38)
            self.assertEqual(updated_team.assists, 18)

    def test_delete_team(self):
        # 在测试会话中添加球队数据
        team = Team(name='Team to Delete', points_scored=50, rebounds=25, assists=5)
        self.session.add(team)
        self.session.commit()

        with app.test_client() as client:
            response = client.delete('/nba_stats/teams/1')
            self.assertEqual(response.status_code, 200)

            # 验证球队在测试会话中是否已被删除
            deleted_team = self.session.get(Team, 1)
            self.assertIsNone(deleted_team)

    def test_create_player(self):
        # 在测试会话中添加球队数据
        team = Team(name='Team for Player')
        self.session.add(team)
        self.session.commit()

        with app.test_client() as client:
            data = {
                'name': 'New Player',
                'team_id': team.id,
                'points': 18,
                'rebounds': 9,
                'assists': 4
            }
            response = client.post('/nba_stats/players', json=data)
            self.assertEqual(response.status_code, 201)

            # 验证数据是否在测试会话中成功创建
            created_player = self.session.get(Player, response.json['player_id'])
            self.assertIsNotNone(created_player)
            self.assertEqual(created_player.name, 'New Player')
            self.assertEqual(created_player.team_id, team.id)
            self.assertEqual(created_player.points, 18)
            self.assertEqual(created_player.rebounds, 9)
            self.assertEqual(created_player.assists, 4)

    def test_update_player(self):
        # 在测试会话中添加球队和球员数据
        team = Team(name='Team for Updating Player')
        player = Player(name='Player to Update', team_id=team.id, points=12, rebounds=6, assists=2)
        self.session.add_all([team, player])
        self.session.commit()

        with app.test_client() as client:
            data = {
                'name': 'Updated Player Name',
                'points': 15,
                'rebounds': 8,
                'assists': 3
            }
            response = client.put('/nba_stats/players/1', json=data)
            self.assertEqual(response.status_code, 200)

            # 验证数据在测试会话中是否成功更新
            updated_player = self.session.get(Player, 1)
            self.assertEqual(updated_player.name, 'Updated Player Name')
            self.assertEqual(updated_player.points, 15)
            self.assertEqual(updated_player.rebounds, 8)
            self.assertEqual(updated_player.assists, 3)

    def test_delete_player(self):
        # 在测试会话中添加球队和球员数据
        team = Team(name='Team for Deleting Player')
        player = Player(name='Player to Delete', team_id=team.id, points=10, rebounds=5, assists=1)
        self.session.add_all([team, player])
        self.session.commit()

        with app.test_client() as client:
            response = client.delete('/nba_stats/players/1')
            self.assertEqual(response.status_code, 200)

            # 验证球员在测试会话中是否已被删除
            deleted_player = self.session.get(Player, 1)
            self.assertIsNone(deleted_player)

if __name__ == '__main__':
    unittest.main()
