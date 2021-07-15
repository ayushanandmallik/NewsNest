import requests
import json
import os
import dotenv


dotenv.load_dotenv()
news_api_key= os.getenv('news_api_key')
n= requests.get(news_api_key)
content= json.loads(n.content)
articles= content['articles']

def get_news_title():
    title=[]
    for i in range(5):
        t= content['articles'][i]['title']
        title.append(t)
    return title

def get_news_source():
    source= []
    for i in range(5):
        s= content['articles'][i]['url']
        source.append(s)

    return source


