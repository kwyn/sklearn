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
  # r = requests.post(apiurl+'/documents', data=json.dumps(payload), headers=headers)
  # print r.text
  r = requests.get(apiurl+'/documents')
  print 'document list', r.text
  r = requests.get(apiurl+'/documents/25')
  print 'document 5' , r.text
  parameters = { 'document_id' : '25'}
  r = requests.get(apiurl+'/search', params=parameters)
  print 'search', r.text
make_requests(pages)