import shutil #this is needed to copy files
import os

def data_extract(filename):
	with open(filename) as file_handler:
		return file_handler.readlines()

def generate_file_with_full_list(filename,data,header):
	shutil.copy('head.tex',filename)
	with open(filename,"a") as file_handler: #a means append
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{'+header+'}}\n\\begin{enumerate}\n\\setlength{\\itemsep}{0pt}\n\\setlength{\\parskip}{0pt}\n')
		for item in data:
			file_handler.write('\\item '+item)
		file_handler.write('\\end{enumerate}\n\\end{document}')

def_data = data_extract("List_def.tex")
generate_file_with_full_list('defs.tex',def_data,'List of Definitions for the First Oral Test')

form_data = data_extract("List_formulate.tex")
generate_file_with_full_list('formulate.tex',form_data,'List of Problems to formulate smth for the First Oral Test')

clever_data = data_extract("List_clever.tex")
generate_file_with_full_list('clever.tex',clever_data,'List of tricky problems for the First Oral Test')

proof_data = data_extract("List_proof.tex")
generate_file_with_full_list('proofs.tex',proof_data,'List of theorems with proof for the First Oral Test')

list1 = [
[14,6,3,17,24],
[16,18,7,13,10],
[12,21,6,9,25],
[8,18,11,30,9],
[13,15,10,19,24],
[22,3,13,31,8],
[7,25,2,32,15],
[9,13,12,33,29],
[14,24,1,34,28],
[23,21,6,2,27],
[27,19,8,35,26],
[18,16,14,36,30],
[13,22,15,37,6],
[2,12,9,38,15],
[26,6,1,31,8],
]

list2 = [
[3,17,4,1,20],
[4,20,5,8,21]
]

list = [
[5,11,4,7,22],
[10,25,7,10,19],
[4,1,11,15,17],
[2,25,10,6,30]
]

counter = 60
version = "version4"
for ticket in list:
	counter += 1
	filename = version+"/"+str(counter)+'.tex'
	shutil.copy('head2.tex',filename)
	with open(filename,"a") as file_handler:
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{Oral Test 1.}}\n\\begin{enumerate}\n')
		file_handler.write('\\item '+def_data[ticket[0]-1])
		file_handler.write('\\item '+def_data[ticket[1]-1])
		file_handler.write('\\item '+form_data[ticket[2]-1])
		file_handler.write('\\item Is the following statement always true?\\\\'+clever_data[ticket[3]-1])
		file_handler.write('\\item '+proof_data[ticket[4]-1])
		file_handler.write('\\end{enumerate}\n\\end{document}')
	inputted_path = r""+filename+""
	os.system("pdflatex -interaction=batchmode -quiet -halt-on-error -output-directory=%s %s" % (version, filename) ) #todo: remove .log .aux