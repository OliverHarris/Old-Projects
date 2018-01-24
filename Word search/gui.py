from tkinter import *



rows = ""
def find():
	global rows
	#get the word search
	s = search.get("1.0",END).replace(" ","")
	search.delete("1.0",END)
	search.insert(INSERT,s)
	wordSearch = search.get("1.0",END)
	#get words to find
	wordsToFind = words.get("1.0",END)
	
	
	##split the rows up
	rows = wordSearch.split("\n")
	##split the words up too
	wordsToFind  = wordsToFind.split("\n")
	
	
	
	##for each word we'll look through the wordsearch
	for word in wordsToFind:
		##now we search each row
		curRow = -1
		curCol = 0
		for row in rows:
			curRow = curRow+1
			curCol = 0
			##split the letters up
			letters = list(row)
			
			##search each letter for the first letter of the word
			for letter in letters:
				try:
					word[0]
				except:
					print ("no words to find")
					return
				curCol = curCol+1
				##we're only looking for the first letter here
				if(letter==word[0]): #word[0] will be the first letter of the word, to match the current letter it's looking at.
					##look right, left, up, down 
					f = False #has it found the word? if it has, the program can move onto the next word
					print ("found the first letter, looking right ",str(curCol))
					f = lookRight(curRow,curCol,word)
					if(f):
						return
					print ("looking left")
					f = lookLeft(curRow,curCol,word)
					if(f):
						return
					print ("looking up")
					f = lookUp(curRow,curCol,word)
					if(f):
						return
					print("looking down")
					f=lookDown(curRow,curCol,word)
					if(f):
						return
					if(not f):
						print ("Couldn't find word!")
	


def lookRight(curRow,curCol,word):
	letters = list(word)
	checked = 1 #we've already found one
	##get the row
	print ("0")
	using = rows[curRow]
	##highlight where the first letter is
	start = "%s.%s"%(curRow+1,curCol-1)
	print (start)
	end = "%s.%s"%(curRow+1,curCol-1+len(word))
	print (end)
	while(checked<len(word)):
		print ("1")
		try:
			if(using[curCol-1+checked]==letters[checked]):
				print ("2")
				
				print (end)
				if(checked+1==len(word)):
					print ("3")
					
					search.tag_add("here", start, end)
					print (start)
					print (end)
					search.tag_config("here", background="yellow", foreground="blue")
					return True
				else:
					checked = checked + 1
			else:
				return False
		except:
			print ("not here")
			return False
		
def lookLeft(curRow,curCol,word):
	letters = list(word)
	checked = 1 #we've already found one
	##get the row
	print ("0")
	using = rows[curRow]
	##highlight where the first letter is
	start = "%s.%s"%(curRow+1,curCol)
	print (start)
	end = "%s.%s"%(curRow+1,curCol-len(word))
	print (end)
	while(checked<len(word)):
		print ("1")
		try:
			if(using[curCol-1-checked]==letters[checked]):
				print ("2")
				
				
				if(checked+1==len(word)):
					print ("3")
					
					search.tag_add("here", end, start)
					print (start)
					print (end)
					search.tag_config("here", background="yellow", foreground="blue")
					return True
				else:
					checked = checked + 1
			else:
				return False
		except:
			print ("not here")
			return False
		

def lookUp(curRow,curCol,word):
	letters = list(word)
	checked = 1 #we've already found one
	##get the row
	print ("0")
	using = rows[curRow]
	##highlight where the first letter is
	start = "%s.%s"%(curRow+1,curCol-1)
	print (start)
	end = "%s.%s"%(curRow+1,curCol)
	print (end)
	search.tag_add("here", start, end)

	search.tag_config("here", background="yellow", foreground="blue")
	while(checked<len(word)):
		print ("1")
		try:
			rowLetters = list(rows[curRow-checked])
			print (rowLetters)
			if(rowLetters[curCol-1]==letters[checked]):
				print ("2")
				start = "%s.%s"%(curRow+1-checked,curCol-1)
				print (start)
				end = "%s.%s"%(curRow+1-checked,curCol)
				print (end)
				search.tag_add("here", start, end)

				search.tag_config("here", background="yellow", foreground="blue")
				if(checked+1==len(word)):
					print ("3")
					
					search.tag_add("here", start, end)
					print (start)
					print (end)
					search.tag_config("here", background="yellow", foreground="blue")
					return True
				else:
					checked = checked + 1
			else:
				return False
		except:
			print ("not here")
			return False



def lookDown(curRow,curCol,word):
	letters = list(word)
	checked = 1 #we've already found one
	##get the row
	print ("0")
	using = rows[curRow]
	##highlight where the first letter is
	start = "%s.%s"%(curRow+1,curCol-1)
	print (start)
	end = "%s.%s"%(curRow+1,curCol)
	print (end)
	search.tag_add("here", start, end)

	search.tag_config("here", background="yellow", foreground="blue")
	while(checked<len(word)):
		print ("1")
		try:
			rowLetters = list(rows[curRow+checked])
			print (rowLetters)
			if(rowLetters[curCol-1]==letters[checked]):
				print ("2")
				start = "%s.%s"%(curRow+1+checked,curCol-1)
				print (start)
				end = "%s.%s"%(curRow+1+checked,curCol)
				print (end)
				search.tag_add("here", start, end)

				search.tag_config("here", background="yellow", foreground="blue")
				if(checked+1==len(word)):
					print ("3")
					
					search.tag_add("here", start, end)
					print (start)
					print (end)
					search.tag_config("here", background="yellow", foreground="blue")
					return True
				else:
					checked = checked + 1
			else:
				return False
		except:
			print ("not here")
			return False










root = Tk()
search = Text(root)
words = Text(root)
Label(root,text="Word search:").grid(row=0,column=1)
search.grid(row=1,column=1)
Label(root,text="Words to find:").grid(row=2,column=1)
words.grid(row=3,column=1)

Button(root,text="Find",command=find).grid(row=4,column=1)


root.mainloop()
