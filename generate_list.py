import random
import os

filename = "list2.txt"


list = [
]

topic_code = {
'%#vector': 1,
'%#rank': 2,
'%#operators': 3,
'%#spectral': 4,
'%#functional': 5,
'%#bilinear': 6,
'%#euclidian': 7,
}
topics = [1,2,3,4,5,6,7]	

def data_extract(filename):
	with open(filename) as file_handler:
		data = file_handler.readlines()
		result = []
		for item in data:
			if ((item[0]=='%') and (item[1]=='#')):#we need only comments that start with %#
				result.append(topic_code[item.strip()])
		return result

def_list    = data_extract("List_def.tex")
def2_list   = data_extract("List_def2.tex") #in the Second test there is def2
form_list   = data_extract("List_formulate.tex")
clever_list = data_extract("List_clever.tex")
proof_list  = data_extract("List_proof.tex")


def check_l (l):
	if (l[0]==l[1]):#we pick 0 and 1 from the same list so they can coincide
		return False
	contents=[def_list[l[0]-1],def2_list[l[1]-1],form_list[l[2]-1],clever_list[l[3]-1],proof_list[l[4]-1]]
	if ((contents[3]==contents[4]) or (contents[1]==contents[0])): #if the first two or last two questions have the same topic, that is bad
		return False
	if (contents.count(1)+contents.count(2)<1):#there should be at least something about vector spaces or ranks
		return False
	if (contents.count(3)+contents.count(5)<1):          #at least smth about operators or covectors
		return False
	if (contents.count(4)<1):          #at least smth about spectral
		return False
	if (contents.count(6)+contents.count(7)<1):  #at least smth about bilinear or euclidian
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
	l.append(random.randint(1,len(def2_list))) #in Second test def2 exists
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