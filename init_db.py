import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjamie


def get_quotes():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(
        'https://bookroo.com/quotes/getting-things-done', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    div_quotes = soup.select('div.css-eez2cp')
    quotes = (quote.text for quote in div_quotes)
    return quotes

# for문 돌릴 필요 없이 바로 DB에 궈궈싱 해버리는 거 !!!
def insert_all():
    quotes = get_quotes()
    db.quotes.insert_many([{'quote': i} for i in quotes])

def read_quote():
    quote = list(db.quotes.aggregate([{'$sample': {'size':1}}, {'$project':{'_id':0}}]))
    print(quote)

# insert_all()
read_quote()

