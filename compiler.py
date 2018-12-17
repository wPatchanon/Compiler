file = input("Enter File Name: ")
f = open(file,"r")

token_List = []
for line in f:
	token_List += line.strip().split()
#print(token_List)
token_List.append('EOF')

grammar = {
	('pgm','line_num') : ['line','pgm'],
	('pgm','EOF') : ['EOF'],
	('line','line_num') : ['line_num','stmt'],
	('stmt','id') : ['asgmnt'],
	('stmt','IF') : ['if'],
	('stmt','PRINT') : ['print'],
	('stmt','GOTO') : ['goto'],
	('stmt','STOP') : ['stop'],
	('asgmnt','id') : ['id','=','exp'],
	('exp','id') : ['term','expc'],
	('exp','const') : ['term','expc'],
	('expc','EOF') : [],
	('expc','line_num') : [],
	('expc','+') : ['+','term'],
	('expc','-') : ['-','term'],
	('term','id') : ['id'],
	('term','const') : ['const'],
	('if','IF') : ['IF','cond','line_num'],
	('cond','id') : ['term','condc'],
	('cond','const') : ['term','condc'],
	('condc','=') : ['=','term'],
	('condc','<') : ['<','term'],
	('print','PRINT') : ['PRINT','id'],
	('goto','GOTO') : ['GOTO','line_num'],
	('stop','STOP') : ['STOP']
}

terminal = {
	'EOF' : 1,
	'line_num' : 10,
	'id' : 11,
	'=' : 17,
	'+' : 17,
	'-' : 17,
	'const' : 12,
	'IF' : 13,
	'<' : 17,
	'PRINT' : 15,
	'GOTO' : 14,
	'STOP' : 16
}

state = ""
stack = ['pgm']
goto = False

for token in token_List:
	err = False
	if len(token) == 1 and token >= 'A' and token <= 'Z':
		toktype = 'id'
	elif token.isdigit():
		token = int(token)
		if 1 <= token <= 100:
			if (stack[-1],'const') in grammar:
				toktype = 'const'
			else:
				toktype = 'line_num'
		elif token <= 1000:
			toktype = 'line_num'
		else :
			err = True
	else:
		toktype = token
	
	match = False
	while(match == False and err == False):
		state = stack.pop()
		if state == 'cond' or state == 'goto':
			goto = True
		if state in terminal:
			match = True
			if state != toktype :
				err = True
		else :
			if (state,toktype) in grammar:
				stack += grammar[(state,toktype)][::-1]
			else :
				err = True
	if err :
		print()
		print('Compile Error ---- Line:: ' + str(line) + ' Token: "' + str(token) + '"')
		break

	if toktype == 'line_num' :
		if goto :
			print("14"+" "+str(token),end = ' ')
			goto = False
		else :
			line = token
			print()
			print(str(terminal[toktype])+" "+str(token),end = ' ')
	elif toktype == 'id' :
		print(str(terminal[toktype])+" "+str(ord(token)-64), end = ' ')
	elif toktype == '+' :
		print(str(terminal[toktype])+" 1",end = ' ')
	elif toktype == '-' :
		print(str(terminal[toktype])+" 2",end = ' ')
	elif toktype == '<' :
		print(str(terminal[toktype])+" 3",end = ' ')
	elif toktype == '=' :
		print(str(terminal[toktype])+" 4",end = ' ')
	elif toktype == 'IF' or toktype == 'PRINT' or toktype == 'STOP':
		print(str(terminal[toktype])+" 0",end = ' ')
	elif toktype == 'EOF' :
		print("\n0")
	elif toktype != 'GOTO':
		print(str(terminal[toktype])+" "+str(token),end = ' ')
print()
if stack == []:
	print("---- Compile Successful ----")

