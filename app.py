from flask import Flask, render_template, request
import config
from elasticsearch import Elasticsearch
import search

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
        results = search.getPrograms(es)

    # Pagination
    results_for_render, pagination = search.paginate(results)
    return render_template('search.html', results=results_for_render, pagination=pagination)

@app.route('/details')
def show_details():
    return render_template('details.html')

@app.route('/feature')
def feature():
    return render_template('subsection.html')

if __name__ == '__main__':
    app.run()
