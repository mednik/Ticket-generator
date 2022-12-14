import shutil #shell utilities, this is needed to copy files
import os

def data_extract(filename):
	with open(filename) as file_handler:
		data = file_handler.readlines()
		result = []
		for item in data:
			if (item[0]!='%'):#we ignore all comments
				result.append(item)
		return result

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
[30, 10, 17, 7, 4, 9706961995227147],
[22, 8, 16, 5, 11, 13438659975466864],
[43, 17, 9, 5, 1, 3886841934264990],
[20, 3, 5, 5, 10, 14706822979275265],
[37, 14, 6, 2, 3, 14511753207112610],
[10, 13, 10, 3, 14, 841268952470040],
[35, 17, 8, 11, 1, 16103702363975004],
[21, 8, 5, 11, 13, 6361315582806062],
[37, 21, 12, 11, 1, 16913492893585646],
[44, 8, 1, 11, 4, 4428809475060351],
[4, 19, 13, 7, 4, 2347816273333306],
[4, 2, 13, 9, 10, 5498790895690747],
[25, 4, 12, 5, 5, 6516671647779424],
[16, 8, 17, 3, 1, 16473788594635544],
[34, 11, 14, 10, 12, 11214936579176879],
[16, 22, 15, 6, 11, 3012779052985344],
[29, 4, 8, 5, 12, 2253044160875649],
[41, 6, 2, 8, 4, 703584615223814],
[2, 17, 12, 6, 15, 5600776295810675],
[15, 1, 2, 6, 2, 4034243412374622],
[43, 14, 4, 6, 4, 13708188171660031],
[13, 21, 6, 8, 13, 14214379889977457],
[8, 2, 8, 5, 4, 628058180323511],
[42, 20, 13, 2, 9, 9597175166610797],
[23, 7, 7, 9, 14, 8293207604131496],
[28, 12, 14, 1, 10, 5348462169736064],
[48, 12, 10, 1, 7, 12232904215362834],
[14, 12, 5, 10, 13, 11249187731269832],
[5, 1, 17, 6, 4, 11951697653705076],
[50, 6, 19, 10, 9, 12496045727744204],
[19, 22, 9, 7, 3, 5355446321107532],
[26, 24, 6, 2, 15, 8856689351558427],
[10, 18, 12, 5, 12, 7114768619092132],
[42, 16, 2, 9, 5, 13387073493085392],
[30, 9, 17, 11, 10, 1016590081269291],
[43, 7, 10, 7, 5, 2308434953308910],
[44, 11, 7, 2, 11, 4494083768791307],
[45, 5, 7, 1, 11, 3574847188804803],
[37, 11, 1, 11, 4, 11479756925521552],
[4, 19, 16, 6, 4, 11399332902661882],
[45, 5, 18, 10, 7, 12787145458473483],
[39, 3, 6, 2, 6, 9241775112698703],
[6, 20, 9, 4, 5, 12122394777819508],
[39, 8, 5, 8, 9, 15653299634646257],
[15, 11, 15, 3, 5, 9278319266157284],
[24, 2, 5, 4, 3, 6725714138949714],
[8, 11, 16, 11, 7, 5035444948747260],
[28, 18, 18, 6, 2, 8153846946317445],
[6, 21, 12, 4, 11, 12068373693994649],
[6, 3, 17, 7, 9, 265642524827125],
[19, 11, 16, 11, 2, 13898933247812618],
[21, 5, 9, 7, 9, 15096288266989429],
[34, 14, 4, 10, 14, 15220936459357127],
[21, 8, 13, 11, 4, 14575459562405785],
[31, 11, 15, 8, 10, 3547535395661429],
[38, 6, 16, 10, 9, 6391995164336657],
[32, 1, 5, 4, 3, 17641746977776420],
[7, 20, 8, 5, 4, 9705650837003718],
[41, 17, 2, 10, 12, 4548267052241066],
[1, 15, 13, 3, 6, 16899272699509709],
[38, 15, 2, 7, 11, 7298300111416844],
[15, 2, 12, 1, 12, 8607909136262917],
[37, 18, 10, 2, 14, 3359978450730280],
[38, 22, 13, 8, 4, 12201191702694730],
[22, 23, 3, 9, 15, 16392057804142878],
[23, 7, 12, 7, 3, 14203289555754154],
[38, 21, 7, 3, 1, 7296204094379734],
[44, 8, 14, 10, 5, 2443512811329480],
[41, 6, 8, 10, 2, 8093255617917426],
[28, 22, 1, 5, 7, 905590047962530],
[35, 7, 9, 11, 9, 603760297459698],
[23, 14, 16, 4, 1, 12284789742602416],
[38, 9, 2, 11, 5, 7617481564016873],
[11, 13, 15, 9, 3, 4227696438073325],
[2, 15, 16, 9, 3, 4696885483622343],
[25, 4, 15, 6, 4, 18186606871283222],
[41, 22, 5, 10, 4, 4433524066938664],
[41, 5, 2, 11, 5, 4402712608270549],
[50, 22, 1, 9, 6, 15173009176612367],
[15, 8, 16, 11, 7, 6044434059250063],
[41, 14, 3, 7, 8, 15082033094299899],
[49, 13, 16, 9, 1, 2451177676425218],
[34, 22, 12, 5, 10, 9763101018815302],
[43, 3, 8, 2, 8, 3365897135224731],
[13, 20, 6, 4, 3, 9584534114004687],
[25, 18, 17, 2, 6, 948246074607137],
[30, 4, 10, 7, 6, 9254966942769991],
[13, 14, 15, 9, 6, 8643380164592300],
[46, 18, 18, 2, 11, 11660855016808832],
[37, 5, 3, 11, 9, 568749866384197],
[19, 23, 4, 9, 12, 13317419343298748],
[22, 1, 4, 7, 5, 16438854960197689],
[8, 16, 18, 9, 12, 7003839352521647],
[35, 21, 7, 8, 1, 2655483796332211],
[41, 10, 14, 3, 6, 17770648279521642],
[13, 1, 8, 7, 10, 10465048381139504],
[23, 1, 15, 10, 1, 7200976945940660],
[41, 11, 11, 8, 9, 3735164044234402],
[41, 6, 11, 6, 8, 12418667354877318],
[26, 10, 19, 7, 9, 16517847238181456],
]

