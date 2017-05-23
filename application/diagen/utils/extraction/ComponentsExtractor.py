import subprocess
import os
import string
import random
import codecs
from .ComponentsClusterizer import cluster
from .TomitaOutputParser import *

def extract_components(text):
	session_name = _get_random_name()
	tomita = TomitaManager(session_name)
	extracted_components = tomita.run_tomita(text)
	components = cluster(extracted_components)
	return components

def _get_random_name(n=17):
	RANDOM_CHARS = string.ascii_letters + string.digits
	return ''.join([random.choice(RANDOM_CHARS) for i in range(n)])

class TomitaManager:

	def __init__(self, session_name='default', path_to_tomita='./diagen/utils/extraction/tomita/'):
		self.session_name = session_name
		self.path_to_tomita = os.path.abspath(path_to_tomita)
		self.session_files_base_path = self.path_to_tomita + '\\' + session_name
		self.tomita_config = self._build_config(session_name)

	def _build_config(self, config_name):
		CONFIG_TEMPLATE = '''encoding "utf8";
		TTextMinerConfig {{ 
			Dictionary = "dic.gzt";
			NumThreads = 1;
			Articles = [
				{{ Name = "компоненты" }}
			]
			Facts = [
				{{ Name = "Component" }}
			]
			Input = {{
				File = "{0}";
			}}
			Output = {{
				File = "{1}";
			}}
		}}
		'''
		config = CONFIG_TEMPLATE.format(self.session_name + '.txt', self.session_name + '.xml')
		return config

	def run_tomita(self, text, clear=True):
		f = codecs.open(self.session_files_base_path + '.txt', 'w', 'utf-8')
		f.write(text)
		f.close()

		f = codecs.open(self.session_files_base_path + '.proto', 'w', 'utf-8')
		f.write(self.tomita_config)
		f.close()
		
		subprocess.Popen([self.path_to_tomita + '\\' + 'tomitaparser.exe', 
			self.session_name + '.proto'], cwd=self.path_to_tomita).wait()

		parser = TomitaOutputParser(self.session_files_base_path + '.xml')
		components = parser.get_components()

		if clear:
			self._perform_clean()
		return components

	def _perform_clean(self):
		os.remove(self.session_files_base_path + '.txt')
		os.remove(self.session_files_base_path + '.proto')
		os.remove(self.session_files_base_path + '.xml')



