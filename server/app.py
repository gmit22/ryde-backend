from flask import Flask
from middleware.middleware import users_api
from database.database import init_connection
import logging

def create_app(config):
    app = Flask(__name__)
 
    logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 
    app.register_blueprint(users_api)
    app.config.from_object(config)
    
    connection_url, db = app.config.get("MONGO_URI"), app.config.get("MONGO_DBNAME")
    app.db = init_connection(connection_url, db)
    
    @app.route('/')
    def serve():
        return "<h1>Welcome!<h1>"
    
    return app
