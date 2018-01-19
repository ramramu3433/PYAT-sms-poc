#!/usr/bin/python
from time import sleep
import serial
from curses import ascii
import sms,logging
import requests,json,datetime,pytz
ser = serial.Serial()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('hello.log')
handler.setLevel(logging.INFO)
ist=pytz.timezone( 'Asia/Kolkata')
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
ser.port = '/dev/ttyUSB1'
ser.baudrate = 128000
ser.timeout = 1
headers={"Content-type":"application/json"}
ser.open()
ser.write('AT+CMGF=1\r\n')
ser.write('AT+CPMS="ME","SM","MT"\r\n')
ser.write('AT+CSCS=\"GSM\"\r\n')
sleep(1)
number=[]
parsed_msg=[]
endpoint='http://192.168.54.101:9200/password_reset/request/'
#parse
class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)         
     
if __name__=="__main__":
   while True:
         
         new=sms.read_sms_number("REC UNREAD")
         if new:
            n=map(sms.read_sms_body,[x for x in new])
            msg=map(sms.stripit,[x for x in n])
            parsed_msg=map(sms.message,[x for x in msg])
            map(sms.delete_sms,[x for x in new])        
         new=[]  
         for x in parsed_msg:
             x.update({"number":x["number"][3:]})
             x.update({"message":x["message"].upper()})
             x.update({"timestamp":ist.localize(datetime.datetime.strptime(x["date"],'%y/%m/%d,%H:%M:%S+22'))})
             x.update({"status":"new"})
             
             logger.info("Message Received From {} at {} , Content is {}".format(x["number"],x["date"],x["message"]))
             if x["message"].upper()=="PASSWORD RESET":
                payload=json.dumps(x,cls=Encoder)
                url=endpoint+str(x["timestamp"])+x["number"]              
                t=requests.put(url,data=payload,headers=headers)
                logger.info("{} for {}".format(t.text,x))            
         parsed_msg=[]  
         sleep(1)
        
 
               
