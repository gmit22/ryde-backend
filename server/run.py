from app import create_app
from database.config import RunConfig

if __name__ == "__main__":

    app= create_app(RunConfig)

    print("Starting server on the port 5000...")
    app.run()