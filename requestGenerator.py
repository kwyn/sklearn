import requests
import logging
import pickle
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus = open('data.pkl', 'rb')
pages = pickle.load(corpus)
corpus.close()
headers = {'content-type': 'application/json'}
# apiurl = 'http://ssaass-1-HarleyKwyn.delta.tutum.io:49375'
apiurl = 'http://172.12.8.150'
# apiurl = 'http://localhost:5000'
def make_requests(pages):
  print len(pages)
  payload = { 'documents' : pages }
  #print payload
  r = requests.post(apiurl+'/documents', data=json.dumps(payload), headers=headers)
  print r.text
  r = requests.get(apiurl+'/documents/doc_1')
  print 'document 1', r.text
  r = requests.get(apiurl+'/documents')
  print 'document list' , r.text

make_requests(pages)