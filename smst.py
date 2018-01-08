#!/usr/bin/env python
"""
sms.py - Used to send txt messages.
"""
import serial
import time

class TextMessage:
    def __init__(self, recipient="+919840175445", message="Hello There!!!"):
        self.recipient = recipient
        self.content = message

    def setRecipient(self, number):
        self.recipient = number

    def setContent(self, message):
        self.content = message

    def connectPhone(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
        time.sleep(1)

    def sendMessage(self):
        self.ser.write("ATZ\r")
        time.sleep(2)
        self.ser.write("AT+CMGF=1\r")

        time.sleep(2)
        self.ser.write("AT+CSCS=GSM\r")
        time.sleep(2)
        self.ser.write("AT+CMGS=" + self.recipient + "\r")
     
        time.sleep(2)
        self.ser.write(self.content + "\r")
        time.sleep(2)
        self.ser.write(chr(26))
        time.sleep(2)

    def readMessage(self):
        self.ser.write("ATZ\r")
        time.sleep(2)
        
        self.ser.write("AT+CMGF=1\r")
        time.sleep(2)

        self.ser.write("AT+CSCS=\"GSM\"\r")
        time.sleep(2)

        
        mode="ALL"
        self.ser.write("AT+CMGL=" + "\"" + mode+"\"" + "\r")
        self.ser.readline().decode('ascii').strip()
        self.ser.readline().decode('ascii').strip()
        self.ser.readline().decode('ascii').strip()
       
        self.ser.write(chr(26))
        time.sleep(2)

    def disconnectPhone(self):
        self.ser.close()
    def read_command_response(self):
        print self.ser.readline().decode('ascii').strip()
        print "\n"

if __name__=="__main__":
   sms= TextMessage()
   sms.connectPhone()
   sms.sendMessage()
   #print sms.message
   sms.disconnectPhone() 
   
