# import the necessary packages
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2
import urllib.request
import numpy as np
import time
import csv
#import RPi.GPIO as GPIO
import pika

#GPIO.setwarnings(False)
#Buzzer_Pin = 17
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(Buzzer_Pin,GPIO.OUT)

print('starting video stream')

time.sleep(1.0)


print('Scan the Product')

class BarCode_Scanner:

    def Initialize_Values(self):
        self.key = "Start"
        
        url='http://192.168.1.3:8080/shot.jpg'
        
        # open the output CSV file for writing and initialize the set of
        # barcodes found thus far
        Barcode_Read =  open('Barcodes.csv', 'w')
        found = set()


        credentials = pika.PlainCredentials('newuser1', 'password')
        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 
                                      5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue='Pi2PC.BarCodeData')
        channel.exchange_declare(exchange='Pi2PC.topic', exchange_type='topic', durable = True, auto_delete = False)
        
    
    def End_Scanning_Product(self):
        self.key = "Quit"
    
    def Buzzer(self,command):
        if command!="0":
            #GPIO.output(Buzzer_Pin,True)
            print("Buzzing")
        else:
            #GPIO.output(Buzzer_Pin,False)
            print("Stopped Buzzing")


    def Scan_Product(self):
        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = urllib.request.urlopen(url)
            frame = np.array(bytearray(frame.read()),dtype=np.uint8)
            frame = cv2.imdecode(frame,-1)
            frame = imutils.resize(frame, width=400)
    
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
    
            # loop over the detected barcodes
            for barcode in barcodes:
            
                Product_Found = 0
        
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                if barcodeData not in found:
                    Barcode_Read.write("{},{}\n".format(datetime.datetime.now(),
                        barcodeData))
                    Barcode_Read.flush()
                    found.add(barcodeData)
                    
                     message_from_pi_BarCode = time.ctime() + " Scanned Bar Code: %"+ str(barcodeData)+"%"
                     
                     channel.basic_publish(exchange = 'Pi2PC.topic', routing_key = 'Cart101.ShoppingMall.BarCodeDaataValue', body = message_from_pi_BarCode)
                    
                    with open('DataBase.csv') as Input_file:
                        csv_reader = csv.reader(Input_file, delimiter=',')
                        for row in csv_reader:
                            if(barcodeData == row[0]):
                                Product_Found = 1
                                print("Product Found")
                                print(row[2])
                                break
                            else:
                                Product_Found = 0
                    
                    if(Product_Found == 0):
                        print("Product not in database, update the database")                    
                    self.Buzzer('1')
                    time.sleep(0.5)
                    self.Buzzer('0')
                    
                    self.End_Scanning_Product()
                    
                    print('Scan the next Product')
                     
            # Exit from the loop
            if self.key == "Quit":
                print("End of Scanning Products")
                break
        
        # close the output CSV file do a bit of cleanup
        Barcode_Read.close()
    
if __name__=='__main__':
    B=BarCode_Scanner()
    B.Initialize_Values()
    B.Scan_Product()
