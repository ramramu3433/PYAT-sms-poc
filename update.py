import elasticsearch
import sys,json


data1='{"doc":{"status":"done"}}'


index='password_reset'
type='request'
id=sys.argv[1]
url='192.168.54.74'
es=elasticsearch.Elasticsearch(host=url)
def update():



   try:
      es.update(index=index,doc_type=type,id=id,body=data1)
   except Exception as e :
      print e
   else:
      print "Updated for id {}".format(id)


if __name__=="__main__":
   update()

