import sqlite3 as lite
import time




def log(text):
	t = time.time()
	f = open("log","a")
	f.write("["+str(t)+"] "+text+"\n")
	f.close()



def grabConnection(c,addr):
	
	
	##First the variables
	auth = False #These are LOCAL variables only used by this thread, when the connection is closed these are lost
	user = "" #Stores the id of the user, so that any requests later can use this
	
	
	for line in readlines(c): #reads line by line ( thats the \n )
		print "line: "+line
		
		
		if(auth):#This goes before not auth  - otherwise when the user auths it will go through this if too
			##clean up the text, and see if it matches
			line = line.rstrip()
			forNow = line[:3]#tells us what to do
			log(user+" command: "+line[:3])
			if(forNow == "lis"):
				
				listThem(c)
			if(forNow == "out"):
				signOut(c,line,user)
			if(forNow == "sin"):
				signIn(c,user)
		
		
		if(not auth):#they have to login before anything happens!
			##inside the line we should get user:password  that means we can split this line into two
			try:
				values = line.split(":",1)
				values[1]
			except:
				print "Values can't split into two"
				c.send("1 Data required in the login\n")
				return
			print values #will give a nice display so we know what we're dealing with (debug)
			##i could of used username,password = line.split(":",2) but i like to make it confusing 
			
			#its possible for no value to be entered for a username or password, so we'll check for that
			if(len(values[0]) == 0 or len(values[1]) == 0):
				print "A value has no data"
				##and we'll return an error to the socket
				c.send("1 Data required in the login\n")
				c.close()##this "should" close the connection and end all the loops
				return
			
			con = lite.connect('data.db') #open the database with the login details.
			##clean up the text
			values[1] = values[1].rstrip()
	
	
			with con:    
	
				cur = con.cursor()    
				cur.execute("SELECT * FROM details WHERE username=? AND password=?",(values[0],values[1]))#It will only work if both values are there
		
				row = cur.fetchone()
				if(not row):
					log(addr+" incorrect login details!")
					print "They're not there"#wrong username/password
					c.send("2 Wrong username or password\n")
					c.close()
		
		
				else:
					#should mean its correct..
					user = row[0] #this is clientID
					auth = True
					c.send("3 Well done, it's correct!\n")
		
			
		print user




def signOut(c,line,clientId):
	line = line[4:len(line)]
	##There is no checking to see if they're already signed out - sounds like a good idea to me. 
	con = lite.connect("data.db")
	with con:
		cur = con.cursor()
		cur.execute("UPDATE details SET 'in'='no'  WHERE clientId=?",(clientId,))
	with con:
		cur = con.cursor()
		## one step further, add it to the history table! :O
		timeStamp = time.time()
		cur.execute("INSERT INTO history VALUES(?,?,?,?)",(clientId,timeStamp,'no',line,))
	c.send("6 you've been signed out goodbye, you are the weakest link\n")

def signIn(c,clientId):

	##There is no checking to see if they're already signed in - sounds like a good idea to me. 
	con = lite.connect("data.db")
	with con:
		cur = con.cursor()
		cur.execute("UPDATE details SET 'in'='yes' WHERE clientId=?",(clientId,))
	with con:
		cur = con.cursor()
		## one step further, add it to the history table! :O
		timeStamp = time.time()
		cur.execute("INSERT INTO history VALUES(?,?,?,?)",(clientId,timeStamp,'yes','',))
	c.send("7 you've signed in..Why?!\n")
	c.close()
	return

def listThem(c):
	##from our database we'll get the list of teachers who aren't in
	con = lite.connect("data.db")
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM whoisnotin")
		rows = cur.fetchall()
		#could be more than one row now, we'll put each row into a string that we can send
		theLineWeWillSend = "" #if it was inside the loop it would be overwritten each time
		if(not rows):
			print "Everyone is in!"
			c.send("4 everyone is in\n")
			c.close()
			return
		for r in rows:
			#in r there is:  teacher   subject   comment 
			#For now the data is NOT safe. 
			theLineWeWillSend=r[0]+":"+r[1]+":"+r[2]+"~"+theLineWeWillSend
		print "total to send. ",theLineWeWillSend #wish i made this shorter, it takes forever to type.
		c.send("5 "+theLineWeWillSend+"\n")
		c.close()
		return
def readlines(sock):
	recv_buffer=1024

	delim='\n'
	buffer = ''
	data = True
	cycles = 0
	while data:
		if(cycles > 100):
			cycles = 0
			yield "Too much data"
		try:
			data = sock.recv(recv_buffer)
			
			buffer += data
			cycles = cycles + 1
			while buffer.find(delim) != -1:
				line, buffer = buffer.split('\n', 1)
			
				cycles = 0 
			
				yield line
		except:
			
			return 

	return
