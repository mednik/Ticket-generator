import random
import os

filename = "list2.txt"


list = [
]

topic_code = {
'%#matrix': 1,
'%#system': 2,
'%#permutation': 3,
'%#determinant': 4,
'%#complex': 5,
'%#polynomial': 6,
}
topics = [1,2,3,4,5,6]	

def data_extract(filename):
	with open(filename) as file_handler:
		data = file_handler.readlines()
		result = []
		for item in data:
			if ((item[0]=='%') and (item[1]=='#')):#we need only comments that start with %#
				result.append(topic_code[item.strip()])
		return result

def_list    = data_extract("List_def.tex")
#def2_list   = data_extract() #in the First test there are no def2
form_list   = data_extract("List_formulate.tex")
clever_list = data_extract("List_clever.tex")
proof_list  = data_extract("List_proof.tex")


def check_l (l):
	if (l[0]==l[1]):#we pick 0 and 1 from the same list so they can coincide
		return False
	contents=[def_list[l[0]-1],def_list[l[1]-1],form_list[l[2]-1],clever_list[l[3]-1],proof_list[l[4]-1]]
	if ((contents[3]==contents[4]) or (contents[1]==contents[0])): #if the first two or last two questions have the same topic, that is bad
		return False
	if (contents.count(5)+contents.count(6)<1):#there should be at least something about complex numbers (or at least polynomials)
		return False
	if (contents.count(4)<1):                  #at least smth about determinants
		return False
	if (contents.count(0)+contents.count(2)<1):#at least smth about matrices or systems
		return False
	for i in topics:
		if (contents.count(i) > 2):#there should not be 3 questions on the same topic
			return False
	return True
#problem: due to the use of this skipping process the resulting distribution may be heavily nonuniform with respect to a particular problem
#possible solution -- change weights of problems after each successful ticket so that the underused ones become prioritized


i=0
while(i<100):
	random.seed()
	seed=random.randint(100,18273518246576125)
	random.seed(seed)
	l=[]
	l.append(random.randint(1,len(def_list)))
	l.append(random.randint(1,len(def_list))) #in First test we use the same list twice
	if (l[0]>l[1]):
		x = l[0]
		l[0]=l[1]
		l[1]=x
	l.append(random.randint(1,len(form_list)))
	l.append(random.randint(1,len(clever_list)))
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