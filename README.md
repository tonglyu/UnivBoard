# UnivBoard

## Virtual Environments and Run

http://flask.pocoo.org/docs/1.0/installation/#virtual-environments
- Before you work on your project, activate the corresponding environment:
```
. venv/bin/activate
(Windows: venv\Scripts\activate)
```
- In order to leave your virtual environment, just run deactivate
- Generate `requirements.txt`
```
pip freeze > requirements.txt
```
- Install and update libraries
```
pip install -r requirements.txt
```
- Download elasticsearch and run under its directory
```
bin/elasticsearch
```
- Import data (SCU)
```
python data/create.py
```
- Run the project
```
python app.py
```
- `requirements.txt`, `runtime.txt`, `Procfile` files are for deployment to heroku
