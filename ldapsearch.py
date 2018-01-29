import sys,subprocess,re


def search(number):
    query='ldapsearch -x telephonenumber={} 1'.format(number)
    print query
    t=subprocess.Popen(query,stdout=subprocess.PIPE, shell=True)
    (output, err) = t.communicate()
    t=re.search('dn.*',output)
    return  t.group(0) if t!=None else 0

if __name__=="__main__":
   number=sys.argv[1]
   print  search(number)
  
