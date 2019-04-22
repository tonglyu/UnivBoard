import os, json
from elasticsearch import Elasticsearch

#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def create_programs(input_dir):
    count = 1
    for path, subdirs, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            file = open(os.path.join(path, filename))
            data = file.read()
            programs = json.loads(data)

            for program in programs:
                
                #es.index(index='scu-program', doc_type='program', id=count, body=program)
                #count += 1

                #update#--------------------------------
                if filename[0:3] == "scu":
                    es.index(index='scu-program', doc_type='program', id=count, body=program)
                    count += 1
                elif filename[0:3] == "smc":
                    es.index(index='smc-course', doc_type='program', id=count, body=program)
                    count += 1
                elif filename[0:3] == "msm":
                    es.index(index='msmu-course', doc_type='program', id=count, body=program)
                    count += 1
                #---------------------------------------

def create_courses(input_dir):
    count = 1
    for path, subdirs, files in os.walk(input_dir):
        for filename in files:
            #update####
            #count = 1
            #########
            if not filename.endswith(".json"):
                continue
            file = open(os.path.join(path, filename))
            data = file.read()
            courses = json.loads(data)

            for course in courses:

                #es.index(index='scu-course', doc_type='course', id=count, body=course)
                #count += 1

                #update#--------------------------------
                if filename[0:3] == "scu":
                    es.index(index='scu-course', doc_type='course', id=count, body=course)
                    count += 1
                elif filename[0:3] == "smc":
                    es.index(index='smc-course', doc_type='course', id=count, body=course)
                    count += 1
                elif filename[0:3] == "msm":
                    es.index(index='msmu-course', doc_type='course', id=count, body=course)
                    count += 1
                #---------------------------------------

print("importing programs data.....")
create_programs("data/programs")
print("importing courses data.....")
create_courses("data/courses")
