import requests
from requests import RequestException

ROOT_URL = r'https://dantri.com.vn'

def check_is_next_page_from_root(url: str):
    return not ('https' in url)

def check_time_out(timeout: int):
    if timeout <= 0:
        raise ValueError("Timeout should be positive")

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
    check_time_out(timeout)
    response = requests.get(url=url, headers=headers, timeout=timeout)
    if response.status_code != 200:
        raise RequestException("The connection to this web has failed. Please try to connect again.")
    return response