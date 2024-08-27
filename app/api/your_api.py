from flask_restx import Namespace, Resource

api = Namespace('hello_api', description='Hello API')

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
