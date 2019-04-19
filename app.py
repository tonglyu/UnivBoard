from flask import Flask, render_template, request
import config
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_object(config)

#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search_programs():
    keywords = request.form['keywords']
    universities = request.values.getlist('univ')
    departments = request.values.getlist('depart')
    results = es.search(index="scu-program", body={"query": {"match": {'title':keywords}}})
    return render_template('search.html', results=results["hits"]["hits"])

@app.route('/feature')
def feature():
    return render_template('subsection.html')

if __name__ == '__main__':
    app.run()
