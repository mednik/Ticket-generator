import shutil #shell utilities, this is needed to copy files
import os
import random
from tqdm import tqdm
import json
from pathlib import Path
import logging
import subprocess

# Constants
LATEX_AUX_EXTENSIONS = [".aux", ".log", ".out"]
DEFAULT_MAX_ATTEMPTS = 10000000
DEFAULT_SEED_RANGE = (100, 18273518246576125)

# Set up logging
# Create formatters
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(levelname)s - %(message)s')

# Create handlers
file_handler = logging.FileHandler('generation.log')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)  # File gets all messages INFO and above

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
console_handler.setLevel(logging.ERROR)  # Console only gets ERROR and above

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def cleanup_latex_aux_files(output_dir: Path, base_name: str):
	for ext in LATEX_AUX_EXTENSIONS:
		file_path = output_dir / (base_name + ext)
		try:
			file_path.unlink(missing_ok=True)
		except OSError as e:
			logger.warning(f"Could not delete {file_path}: {e}")
			# Log more details about the error
			logger.debug(f"Error details: {str(e)}", exc_info=True)

'''
Extracts data from files in the following format: there should alternate 
	lines with %# that declare a topic code 
	and 
	lines with problem formulations.
Any lines with % without # or with %%# are ignored (if ignore_comments=True) so a problem can be commented out.
'''
def data_extract(filename: Path, topic_codes, ignore_comments=True):
	logger.info(f"Extracting data from {filename}")
	with open(filename, encoding='utf-8') as file_handler:
		data = file_handler.readlines()
		result = []
		result_topic = []
		parsing = False
		for item in data:
			if not parsing:
				if '\\itemsep' in item:
					parsing = True
				continue
			if '\\end{enumerate}' in item:
				break
			if not item.startswith('%') or not ignore_comments:
				result.append(item)
			if item.startswith('%#'): # for topic_codes we need only comments that start with %#
				result_topic.append(topic_codes[item.strip()])
		if len(result) != len(result_topic):
			logger.error(f"For filename {filename} there are {len(result)} tickets but only {len(result_topic)} marked with %# topic code")
			raise AssertionError(f"For filename {filename} there are {len(result)} tickets but only {len(result_topic)} marked with %# topic code")
		logger.info(f"Successfully extracted {len(result)} items from {filename}")
		return result, result_topic

def generate_file_with_full_list(filename: Path, data, header):
	logger.info(f"Generating full list file: {filename}")
	shutil.copy('head.tex', filename)
	with open(filename, "a", encoding='utf-8') as file_handler: #a means append
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{'+header+'}}\n\\begin{enumerate}\n\\setlength{\\itemsep}{0pt}\n\\setlength{\\parskip}{0pt}\n')
		for item in data:
			file_handler.write('\\item '+item)
		file_handler.write('\\end{enumerate}\n\\end{document}')
	logger.info(f"Full list file generated successfully: {filename}")

'''
Applies data_extract to each file, could be done with some use of map() but would be less readable
'''
def read_data(filenames: dict[str, Path], topic_codes):
	logger.info("Starting to read data from all files")
	data = {}
	data_topic = {}
	for key in filenames:
		logger.info(f"Processing file: {filenames[key]}")
		data[key], data_topic[key] = data_extract(filenames[key], topic_codes)
	logger.info("Finished reading all data files")
	return data, data_topic
	
def form_ticket(filename: Path, ticket, data, exam_name): # ticket here means "question paper" or "exam paper"
	logger.info(f"Forming ticket: {filename}")
	shutil.copy('head2.tex', filename) # the tex preambule is prepared beforehands
	with open(filename, "a", encoding='utf-8') as file_handler:
		file_handler.write('\\begin{document} \n\\centerline{\\textbf{'+exam_name+'}}\n')
		#TODO better
		l = {}
		for key in data:
			l[key] = (data[key][ticket[key]-1]).removeprefix(r'\item ')
		
		# Format the ticket content
		ticket_content = [
			'~\\\\',
			'\\textbf{Определения}. \\\\',
			f'1. (1 балл) {l["def1"]} \\\\',
			f'2. (1 балл) {l["def2"]} \\\\',
			'\\textbf{Формулировка}. \\\\',
			f'1. (1 балл) {l["formulate"]} \\\\',
			'\\textbf{Алгоритм}. \\\\',
			f'1. (2 балла) {l["algorithm"]} \\\\',
			'\\textbf{Доказательства}. \\\\',
			f'1. (2 балла) {l["proof1"]} \\\\',
			f'1. (3 балла) {l["proof2"]} \\\\',
			'\\end{document}'
		]
		file_handler.write('\n'.join(ticket_content))
	logger.info(f"Ticket formed successfully: {filename}")

'''
This procedure checks whether ticket is good enough.
The checks should be handcrafted for each Oral Test separately as they represent our wishes about the ticket topics.
'''
def check_l (l, data_topics, topic_rules):
	if (l['def1']==l['def2']): # in the Oral Test we pick 0 and 1 from the same list so they can coincide
							   # this check is superceded by a later one but it makes sense to leave it in case the later one is deleted
		return False
		
	contents={key:data_topics[key][ int(l[key])-1 ] for key in l if key!='seed'} # for each question find its topic
	
	if ((contents['proof2']==contents['proof1']) or (contents['def1']==contents['def2'])): # if the first two or last two questions have the same topic, that is bad
		return False
		
	contents = list(contents.values())
	
	# Check minimum required counts for individual topics
	for topic, min_count in topic_rules['required_min_counts'].items():
		if contents.count(topic) < min_count:
			return False
			
	# Check combined requirements
	for combined_req in topic_rules.get('combined_requirements', []):
		total_count = sum(contents.count(topic) for topic in combined_req['topics'])
		if total_count < combined_req['min_count']:
			return False
			
	# Check maximum count per topic
	for topic in set(contents):
		if contents.count(topic) > topic_rules['max_count_per_topic']:
			return False
			
	return True

