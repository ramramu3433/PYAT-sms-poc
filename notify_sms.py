#!/usr/bin/python
from time import sleep
import serial
from curses import ascii
import sms
ser = serial.Serial()
ser.port = '/dev/ttyUSB1'
ser.baudrate = 128000
ser.timeout = 1

ser.open()
ser.write('AT+CMGF=1\r\n')
#ser.write('AT+CPMS="SM","ME","MT"\r\n')
ser.write('AT+CSCS=\"GSM\"\r\n')
sleep(10)
number=[]
def read_inifiny():
    return ser.readlines()

def parse_new(string):
    #number=[]
    for x in string:
        if x.startswith("+CMTI:"):
           number.append(x.split(',')[1].rstrip())
           
     
if __name__=="__main__":
   while True:
         msg=read_inifiny()
         new=parse_new(msg)
         n=map(sms.read_sms_body,[x for x in new])
         #new=parse_new(n)
         msg=map(sms.stripit,[x for x in n])
         parsed_msg=map(sms.message,[x for x in msg])
         
           
         for x in parsed_msg:
             print x
            
         sleep(10)
        
 
               
