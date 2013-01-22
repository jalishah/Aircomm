import msgpack
from interface import Interface
from time import sleep
import serial
import thread
from Crypto.Cipher import DES

i = Interface('/dev/ttyACM1')

mcounter = 0

def send_msg():
	global mcounter	
	global i	
	mFlag = 0	
	mType = 'b'
	msenderID = 5
	mspeed = 4.2	
	mheading = 360
	mpayload = 'abcdefgh'
	
	des = DES.new('12345678', DES.MODE_ECB)
	cipher_text = des.encrypt(mpayload)
	
	while 1:
		myMessage = msgpack.packb([mFlag,mType,msenderID,mspeed,mheading,cipher_text,mcounter])
		i.send(myMessage)
		mcounter += 1
		sleep(0.1)
	
def receive_msg():
	des = DES.new('12345678', DES.MODE_ECB)
	unp = msgpack.Unpacker()
	global i
	while 1:
		data = i.receive()
		unp.feed(data)
		for msg in unp:
			if type(msg) is tuple:
				print msg
				if len(msg) == 7:
					print des.decrypt(msg[5])
				else:
					print 'garbage type 1', msg 
			else:
				print 'garbage type 2', msg

		
try:
	thread.start_new_thread(receive_msg, () )
	thread.start_new_thread(send_msg, () )

except:
	print "Error: unable to start thread"

while True:
	sleep(1)
