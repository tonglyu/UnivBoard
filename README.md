# UnivBoard

## Run Instructions

### Virtual Environments

- Activate the corresponding environment:
```
. venv/bin/activate
(Windows: venv\Scripts\activate)
```
- In order to leave your virtual environment, just run `deactivate`
- Generate `requirements.txt`
```
pip freeze > requirements.txt
```
- Install and update libraries
```
pip install -r requirements.txt
```

### Elasticsearch

- Download elasticsearch and run under its directory to start the server
```
bin/elasticsearch
```
- Import our data
```
python data/create.py
```
- Run the project
```
python app.py
```
