import requests
from requests import RequestException

def check_is_next_page_from_root(url: str):
    return not ('https' in url)

def get_connection(url: str, headers: dict, timeout=10):
    '''
    Get connection to web by url
    
    Args:
        * `url`: The url of web to crawl
        * `header`: Set header to requests, it helps avoid bot detection
        * `timeout`: The maximum of time to requests
        
    Return:
        * `response`: The response after requesting consists of *status_code*, *text* 
    '''
    if timeout <= 0:
        raise ValueError("Timeout value should be positive")
    response = requests.get(url=url, headers=headers, timeout=timeout)
    if response.status_code != 200:
        raise RequestException("The connection to this web has failed. Please try to connect again.")
    return response