import socket,thread,sys,time
import main

host = "##.website"   #ip of device
port = 1998	#port to connect to



s = socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

main.log("ready for connections")
print "Ready for connections"
s.listen(5)



while(True):
	try:
		c,addr = s.accept()
		c.settimeout(20)
		address = addr[0]
		main.log("Got connection from "+str(address))
		print "Got a connection from ",str(address)
		
		thread.start_new_thread(main.grabConnection,(c,addr))
	except Exception as e:
		main.log("Error for connection thread(Still running) "+str(e))
		print "Error at step 1 .. "+str(e)
		try:
			c.shutdown(1)
		except:
			pass
		try:
			c.close()
		except:
			pass
	
	
