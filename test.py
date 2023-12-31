import os
import scripts
from crawler import dantri
from config import Config

HOST = Config.HOST
PORT = Config.PORT
DB_NAME = Config.DB_NAME
COLLECTION_NAME = Config.COLLECTION_NAME
URL = Config.URL

client = scripts.get_connection_to_db(HOST, PORT)
database = client[DB_NAME]
collection = database[COLLECTION_NAME]

response = dantri.get_connection(URL, Config.HEADERS, Config.TIMEOUT)
info = dantri.get_info_from_an_article(response)
collection.insert_one(info)


