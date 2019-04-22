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
    suffix = "-program"
    index=""
    keywords = request.form['keywords']
    universities = request.values.getlist('univ')
    departments = request.values.getlist('depart')
    print(departments)
    # return 50 results
    body = {
        "from" : 0,
        "size" : 30,
        "query": {
            "bool": {
                "must": [],
                "should": [],
                "minimum_should_match" : 0
            }
        }
    }
    if keywords != "":
        body["query"]["bool"]["must"].append({"match": {'title':keywords}})
    for department in departments:
        body["query"]["bool"]["should"].append({"term": {'department.keyword':department}})
    if len(body["query"]["bool"]["should"]) > 0:
        body["query"]["bool"]["minimum_should_match"] = 1

    for university in universities:
        index += university + suffix + ","
    if len(universities) == 0:
        index = "smc-program,msmu-program,scu-program"
    results = es.search(index=index.rstrip(","), body=body)
    return results

def getCourses(es):
    suffix = "-course"
    index=""
    keywords = request.form['keywords2']
    universities = request.values.getlist('univ2')
    departments = request.values.getlist('depart2')
    field = request.form['field']
    print(departments)
    # return 50 results
    body = {
        "from" : 0,
        "size" : 30,
        "query": {
            "bool": {
                "must": [],
                "should": [],
                "minimum_should_match" : 0
            }
        }
    }
    if keywords != "":
        if field == "title":
            body["query"]["bool"]["must"].append({"match": {'title':keywords}})
        else:
            body["query"]["bool"]["must"].append({"match": {'initial':keywords}})
    for department in departments:
        body["query"]["bool"]["should"].append({"term": {'department.keyword':department}})
    if len(body["query"]["bool"]["should"]) > 0:
        body["query"]["bool"]["minimum_should_match"] = 1

    for university in universities:
        index += university + suffix + ","
    if len(universities) == 0:
        index = "smc-course,msmu-course,scu-course"
    results = es.search(index=index.rstrip(","), body=body)
    return results
