file = open("word.txt", "r")
wholeText = file.read()
#split the rows
wholeText = wholeText.replace(" ","")
row = wholeText.split()


def findWord(word):
	print "finding ",word
	#for each row look for the first letter
	curRow = 0
	curCol = 0
	
	found = False
	for r in row:
		letters = list(r)
		
		for l in letters:
			if(l == word[0]):
				
				#look right
				found = lookRight(word,curRow,curCol)
				if(found):
					return
				found = lookLeft(word,curRow,curCol)
				if(found):
					return
				found = lookUp(word,curRow,curCol)
				if(found):
					return
				found = lookDown(word,curRow,curCol)
				if(found):
					return
				found = diagonal(word,curRow,curCol)
				if(found):
					return
				
			curCol = curCol + 1
		curRow=curRow+1
		curCol = 0
		if(found or curRow==24):
			break
	if(not found):
		print "Unable to find ",word
		return
	else:
		return


def lookRight(word,curRow,curCol):
	letters = list(word)
	checked  = 1 #already found the first letter
	workingRow = list(row[curRow])
	cords = [word[0]+"~("+str(curRow+1)+","+str(curCol+1)+")"]
	while(checked<len(word)):
		try:
			
			if(workingRow[curCol+checked]==letters[checked]):
				cords.append(word[checked]+"~("+str(curRow+1)+","+str(curCol+checked+1)+")")
				if(checked+1==len(word)):
					print cords
					return True
				else:
					checked = checked + 1
			else:
				return False
		except:
			return False
			

def lookLeft(word,curRow,curCol):
	letters = list(word)
	checked  = 1 #already found the first letter
	workingRow = list(row[curRow])
	cords = [word[0]+"~("+str(curRow+1)+","+str(curCol+1)+")"]
	while(checked<len(word)):
		try:
			
			if(workingRow[curCol-checked]==letters[checked]):
				cords.append(word[checked]+"~("+str(curRow+1)+","+str(curCol-checked+1)+")")
				if(checked+1==len(word)):
					print cords
					return True
				else:
					checked = checked + 1
			else:
				return False
		except:
			return False

def lookUp(word,curRow,curCol):
	letters = list(word)
	checked  = 1 #already found the first letter
	cords = [word[0]+"~("+str(curRow+1)+","+str(curCol+1)+")"]
	while(checked<len(word)):
		try:
			
			rowLetters = list(row[curRow-checked])
			if(rowLetters[curCol]==letters[checked]):
				cords.append(word[checked]+"~("+str(curRow+checked+1)+","+str(curCol+1)+")")
				if(checked+1==len(word)):
					print cords
					return True
				else:
					checked = checked + 1
			else:
				return False
			
			
			
		except:
			return False

def lookDown(word,curRow,curCol):
	letters = list(word)
	checked  = 1 #already found the first letter
	cords = [word[0]+"~("+str(curRow+1)+","+str(curCol+1)+")"]
	while(checked<len(word)):
		try:
			
			rowLetters = list(row[curRow+checked])
			if(rowLetters[curCol]==letters[checked]):
				cords.append(word[checked]+"~("+str(curRow+checked+1)+","+str(curCol+1)+")")
				if(checked+1==len(word)):
					print cords
					return True
				else:
					checked = checked + 1
			else:
				return False
			
			
			
		except:
			return False
			


def diagonal(word,curRow,curCol):
	letters = list(word)
	checked = 1
	block =0
	cords =  [word[0]+"~("+str(curRow+1)+","+str(curCol+1)+")"]
	while(checked<len(word)):
		#check + row + col
		try:
			if(block==0):

				rowLetters = list(row[curRow+checked])

				if(rowLetters[curCol+checked]==letters[checked]):
					
					cords.append(word[checked]+"~("+str(curRow+checked+1)+","+str(curCol+checked+1)+")")
					if(checked+1==len(word)):
						print cords
						return True
					else:
						checked = checked + 1
						continue
				block = 1
		except:
			block = 1
		
		try:
			if(block==1):
				#check + row + col
				rowLetters = list(row[curRow-checked])
				if(rowLetters[curCol-checked]==letters[checked]):

						cords.append(word[checked]+"~("+str(curRow-checked+1)+","+str(curCol-checked+1)+")")
						if(checked+1==len(word)):
							print cords
							return True
						else:
							checked = checked + 1
							continue
			
		
				block = 2
		except:
			block = 1
			
		
		try:
			if(block==2):
				#check - row + col
				rowLetters = list(row[curRow-checked])
				if(rowLetters[curCol+checked]==letters[checked]):
			
						cords.append(word[checked]+"~("+str(curRow-checked+1)+","+str(curCol+checked+1)+")")
						if(checked+1==len(word)):
							print cords
							return True
						else:
							checked = checked + 1
							continue
				else:
		
					block = 3
		except:
			block = 3
			
		try:
			if(block==3):
				#check - row + col
				rowLetters = list(row[curRow+checked])
				if(rowLetters[curCol-checked]==letters[checked]):
		
						cords.append(word[checked]+"~("+str(curRow+checked+1)+","+str(curCol-checked+1)+")")
						if(checked+1==len(word)):
							print cords
							return True
						else:
							checked = checked + 1
							continue
				else:
		
					return
		except:
			return
				
#list words to find

file = open("wordsToFind.txt", "r")
wholeText = file.read()
#split the rows
wordsToFind = wholeText.split()

for word in wordsToFind:
	findWord(word)
