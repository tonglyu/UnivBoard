from flask import Flask, render_template, request
import config
from elasticsearch import Elasticsearch
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config.from_object(config)
results = {}

#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['Get', 'POST'])
def search_programs():
    global results
    if request.method == "POST":
        keywords = request.form['keywords']
        universities = request.values.getlist('univ')
        departments = request.values.getlist('depart')
        results = es.search(index="scu-program", body={"from" : 0, "size" : 50, "query": {"match": {'title':keywords}}})

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    search = False
    q = request.args.get('q')
    if q:
        search = True
    results_for_render = results["hits"]["hits"][offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(results["hits"]["hits"]), search=search, css_framework='bootstrap4')
    return render_template('search.html', results=results_for_render, pagination=pagination)

@app.route('/details')
def show_details():
    return render_template('details.html')

@app.route('/feature')
def feature():
    return render_template('subsection.html')

if __name__ == '__main__':
    app.run()
