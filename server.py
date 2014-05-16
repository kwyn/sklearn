#! /usr/local/bin/python

from flask import Flask, jsonify, make_response, request, abort
# from flask.ext.restful import reqparse, abort, Api, Resource
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import os, shutil
import logging
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

app = Flask(__name__)

#########################################################################
#Intilize psuedo database and tfidf service
#########################################################################

# tfidf = TfidfVectorizer(stop_words='english')


#########################################################################
#Helper methods
#########################################################################

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def add_documents(documents):
    storage = open('corpus.pkl', 'rb')
    corpus = pickle.load(storage)
    storage.close()
    doc_list = list()
    storage = open('corpus.pkl', 'wb')
    for document in documents:
        doc_id = str( len(corpus) + 1 )
        doc = { 'doc_id' : doc_id , 'document_body': document }
        corpus.append( doc )
        doc_list.append(doc_id)
    pickle.dump(corpus, storage)
    storage.close()
    return corpus

def make_document_list():
    storage = open('corpus.pkl', 'rb')
    corpus = pickle.load(storage)
    print len(corpus)
    results = corpus
    storage.close()
    return results

def get_document():
    corpus = pickle.load(storage)
    return corpus

# def train():
#     storage = open('corpus.pkl', 'rb')
#     corpus = pickle.load(storage)
#     matrix = tfidf.fit_transform(pages[0:10])
#     storage.close()

# matrix = tfidf.fit_transform(pages[0:10])

#########################################################################
#Document handlers
#########################################################################

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return "Semantic Similarity as a Super Service SSAASS"


#########################################################################
#Document handlers
#########################################################################

@app.route('/documents', methods = ['GET','POST'])
def get_document_list():
    if request.method == 'POST' :
        if not request.json :
            raise InvalidUsage('Send data in json format', status_code=400)
        if 'documents' not in request.json :
            raise InvalidUsage("Json must have 'documents' key ", status_code=400)
        if type(request.json['documents']) is not list :
            raise InvalidUsage('Requires a document list', status_code=400)
        document_ids = add_documents( request.json['documents'] )
        return jsonify( { 'document_ids': document_ids } )
    elif request.method == 'GET' :
        doclist = make_document_list()
        return jsonify( { 'document_ids': doclist } )


@app.route('/documents/<document_id>', methods = ['GET', 'DELETE'])
def documents(document_id):
    if request.method == 'GET' :
        return jsonify( { 'document_id_placeholder': document_id } )
    elif request.method == 'DELETE' :
        return jsonify( { 'document_id_placeholder': document_id } )

#########################################################################
#Search handler
#########################################################################

@app.route('/search', methods = ['GET'])
def search():
    if request.form['document_id'] :
        result = get_similar( doc_id = request.form['document_id'] )
    elif request.form['document_body'] :
        result = get_similar( doc_body = request.form['document_body'] )
    else:
        raise InvalidUsage('bad request, please send document_id or document_body', status_code=400)
    return jsonify( {'results': result } )


# storage = open('corpus.pkl', 'rb')
# corpus = pickle.load(storage)
# storage.close()

# tfidf = TfidfVectorizer(stop_words='english')
# matrix = tfidf.fit_transform(pages[0:10])

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")







