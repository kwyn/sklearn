#! /usr/local/bin/python

from flask import Flask, jsonify, make_response, request, abort
# from flask.ext.restful import reqparse, abort, Api, Resource
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os, shutil
import logging
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

app = Flask(__name__)

#########################################################################
#Intilize psuedo database and tfidf service
#########################################################################

tfidf = TfidfVectorizer(stop_words='english')

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
    try:
        storage = open('corpus.pkl', 'rb')
        corpus = pickle.load(storage)
        storage.close()
    except:
        corpus = list()
        pass
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
    results = corpus
    storage.close()
    return results

def get_document(document_id):
    storage = open('corpus.pkl', 'rb')
    corpus = pickle.load(storage)
    storage.close()
    for document in corpus :
        if document['doc_id'] == document_id :
            return document
    raise InvalidUsage("Document not found", status_code=404)

def get_raw_array(corpus):
    raw_docs = list()
    for document in corpus :
        raw_docs.append(document['document_body'])
    return raw_docs

def get_doc_ids():
    storage = open('corpus.pkl', 'rb')
    corpus = pickle.load(storage)
    storage.close()
    id_list = list()
    for document in corpus :
        id_list.append(document['doc_id'])
    return id_list

def train():
    storage = open('corpus.pkl', 'rb')
    corpus = pickle.load(storage)
    storage.close()
    documents = get_raw_array(corpus)
    result_array = tfidf.fit_transform(documents)
    return result_array

def get_similar(doc_id = None, doc_body = None):
    if doc_id is not None :
        matrix = train()
        doc = get_document(doc_id)
        doc_vect = tfidf.transform([doc['document_body']]).todense()
    elif doc_body is not None :
        matrix = train()
        doc_vect = tfidf.transform(doc_body)
    results = cosine_similarity(matrix, doc_vect)
    document_array = np.array( get_doc_ids(), np.int32)[np.newaxis]
    document_array = document_array.T
    results = np.append(document_array, results, 1)
    results = np.sort(results.view([('',results.dtype)]*results.shape[1]), axis=0, kind='mergesort', order=['f1']).view(results.dtype)
    results = results[::-1] 
    return results.tolist()

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
        return jsonify( { 'documents': make_document_list() } )


@app.route('/documents/<document_id>', methods = ['GET', 'DELETE'])
def documents(document_id):
    if request.method == 'GET' :
        return jsonify( { 'document':  get_document( document_id ) })
    elif request.method == 'DELETE' :
        return jsonify( { 'document_id_placeholder': document_id } )

#########################################################################
#Search handler
#########################################################################

@app.route('/search', methods = ['GET'])
def search():
    if request.args.get('document_id') is not None :
        result = get_similar( doc_id = request.args.get('document_id'))
    elif request.args.get('document_body') is not None:
        result = get_similar( doc_body = request.args.get('document_body') )
    else:
        raise InvalidUsage('bad request, please send valid document_id or document_body', status_code=400)
    return jsonify( {'results': result } )

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
