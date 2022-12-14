import random
import os

def_list    = [1,1,1,1,1,1,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5]
def2_list   = [1,1,1,1,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,1,5,4]
form_list   = [1,1,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,5,5,5]
clever_list = [2,2,2,3,4,5,4,4,3,3]
proof_list  = [1,1,1,3,3,3,3,3,3,3,3,4,4,5,5]

topics = [1,2,3,4,5]
filename = "list.txt"


list = [
]

def check_l (l):
	contents=[def_list[l[0]-1],def2_list[l[1]-1],form_list[l[2]-1],clever_list[l[3]-1],proof_list[l[4]-1]]
	if ((contents[3]==contents[4]) or (contents[3]==contents[4]) or (contents[1]==contents[0])):
		return False
	else:
		if ((contents.count(4)+contents.count(5)<1) or (contents.count(3)<1)):
			return False
		else:
			for i in topics:
				if (contents.count(i) > 2):
					return False
			return True
#problem: due to the use of this skipping process the resulting distribution may be heavily nonuniform with respect to a particular problem
#possible solution -- change weights of problems after each successful ticket so that the underused ones become prioritized


i=0
while(i<60):
	random.seed()
	seed=random.randint(100,18273518246576125)
	random.seed(seed)
	l=[]
	l.append(random.randint(1,len(def_list)))
	l.append(random.randint(1,len(def2_list)))
	l.append(random.randint(1,len(form_list)))
	l.append(random.randint(2,len(clever_list)))#problem 1 was banned
	l.append(random.randint(1,len(proof_list)))
	l.append(seed)
	if check_l (l):
		list.append(l)
		i += 1

with open(filename,"a") as file_handler:
	file_handler.write('list=[\n')
	for item in list:
		file_handler.write(repr(item))
		file_handler.write(',\n')
	file_handler.write(']')