import sys,subprocess,re
type=sys.argv[2]


def search(number):
    if type=='PWDRST':
       query='ldapsearch -x telephonenumber={} 1'.format(number)
    elif type=='UNAC':
       query='ldapsearch -xLLL "(& (telephoneNumber={})(pwdAccountLockedTime=*))"'.format(number)
    elif type=="UNACR":
       query='ldapsearch -x telephonenumber={}'.format(number)
   
    print query
    t=subprocess.Popen(query,stdout=subprocess.PIPE, shell=True)
    (output, err) = t.communicate()
    t=re.search('dn.*',output)
    return  t.group(0) if t!=None else 0

if __name__=="__main__":
   
   number=sys.argv[1]
   print  search(number)
  
