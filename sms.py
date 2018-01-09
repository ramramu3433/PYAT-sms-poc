#!/usr/bin/python
from time import sleep
import serial
from curses import ascii
import notify_sms
ser = serial.Serial()
ser.port = '/dev/ttyUSB1'
ser.baudrate = 128000
ser.timeout = 3

ser.open()
ser.write('AT+CMGF=1\r\n')
#ser.write('AT+CPMS="SM","ME","MT"\r\n')
ser.write('AT+CSCS=\"GSM\"\r\n')
sleep(10)

def sendsms(number,text):
    ser.write('AT+CMGF=1\r\n')
    sleep(2)
    ser.write('AT+CMGS="%s"\r\n' % number)
    ser.write('%s' % text)
    ser.write(ascii.ctrl('z'))    
    print "Text: %s  \nhas been sent to: %s" %(text,number)


def read_message(x):
    if x.startswith('+CMGL:'):
       return True         

def delete_all_sms():
    ser.write('AT+CMGF=0\r\n')
    sleep(5)
    ser.write('AT+CMGD=0,4\r\n')
    sleep(5)
    ser.write('AT+CMGF=1\r\n')

def delete_read_sms():
    ser.write('AT+CMGF=0\r\n')
    sleep(5)
    ser.write('AT+CMGD=0,1\r\n')
    sleep(5)
    ser.write('AT+CMGF=1\r\n')
    
def check_ussd_support():
    ser.write('AT+CMGF=0\r\n')
    ser.write('AT+CUSD=?\r\n')
    ser.write('AT+CMGF=1\r\n')
    

def get_balance():
    ser.write('AT+CMGF=0\r\n')
    ser.write('AT+CUSD=1,*141#,15\r\n')
    ser.read(1)
    a = ser.readlines()
    print a
    ser.write('AT+CMGF=1\r\n')

def ussd_sms_check():
    ser.write('AT+CMGF=0\r\n')
    ser.write('AT+CUSD=1,*141*1#,15\r\n')
    ser.read(100)
    a = ser.readlines()
    print a
    ser.write('AT+CMGF=1\r\n')

def read_sms_number(mode):
    ser.write('AT+CMGF=1\r\n')
    cmd='AT+CMGL=\"{}\"\r\n'.format(mode)
    ser.write(cmd)
    ms=ser.readlines()
    r=[]
    for x in ms: 
        if read_message(x):
           r.append(str(x).split(',')[0].split(':')[1])
    return [x for x in r]

def read_sms_body(number):
    ser.write('AT+CMGF=1\r\n')       
    cmd='AT+CMGR={}\r\n'.format(number)
    ser.write(cmd)
    ms=ser.readlines() 
    return ms
  
def stripit(string):
    out=[]
    for x in string:
        if x!='\r\n':
           out.append(x.strip())
    return out
def message(string):
     message=[]
     out= []
     for y in string:
            if y.startswith('+CMGR:'):
               t=y.split('"')
               number=t[3]
               date=t[5]
               out={"number":number,"date":date}

            elif y=='OK':
                 pass
            elif y==',':
                 pass
            elif y==' ':
                 pass
            elif y== '/n':
                 pass
            elif type(y)=='NoneType':
                 pass
            elif y.startswith('+CMTI'):
                 pass             
            else :
               if "message" in out:
                   out["message"]=out["message"]+","+y
               else:
                   out.update({"message":y})   
            #message.append(out)
     return out      
if __name__=="__main__":
    
    body=map(read_sms_body,read_sms_number("ALL"))
    output=[]
    msg=map(stripit,[x for x in body])
    parsed_msg=map(message,[x for x in msg])
    for x in parsed_msg:
        print x    
               
