import sms
import serial
import sys
number=sys.argv[1]
text= sys.argv[2]

def send_sms(number,text):
    sms.sendsms(number,text)
    print "successful"   
    
if __name__=="__main__":
   send_sms(number,text)

