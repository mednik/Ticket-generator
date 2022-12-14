import shutil #shell utilities, this is needed to copy files
import os
import random
from tqdm import tqdm

'''
Extracts data from files in the following format: there should alternate 
	lines with %# that declare a topic code 
	and 
	lines with problem formulations.
Any lines with % without # or with %%# are ignored (if ignore_comments=True) so a problem can be commented out.
'''
def data_extract(filename, topic_codes, ignore_comments=True):
	with open(filename) as file_handler:
		data = file_handler.readlines()
		result = []
		result_topic = []
		for item in data:
			if (item[0]!='%') or (ignore_comments == False):# if ignore_comments=True we ignore all TeX comments
				result.append(item)
			if ((item[0]=='%') and (item[1]=='#')): # for topic_codes we need only comments that start with %#
				result_topic.append(topic_codes[item.strip()])
		if (len(result) != len(result_topic)):
			raise AssertionError(f"For filename {filename} there are {len(result)} tickets but only {len(result_topic)} marked with %# topic code")
		return result, result_topic

def generate_file_with_full_list(filename, data, header):
	shutil.copy('head.tex', filename)
	with open(filename, "a") as file_handler: #a means append
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{'+header+'}}\n\\begin{enumerate}\n\\setlength{\\itemsep}{0pt}\n\\setlength{\\parskip}{0pt}\n')
		for item in data:
			file_handler.write('\\item '+item)
		file_handler.write('\\end{enumerate}\n\\end{document}')

'''
Applies data_extract to each file, could be done with some use of map() but would be less readable
'''
def read_data (filenames, topic_codes):
	data = {}
	data_topic = {}
	for key in filenames:
		data[key], data_topic[key] = data_extract(filenames[key], topic_codes)
	return data, data_topic
	
def generate_full_question_list (aux_filenames, data):
	for key, value in aux_filenames.items():
		generate_file_with_full_list(value[1], data[key], value[0])

def compile_full_question_list (aux_filenames):
	for key in aux_filenames:
		os.system(f"pdflatex -interaction=batchmode -quiet -halt-on-error {aux_filenames[key][1]}") 

def form_ticket (filename, ticket, data): # ticket here means "question paper" or "exam paper"
	shutil.copy('head2.tex', filename) # the tex preambule is prepared beforehands
	with open(filename, "a") as file_handler:
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{Oral Test 1.}}\n\\begin{enumerate}\n')
		#TODO better
		for key in data:
			file_handler.write('\\item '+data[key][ticket[key]-1])
		file_handler.write('\\end{enumerate}\n\\end{document}')

'''
This procedure checks whether ticket is good enough.
The checks should be handcrafted for each Oral Test separately as they represent our wishes about the ticket topics.
'''
def check_l (l, data_topics):
	if (l['def1']==l['def2']): # in the Fall Oral Test we pick 0 and 1 from the same list so they can coincide
							   # this check is superceded by a later one but it makes sense to leave it in case the later one is deleted
		return False
	
	contents={key:data_topics[key][ int(l[key])-1 ] for key in l if key!='seed'} # for each question find its topic
	
	if ((contents['clever']==contents['proof']) or (contents['def1']==contents['def2'])): # if the first two or last two questions have the same topic, that is bad
		return False
		
	contents = list(contents.values())
		
	if (contents.count('complex numbers')+contents.count('polynomials')<1): # there should be at least something about complex numbers (or at least polynomials)
		return False
	if (contents.count('determinants')<1):                       # at least smth about determinants
		return False
	if (contents.count('matrices')+contents.count('systems')<1): # at least smth about matrices or systems
		return False
	for i in contents:
		if (contents.count(i) > 2):                              # there should not be 3 questions on the same topic
			return False
	return True
#problem: due to the use of this skipping process the resulting distribution may be heavily nonuniform with respect to a particular problem
#possible solution -- change weights of problems after each successful ticket so that the underused ones become prioritized


