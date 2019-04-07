import subprocess
import threading
import time
from elasticsearch import Elasticsearch
import newspaper
from flask import request, Flask
import json
from newsapi import NewsApiClient
import time
import datetime
app = Flask(__name__)

#this is the repeatable thing for search
@app.route('/query', methods = ['GET'])
def query():
    search = request.args.get('search')
    res = es.search(index="articles", size=100, body={"query": {"multi_match": {"query": search, "fields":['text', 'title']}}})
    x = {}
    for hit in res['hits']['hits']:
        if 'link' in hit['_source'].keys() && 'author' in hit['_source'].keys() && 'picture' in hit['_source'].keys():
            print(hit['_source'])
            x[hit['_source']['title']] = [hit['_source']['link'], hit['_source']['author'], hit['_source']['picture']]
    return json.dumps(x)

if __name__ == '__main__':

    es = Elasticsearch()

    newsapi = NewsApiClient(api_key='ab1223db856247deaabeb8a682ad6a1a')

    all_articles = newsapi.get_everything(q='', sources='bbc-news,the-verge,abc-news,associated-press,bloomberg,google-news,cnn,the-new-york-times,the-hill,washington-post,npr,pbs', from_param='2019-03-20',
                                      to='2019-04-06', language='en', sort_by='publishedAt', page_size=100)
    for article in all_articles['articles']:
        res = es.index(index="articles", doc_type='news', body={'author': article['author'], 'picture': article['urlToImage'], 'link': article['url'], 'title': article['title'], 'text': article['content']})
    es.indices.refresh(index="articles")
    app.run(debug=True, host = '0.0.0.0', port=80)
