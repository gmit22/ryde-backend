class RunConfig:

    MONGO_HOST = '192.168.1.37'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'rydedb'
    MONGO_URI = "mongodb+srv://gunit_ryde:gunit_ryde@ryde-cluster.pdveurs.mongodb.net/?retryWrites=true&w=majority"

class TestConfig:

    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'ryde-db'
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}"
    TESTING = True

    