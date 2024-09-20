from flask import Flask, jsonify, request,make_response
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Connect to the Elasticsearch server running locally
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Route to check Elasticsearch connection
@app.route('/ping', methods=['GET'])
def ping():
    if es.ping():
        return jsonify({"message": "Connected to Elasticsearch"}), 200
    else:
        return jsonify({"message": "Failed to connect to Elasticsearch."}), 500

# Route to create an index and add a document
@app.route('/add', methods=['POST'])
def add_document():
    data = request.json
    print(data)
    # Example document structure
    doc = {
        'title': data.get('title'),
        'content': data.get('content')
    }
    
    res = es.index(index='test-index', body=doc)
    return jsonify(res), 201

# Route to search documents
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    
    # Perform a simple match query
    res = es.search(index='test-index', body={
        'query': {
            'match': {
                'content': query
            }
        }
    })
    
    return jsonify(res['hits']['hits']), 200


@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    res=es.delete(index="test-index",id=id)
    return jsonify("message:suc")

if __name__ == '__main__':
    app.run(debug=True)
