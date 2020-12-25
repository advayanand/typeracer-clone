import urllib.request
import json
import random

_BOOK_TITLES_FILE = 'novel_titles.txt'
_QUOTES_BASE_URL = 'https://goodquotesapi.herokuapp.com/title/'

def get_random_book_title() -> str:
    file = open(_BOOK_TITLES_FILE)
    titles = file.readlines()

    return random.choice(titles).rstrip('\n')

def get_random_quote() -> (str, str, str):
    book = get_random_book_title()
    url = _QUOTES_BASE_URL + '+'.join(book.split())
    obj = get_json_from_url(url)

    num_pages = obj['total_pages']
    while True:
        random_page = random.randint(1, num_pages)
        if random_page != 1:
            url = _QUOTES_BASE_URL + '+'.join(book.split()) + '?page=' + str(random_page)
            obj = get_json_from_url(url)

        quotes_list = obj['quotes']
        quotes_list = [i for i in quotes_list if i['publication'] is not None and i['publication'].lower() == book.lower()]
        if len(quotes_list) > 0:
            break
    quote = random.choice(quotes_list)
    return quote['quote'], quote['author'], quote['publication']


def get_json_from_url(url: str) -> dict:
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode(encoding='utf-8')
    return json.loads(data)

