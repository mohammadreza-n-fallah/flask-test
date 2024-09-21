from flask import Flask, jsonify, request,make_response,json
from elasticsearch import Elasticsearch
import datetime

app = Flask(__name__)

# Connect to the Elasticsearch server in docker
es = Elasticsearch([{'host': 'es', 'port': 9200, 'scheme': 'http'}])


@app.route("/all_articles",methods=["GET"])
def get_all_article():
    res=es.search(index="articles",body={
        "size":1000,
        "from":0,
        "query":{
            "match_all":{}
        }
    })
    return jsonify(res['hits']['hits'])


#create an index and add a article
@app.route('/articles', methods=['POST'])
def add_document():
    data = request.json
    print(data)
    # Example document structure
    doc = {
        'title': data.get('title'),
        'abstract': data.get('abstract'),
        "published_date":data.get('published_date') or datetime.datetime.now(),
        "author":data.get('author'),
    }
    try:
        res = es.index(index='articles', body=doc)
        return jsonify({"created_id":res['_id']}),201
    except:
        return jsonify({"message":"don't add article"})


#update a specific article with id
@app.route("/articles/<id>",methods=["PUT"])
def edit_article(id):
    data = request.json
    print(data)
    # Example document structure
    doc = {
        'title': data.get('title'),
        'abstract': data.get('abstract'),
        "published_date":data.get("published_date") or datetime.datetime.now(),
        "author":data.get("author")
    }
    try:
        res=es.update(index="articles",id=id ,body={"doc": doc})
        return jsonify({"message":" update is successful"})
    except:
        return jsonify({"message":"don't update"})


# delete a specific article with id
@app.route("/articles/<id>", methods=["DELETE"])
def delete(id):
    try:
        res=es.delete(index="articles",id=id)
        return jsonify({"message":"the article deleted"})
    except:
        return jsonify({"message":"don't delete"})



#search articles by query args
@app.route('/articles/search', methods=['GET'])
def search():
    query = request.args.get('q',"")
    try:
        # match query
        res = es.search(index='articles', body={
            'query': {
                'match': {
                    'abstract': query
                }
            }
        })
        return jsonify({"result":[hit["_source"] for hit in res["hits"]["hits"]]}),200
    except:
        return jsonify({"message":"search is faild"})



#return article by specific id
@app.route("/articles/<id>",methods=["GET"])
def get_article(id):
    try:
        res=es.get(index="articles",id=id)
        return jsonify(res["_source"])
    except:
        return jsonify({"message":"not found"})



if __name__ == '__main__':
    app.run(debug=True)
