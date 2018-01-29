import sms
import serial
import sys
number=sys.argv[1]
text="This number is not registered, Please try again with registered number"

def send_sms(number,text):
    sms.sendsms(number,text)
    print "successful"   
    
if __name__=="__main__":
   send_sms(number,text)

