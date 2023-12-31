import time
import scripts
from tqdm import tqdm
from config import Config
from crawler import dantri
from collections import defaultdict

HOST = Config.HOST
PORT = Config.PORT
DB_NAME = Config.DB_NAME
COLLECTION_NAME = Config.COLLECTION_NAME
ROOT_URL = Config.ROOT_URL
HEADERS = Config.HEADERS
TIMEOUT = Config.TIMEOUT

def main():
    # connect to database
    client = scripts.get_connection_to_db(HOST, PORT)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    topics = dantri.get_topics(root_url=ROOT_URL, headers=HEADERS, timeout=TIMEOUT)
    # get all article's link in each pagination
    i = 1
    articles_by_topic = defaultdict(list)
    for main_topic, sub_topics in topics.items():
        print(main_topic)
        for sub_topic in sub_topics:
            articles_links = dantri.get_articles_by_topic(sub_topic, headers=Config.HEADERS, timeout=Config.TIMEOUT)
            articles_by_topic[main_topic] += articles_links
            time.sleep(1)
        time.sleep(1)
    
    # get article's information    
    articles_content_by_topic = defaultdict(list)
    for topic, articles in articles_by_topic.items():
        print(topic)
        for article_link in tqdm(articles):
            articles_content_by_topic[topic].append(dantri.get_info_from_an_article(article_link, headers=Config.HEADERS, timeout=Config.TIMEOUT))
            time.sleep(0.5)
        time.sleep(1)
    
    collection.insert_one(articles_content_by_topic)

if __name__ == '__main__':
    main()