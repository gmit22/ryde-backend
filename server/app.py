from flask import Flask

from middleware.middleware import users_api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(users_api)
    return app


if __name__ == "__main__":

    app = create_app()
    print("Starting server on the port 5000...")
    app.run()