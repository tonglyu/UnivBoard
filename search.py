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
    results = es.search(index="scu-program", body={"from" : 0, "size" : 50, "query": {"match": {'title':keywords}}})
    return results