def create_ticket(seed, data, data_topics, topic_rules, max_attempts=DEFAULT_MAX_ATTEMPTS):
	random.seed(seed)
	
	for _ in range(max_attempts):
		l = {key: random.randint(1, len(data[key])) for key in data}
		l['def1'], l['def2'] = sorted([l['def1'], l['def2']])
		l['seed'] = seed
		
		if check_l(l, data_topics, topic_rules):
			return l
	raise ValueError(f"Could not generate valid ticket after {max_attempts} attempts")

def create_many_tickets (initial_seed, data, data_topics, num_required_tickets, topic_rules):
	random.seed(initial_seed)
	ticket_list = []
	
	for i in tqdm(range(num_required_tickets), desc="Generating tickets"):
		try:
			seed = random.randint(*DEFAULT_SEED_RANGE)
			ticket = create_ticket(seed, data, data_topics, topic_rules)
			ticket_list.append(ticket)
		except ValueError as e:
			logger.error(f"Failed to generate ticket {i+1}: {str(e)}")
			raise
			
	return ticket_list

# just in case smth happens
def save_ticket_list_as_file (filename, ticket_list):
	logger.info(f"Saving ticket list to {filename}")
	with open(filename, "a", encoding='utf-8') as file_handler:
		file_handler.write('ticket_list=[\n')
		file_handler.write(',\n'.join(repr(item) for item in ticket_list))
		file_handler.write('\n]')
	logger.info(f"Ticket list saved successfully to {filename}")

def compile_ticket(folder: Path, filename: str):
	logger.info(f"Compiling LaTeX file: {filename}")
	cmd = ["pdflatex", "-interaction=batchmode", "-quiet", "-halt-on-error", 
		   f"-output-directory={folder}", str(folder/filename)]
	
	try:
		result = subprocess.run(cmd, capture_output=True, text=True)
		if result.returncode != 0:
			logger.error(f"Failed to compile {filename}")
			logger.error(f"LaTeX error output: {result.stderr}")
		else:
			logger.info(f"Successfully compiled {filename}")
	except subprocess.SubprocessError as e:
		logger.error(f"Error running pdflatex: {e}")
		raise
	
	# Clean up auxiliary files
	base_name = Path(filename).stem
	cleanup_latex_aux_files(folder, base_name)

def form_and_compile_tickets(ticket_list, data, counter_init=0, folder: Path = Path("version1"), exam_name="Коллоквиум"):
	logger.info(f"Starting to form and compile {len(ticket_list)} tickets in {folder}")
	counter = counter_init
	folder.mkdir(mode=0o777, exist_ok=True)
		
	for ticket in tqdm(ticket_list):
		counter += 1 # we do this manually instead of enumerate because I want to start not from 0; maybe there is some built-in option in enumerate too
		filename = f'{counter:03d}.tex' # 03d means that 1 -> 001, 31 -> 031, 324 -> 324, so that all filenames have same length
		form_ticket(folder/filename, ticket, data, exam_name)
		compile_ticket(folder, filename)
	logger.info(f"Finished forming and compiling all tickets in {folder}")

def main():
	logger.info("Starting ticket generation process")
	# Get configuration file from user
	print("Please select configuration file:")
	print("1. config_fall.json")
	print("2. config_spring.json")
	choice = input("Enter 1 or 2: ").strip()
	
	config_file = Path("config_fall.json" if choice == "1" else "config_spring.json")
	logger.info(f"Selected configuration file: {config_file}")
	
	# Load configuration
	with open(config_file, 'r', encoding='utf-8') as f:
		config = json.load(f)
	logger.info("Configuration loaded successfully")
	
	version = 2 # increase this if you want to get more tickets without erasing previous!

	# Build input filenames from config
	input_filenames = {}
	base_path = Path(config['base_data_path'])
	for key, filename in config['input_file_map'].items():
		input_filenames[key] = base_path / filename
			
	topic_code = config['topic_codes']
			
	data, data_topics = read_data(input_filenames, topic_code)
	print('Reading data complete.')
	
	ticket_list = create_many_tickets(
		initial_seed=2025,
		data=data,
		data_topics=data_topics,
		num_required_tickets=100,
		topic_rules=config['topic_rules']
	)
	print('Ticket list created...')
	save_ticket_list_as_file(Path(f"ticket_list_{version}.txt"), ticket_list)
	print(f'... and saved as file ticket_list_{version}.txt.')
	
	output_folder = Path(config['output_folder_prefix'] + str(version))
	form_and_compile_tickets(
		ticket_list,
		data,
		counter_init=0,
		folder=output_folder,
		exam_name=config['exam_name']
	)
	print('Tickets finished! Good luck.')
	logger.info("Ticket generation process completed successfully")
	
if __name__ == '__main__':
	main()