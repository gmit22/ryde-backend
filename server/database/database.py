import pymongo

def init_connection(connection_url, db_name):
    client = pymongo.MongoClient(connection_url)
    db = client.get_database(db_name)    
    return db
