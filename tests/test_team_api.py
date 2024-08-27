import unittest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from flask_testing import TestCase
from app import create_app, db
from app.models import Team

class TestTeamAPI(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('app.models.Team.query')
    def test_get_teams(self, mock_query):
        # 创建一个 mock 的球队列表
        mock_teams = [Team(name='Team 1', city='City 1'), Team(name='Team 2', city='City 2')]
        mock_query.all.return_value = mock_teams

        response = self.client.get('/team/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['name'], 'Team 1')
        self.assertEqual(response.json[1]['name'], 'Team 2')

if __name__ == '__main__':
    unittest.main()
