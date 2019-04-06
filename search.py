import subprocess
import time
import threading
from elasticsearch import Elasticsearch
import newspaper
from flask import Flask
app = Flask(__name__)

def start_server(): subprocess.call(["elasticsearch-6.7.1/bin/elasticsearch"])
    #Popen(subprocess.call(["elasticsearch-6.7.1/bin/elasticsearch"]))

t = threading.Thread(target=start_server)
t.start()

time.sleep(15)

es = Elasticsearch()

paper = newspaper.build('https://www.nytimes.com/section/politics')
arts = []
print(paper.articles)
for article in paper.articles:
    print("here")
    article.download()
    article.parse()
    res = es.index(index="articles", doc_type='news', body={'picture': article.top_image, 'title': article.title, 'text': article.text, 'link': article.url})
es.indices.refresh(index="articles")

#this is the repeatable thing for search
res = es.search(index="articles", size=100, body={"query": {"multi_match": {"query": "Trump", "fields":['text', 'title']}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print(hit['_source']['title'])
