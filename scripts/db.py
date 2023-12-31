from pymongo import MongoClient

def get_connection_to_db(host: str, port: int):
    CONNECTION_STR = f'''mongodb://{host}:{port}'''
    client = MongoClient(CONNECTION_STR)
    
    return client