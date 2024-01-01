import time
import scripts
import argparse
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

parser = argparse.ArgumentParser()

parser.add_argument("-w", "--website", default="dantri", help='''
                    Choose website which you want to get articles\n
                    There are 2 options:\n
                        + dantri
                        + vnexpress
                    ''')

def get_all_from_dantri(root_url: str, headers: dict, timeout=10):
    if timeout <= 0:
        raise ValueError("Timeout should be positive")
    
    topics = dantri.get_topics(root_url=root_url, headers=headers, timeout=timeout)
    # get all article's link in each pagination
    articles_by_topic = defaultdict(list)
    for main_topic, sub_topics in topics.items():
        print(main_topic)
        for sub_topic in sub_topics:
            articles_links = dantri.get_articles_by_topic(sub_topic, headers=headers, timeout=timeout)
            articles_by_topic[main_topic] += articles_links
            time.sleep(1)
        time.sleep(1)
    
    # get article's information    
    articles_content_by_topic = defaultdict(list)
    for topic, articles in articles_by_topic.items():
        print(topic)
        for article_link in tqdm(articles):
            articles_content_by_topic[topic].append(dantri.get_info_from_an_article(article_link, headers=headers, timeout=timeout))
            time.sleep(0.5)
        time.sleep(1)
    return articles_content_by_topic

def get_all_from_vnexpress(root_url: str, headers: dict, timeout=10):
    pass

def main():
    args = parser.parse_args()
    
    # connect to database
    client = scripts.get_connection_to_db(HOST, PORT)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    if args.website == 'dantri':
        articles_content_by_topic = get_all_from_dantri(ROOT_URL, HEADERS, TIMEOUT)
    elif args.website == 'vnexpress':
        get_all_from_vnexpress(ROOT_URL, HEADERS, TIMEOUT)
        
    # collection.insert_one(articles_content_by_topic)

if __name__ == '__main__':
    main()
    
