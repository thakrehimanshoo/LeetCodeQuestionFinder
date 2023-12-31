from flask import Flask, render_template, request, jsonify
from query import get_links

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    input_query = request.form['query']
    
    #will get links from query.py
    links = get_links(input_query)
    
    return jsonify(links=links)

if __name__ == '__main__':
    app.run(debug=True)
