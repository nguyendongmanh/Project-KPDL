import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))

class Config:
    URL = os.getenv('URL')
    TIMEOUT = int(os.getenv('TIMEOUT'))
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))
    DB_NAME = os.getenv('DB_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    
    