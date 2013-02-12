import msgpack
from interface import Interface
from time import sleep
import serial
import thread
import yaml
import zmq
import random


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5557")
i = Interface('/dev/ttyACM1')

mcounter = 0

def send_msg():
	global mcounter	
	global i	
	mFlag = 0	
	mType = 'aa'
	msenderID = 5
	mspeed = 4.2	
	mheading = 360
	mpayload = 'abcdefgh'
	
	
	while 1:
		myMessage = msgpack.packb([mFlag,mType,msenderID,mspeed,mheading,mpayload,mcounter])
		i.send(myMessage)
		mcounter += 1
		sleep(0.1)
	
def receive_msg():
	unp = msgpack.Unpacker()
	global i
	while 1:
		data = i.receive()
		unp.feed(data)
		for msg in unp:
			if type(msg) is tuple:
				print msg
				if len(msg) == 7:
					if(msg[1]=='ab'):
						socket.send(msg[5])
			#	else:
			#		print 'garbage type 1', msg 
			#else:
			#	print 'garbage type 2', msg 

		
try:
	thread.start_new_thread(receive_msg, () )
	thread.start_new_thread(send_msg, () )

except:
	print "Error: unable to start thread"

while True:
	sleep(1)
