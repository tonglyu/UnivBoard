from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from flask_paginate import Pagination, get_page_parameter



def getDetails(es):
    index = request.args.get('index')
    id = request.args.get('id')
    results = es.get(index=index, id=id, doc_type=index.split("-")[1])
    courses = results['_source'].get('related courses', [])
    related = []
    for course in courses:
        body = {
            "query": {
                "bool": {
                    "must": [{"term": {'initial.keyword':course}}]
                }
            }
        }
        result = es.search(index=index.replace("program", "course"), body=body)
        if result["hits"]["total"]["value"] != 0:
            related.append(result["hits"]["hits"][0]["_source"])
    results['_source']['related courses'] = related
    return results['_source']
