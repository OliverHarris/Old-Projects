# Project - word search
This was developed in my A-level. The task was given by the teacher to complete a word search on paper so I decided to develop a program.
I only allowed up to two hours to complete this task as I didn't want it to be too complicated. 

## Version one
This is the "find.py". This doesn't have an interface but tasks two files and outputs the locations to the terminal like so:
```
finding  ALU 
['A~(2,23)', 'L~(2,22)', 'U~(2,21)']
```

## Version two
I started to create an interface using pythons tkinter. This somewhat works but isn't as developed as find.py.
It currently highlights every time it finds the first letter, and stops when it finds the complete word. This can make it 
confusing to read, but it also squashes up the characters which is even harder.
- To fix this I can add +n to the found characters number and when the program redisplays the word search, to add a space after each character
