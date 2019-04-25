from flask import Flask, render_template, request
import config, os, re
from elasticsearch import Elasticsearch
import search, detail
import certifi

app = Flask(__name__)
app.config.from_object(config)
results = {}

#connect to our cluster
# es = Elasticsearch([{'host': 'localhost', 'port':9200}])

# Parse the auth and host from env:
bonsai = "https://9yg7zvgsw9:j67pfvx22a@pine-523218699.us-east-1.bonsaisearch.net"
auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# Connect to cluster over SSL using auth for best security:
es_header = [{
 'host': host,
 'port': 443,
 'use_ssl': True,
 'http_auth': (auth[0],auth[1])
}]

# Instantiate the new Elasticsearch connection:
es = Elasticsearch(es_header)

body = {
    "size":"0",
    "aggs": {
        "uniq_depart": {
            "terms": {
                "field": "department.keyword",
                "size" : 500
            }
        }
    }
}
msmu_depart = es.search(index="msmu-program", body=body)['aggregations']['uniq_depart']['buckets']
smc_depart = es.search(index="smc-program", body=body)['aggregations']['uniq_depart']['buckets']
scu_depart = es.search(index="scu-program", body=body)['aggregations']['uniq_depart']['buckets']

@app.route('/')
@app.route('/search')
def index():
    return render_template('index.html', smc_depart=smc_depart, scu_depart=scu_depart, msmu_depart=msmu_depart)

@app.route('/search/programs', methods=['Get', 'POST'])
def search_programs():
    global results
    if request.method == "POST":
        results = search.getPrograms(es)

    # Pagination
    results_for_render, pagination = search.paginate(results)
    return render_template('search.html', smc_depart=smc_depart, scu_depart=scu_depart, msmu_depart=msmu_depart, results=results_for_render, pagination=pagination, type="program")

@app.route('/search/courses', methods=['Get', 'POST'])
def search_courses():
    global results
    if request.method == "POST":
        results = search.getCourses(es)

    # Pagination
    results_for_render, pagination = search.paginate(results)
    return render_template('search.html', smc_depart=smc_depart, scu_depart=scu_depart, msmu_depart=msmu_depart, results=results_for_render, pagination=pagination, type="course")

@app.route('/details')
def show_details():
    details = detail.getDetails(es)
    return render_template('details.html', details=details)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