def create_ticket (seed, data, data_topics):
	random.seed(seed)
	
	while(1):
		l={}
	
		for key in data:
			l[key] = random.randint(1, len(data[key]))
	
		if (l['def1']>l['def2']):
			l['def1'], l['def2'] = l['def2'], l['def1']
		# l['def1'], l['def2'] = sorted([l['def1'], l['def2']])
		# l['def1'], l['def2'] = min(l['def1'], l['def2']), max(l['def1'], l['def2'])

		l['seed'] = seed
	
		if check_l (l, data_topics):
			return l
	
		
def create_many_tickets (initial_seed, data, data_topics, num_required_tickets):
	random.seed(initial_seed)
	ticket_list = []
	
	for i in range(num_required_tickets):
		seed=random.randint(100,18273518246576125)
		ticket_list.append(create_ticket (seed, data, data_topics))
	
	return ticket_list

# just in case smth happens
def save_ticket_list_as_file (filename, ticket_list):
	with open(filename,"a") as file_handler:
		file_handler.write('ticket_list=[\n')
		for item in ticket_list:
			file_handler.write(repr(item))
			file_handler.write(',\n')
		file_handler.write(']')

def compile_ticket (folder, filename):
	#inputted_path = r""+filename+"" #что это была за строка? она нигде ведь не использовалась?
	os.system("pdflatex -interaction=batchmode -quiet -halt-on-error -output-directory=%s %s" % (folder, folder+'/'+filename) ) 
	#todo: remove .log .aux
	
def form_and_compile_tickets (ticket_list, data, counter_init=0, folder="version1"):
	counter = counter_init
	os.makedirs(folder, mode=0o777, exist_ok=True)
		
	for ticket in tqdm(ticket_list):
		counter += 1 # we do this manually instead of enumerate because I want to start not from 0; maybe there is some built-in option in enumerate too
		filename = f'{counter:03d}.tex' #03d means that 1 -> 001, 31 -> 031, 324 -> 324, so that all filenames have same length
		form_ticket(folder+'/'+filename, ticket, data)
		compile_ticket(folder, filename)
		

def main():
	version = 1 # increase this if you want to get more tickets without erasing previous!

	# first file is input, the second is an auxillary file to see all questions together
	input_filenames = {'def1': "List_def.tex", 
			 'def2': "List_def.tex", 
             'formulate': "List_formulate.tex",
			 'clever': "List_clever.tex",
			 'proof': "List_proof.tex",
			}
			
	auxillary_filenames = {'def1': ["List of Definitions for the First Oral Test", "defs.tex"], 
			 'def2': ["List of Definitions for the First Oral Test", "defs.tex"], # this will overwrite the previous with the same content, this is no problem
             'formulate': ["List of Problems to formulate smth for the First Oral Test", "formulate.tex"],
			 'clever': ["List of tricky problems for the First Oral Test", "clever.tex"],
			 'proof': ["List of theorems with proof for the First Oral Test", "proofs.tex"],
			}
			
	topic_code = {
		'%#matrix': 'matrices',
		'%#system': 'systems',
		'%#permutation': 'permutations',
		'%#determinant': 'determinants',
		'%#complex': 'complex numbers',
		'%#polynomial': 'polynomials',
		}
			
	data, data_topics = read_data(input_filenames, topic_code)
	print('Reading data complete.')
	
	generate_full_question_list(auxillary_filenames, data)
	print('Full question lists generated.')
	compile_full_question_list(auxillary_filenames)
	print('Full question lists compiled.')
	print('')
	
	ticket_list = create_many_tickets (initial_seed=2022, data=data, data_topics=data_topics, num_required_tickets=160)
	print('Ticket list created...')
	save_ticket_list_as_file (f"ticket_list_{version}.txt", ticket_list)
	print(f'... and saved as file ticket_list_{version}.txt.')
	
	form_and_compile_tickets (ticket_list, data, counter_init = 0, folder = f"version{version}")
	print('Tickets finished! Good luck.')
	
if __name__ == '__main__':
    main()