counter = 0
version = "version1"
if not os.path.exists(version):
	os.makedirs(version)
from tqdm import tqdm #progress bar
for ticket in tqdm(list):
	counter += 1
	if (counter<10):
		s = "00"
	elif (counter<100):
		s = "0"
	else:
		s = ""
	
	filename = version+"/"+s+str(counter)+'.tex'
	shutil.copy('head2.tex',filename)
	with open(filename,"a") as file_handler:
		#Заголовок
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{Oral Test 2.}}\n')
		file_handler.write('\\begin{flushleft} \n\\textbf{Your name is:} \\hrulefill \\textbf{\\ \\ Your group is:}\\ \\underline{ ~~~~~~~~~~~~~}\n\\end{flushleft}\n')
		#Табличка
		file_handler.write('\\begin{table}[h!]\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n1 & 2 & 3 & 4 & 5 & $\\sum$ \\\\ \\hline\n')
		file_handler.write('\\phantom{{\\huge $\\sum$}}/2  & \\phantom{{\\huge $\\sum$}}/2  & \\phantom{{\\huge $\\sum$}}/2  &  \\phantom{{\\huge $\\sum$}}/2 &  \\phantom{{\\huge $\\sum$}}/2 & \\phantom{{\\huge $\\sum$}} /10    \\\\ \\hline\n')
		file_handler.write('\\end{tabular}\n\\end{table}\n')
		#Сам билет
		file_handler.write('\\begin{enumerate}\n')
		file_handler.write('\\item '+def_data[ticket[0]-1])
		file_handler.write('\\item '+(def2_data[ticket[1]-1]))
		file_handler.write('\\item '+form_data[ticket[2]-1])
		file_handler.write('\\item Is the following statement always true?\\\\'+clever_data[ticket[3]-1])
		file_handler.write('\\item '+proof_data[ticket[4]-1])
		file_handler.write('\\end{enumerate}\n\\end{document}')
	inputted_path = r""+filename+""
	os.system("pdflatex -interaction=batchmode -quiet -halt-on-error -output-directory=%s %s" % (version, filename) ) #todo: remove .log .aux