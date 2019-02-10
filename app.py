from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import config

app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/feature')
def feature():
    return render_template('subsection.html')

if __name__ == '__main__':
    app.run()
