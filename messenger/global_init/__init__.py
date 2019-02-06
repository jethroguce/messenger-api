from .flask_app import create_flask_app
from flask_restful import Api
from flask_cors import CORS

app = create_flask_app()
api = Api(app)
CORS(app)
