import shutil #shell utilities, this is needed to copy files
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
generate_file_with_full_list('defs.tex',def_data,'List of Definitions for the Second Oral Test')

def2_data = data_extract("List_def2.tex")
generate_file_with_full_list('defs2.tex',def2_data,'List of Definitions and Simple Questions for the Second Oral Test')

form_data = data_extract("List_formulate.tex")
generate_file_with_full_list('formulate.tex',form_data,'List of Problems to formulate smth for the Second Oral Test')

clever_data = data_extract("List_clever.tex")
generate_file_with_full_list('clever.tex',clever_data,'List of tricky problems for the Second Oral Test')

proof_data = data_extract("List_proof.tex")
generate_file_with_full_list('proofs.tex',proof_data,'List of theorems with proof for the Second Oral Test')

list=[
[20, 5, 11, 2, 6, 9842066334629037],
[3, 15, 19, 2, 3, 8694656135448847],
[27, 18, 17, 10, 2, 1125474791602691],
[7, 19, 20, 2, 5, 11290140805840840],
[23, 6, 14, 8, 7, 6267665839918960],
[24, 5, 7, 3, 2, 10647373780879441],
[28, 3, 20, 2, 9, 15838092246359425],
[24, 10, 19, 7, 9, 3628543106638556],
[15, 20, 19, 8, 15, 18219924728789101],
[34, 6, 11, 10, 2, 4771428821706527],
[26, 13, 18, 2, 15, 14484789509961120],
[22, 5, 8, 6, 2, 8587152805544725],
[4, 22, 12, 2, 6, 9939111417460489],
[25, 15, 3, 7, 4, 10313212420104468],
[15, 4, 15, 3, 1, 884008592054737],
[7, 19, 4, 6, 7, 2528830031226835],
[5, 14, 17, 2, 8, 59969007622524],
[17, 21, 21, 3, 4, 10678485300361710],
[22, 7, 9, 8, 15, 11603548467784113],
[22, 21, 20, 3, 6, 8475225162242624],
[34, 2, 12, 3, 4, 9092719905417097],
[26, 12, 17, 3, 4, 6458027032757841],
[23, 6, 17, 6, 10, 4363378111026233],
[20, 19, 21, 4, 1, 3336872506461717],
[13, 21, 21, 2, 1, 3487069564028003],
[26, 12, 2, 8, 9, 17452556594737629],
[12, 2, 10, 5, 15, 1185779502767824],
[4, 13, 18, 8, 14, 8559813158821622],
[9, 14, 17, 9, 13, 7165569303894726],
[2, 14, 16, 5, 2, 17469049110590692],
[1, 14, 9, 3, 13, 3910391817963606],
[2, 14, 4, 5, 5, 712880568207362],
[1, 12, 16, 4, 2, 8667903754723851],
[34, 14, 3, 2, 1, 1907495545074269],
[3, 11, 11, 8, 2, 17311597131420201],
[18, 1, 4, 9, 15, 9879914293992434],
[6, 18, 3, 5, 4, 4056992176317135],
[24, 19, 21, 10, 3, 3263591057466100],
[23, 11, 5, 5, 5, 13299137086905519],
[29, 18, 1, 10, 3, 5691242833420125],
[5, 11, 18, 6, 3, 14027715573879786],
[13, 7, 2, 6, 11, 7277249144991240],
[29, 9, 4, 2, 6, 2257801364149968],
[32, 9, 15, 6, 11, 15951813012172656],
[11, 4, 13, 3, 13, 12524646493752171],
[1, 21, 13, 2, 10, 567740131863684],
[2, 12, 18, 4, 12, 4137512229599287],
[12, 21, 20, 3, 11, 11433698291478945],
[14, 4, 5, 7, 8, 8465927796233168],
[23, 19, 17, 10, 15, 3539634609129504],
[32, 22, 7, 2, 5, 13004759577624470],
[29, 20, 6, 7, 8, 4581501096107571],
[24, 21, 18, 6, 9, 18182836702603778],
[23, 12, 1, 9, 13, 4385876709785992],
[9, 10, 1, 7, 10, 4993133363129669],
[21, 7, 20, 9, 3, 7247062848112674],
[32, 18, 2, 6, 7, 7395708607417268],
[24, 8, 4, 5, 7, 11342005270625905],
[30, 7, 17, 10, 13, 2492023580379459],
[19, 22, 8, 8, 2, 2743327445281663],
]

counter = 99
version = "version4"
for ticket in list:
	counter += 1
	filename = version+"/"+str(counter)+'.tex'
	shutil.copy('head2.tex',filename)
	with open(filename,"a") as file_handler:
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{Oral Test 2.}}\n\\begin{enumerate}\n')
		file_handler.write('\\item '+def_data[ticket[0]-1])
		file_handler.write('\\item '+(def2_data[(ticket[1]-1)%17]))
		file_handler.write('\\item '+form_data[ticket[2]-1])
		file_handler.write('\\item Is the following statement always true?\\\\'+clever_data[ticket[3]-1])
		file_handler.write('\\item '+proof_data[ticket[4]-1])
		file_handler.write('\\end{enumerate}\n\\end{document}')
	inputted_path = r""+filename+""
	os.system("pdflatex -interaction=batchmode -quiet -halt-on-error -output-directory=%s %s" % (version, filename) ) #todo: remove .log .aux