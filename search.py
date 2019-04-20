from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from flask_paginate import Pagination, get_page_parameter

def paginate(results):
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
    return results_for_render, pagination

def getPrograms(es):
    keywords = request.form['keywords']
    universities = request.values.getlist('univ')
    departments = request.values.getlist('depart')
    # return 50 results
    body = {
        "from" : 0,
        "size" : 30,
        "query": {
            "bool": {
                "must": [],
                "should": []
            }
        }
    }
    if keywords != "":
        body["query"]["bool"]["must"].append({"match": {'title':keywords}})
    for department in departments:
        body["query"]["bool"]["should"].append({"term": {'department.keyword':department}})
    results = es.search(index="scu-program", body=body)
    return results
