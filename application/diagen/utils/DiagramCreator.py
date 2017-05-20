import string
import random
import os
import subprocess
from subprocess import STDOUT

def build_diagram_from_code(code, path_to_builder='./diagen/utils/plantuml/', path_to_img='./diagen/static/diagrams/'):
	file_name = get_random_name()
	f = open(path_to_img + file_name + '.txt', 'w')
	f.write(code)
	f.close()

	try:
		subprocess.check_output(['java', '-jar', path_to_builder + 'plantuml.jar', path_to_img+file_name+'.txt'], stderr=STDOUT)
	except subprocess.CalledProcessError as exc:
		os.remove(path_to_img + file_name + '.txt')
		raise Exception(exc.output)

	os.remove(path_to_img + file_name + '.txt')
	return file_name+'.png'

def get_random_name(n=17):
	RANDOM_CHARS = string.ascii_letters + string.digits
	return ''.join([random.choice(RANDOM_CHARS) for i in range(n)])

if __name__ == '__main__':
	code = '@startuml\nBob->Alice : hello\n@enduml'
	file = build_diagram_from_code(code)
	print(file)