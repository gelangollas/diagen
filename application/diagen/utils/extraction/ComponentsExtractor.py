import subprocess
import os
import string
import random
import codecs
from .ComponentsClusterizer import cluster
from .TomitaOutputParser import *

def extract_components(text, component_types, component_names):
	session_name = _get_random_name()
	tomita = TomitaManager(session_name)
	extracted_components = tomita.run_tomita(text, component_types, component_names)
	components = cluster(extracted_components)
	return components

def _get_random_name(n=17):
	RANDOM_CHARS = string.ascii_letters + string.digits
	return ''.join([random.choice(RANDOM_CHARS) for i in range(n)])

DEFAULT_COMPONENTS = [
	'модуль',
	'компонент',
	'класс',
	'библиотека',
	'функция',
	'алгоритм',
	'файл'
]

class TomitaManager:

	def __init__(self, session_name='default', path_to_tomita='./diagen/utils/extraction/tomita/'):
		self.session_name = session_name
		self.path_to_tomita = os.path.abspath(path_to_tomita)
		self.session_files_base_path = self.path_to_tomita + '\\' + session_name
		self.tomita_config = self._build_config(session_name)

	def _build_config(self, config_name):
		CONFIG_TEMPLATE = '''encoding "utf8";
		TTextMinerConfig {{ 
			Dictionary = "{0}";
			NumThreads = 1;
			Articles = [
				{{ Name = "компоненты" }}
			]
			Facts = [
				{{ Name = "Component" }}
			]
			Input = {{
				File = "{1}";
			}}
			Output = {{
				File = "{2}";
			}}
		}}
		'''
		config = CONFIG_TEMPLATE.format(self.session_name + '.gzt', self.session_name + '.txt', self.session_name + '.xml')
		return config

	def _build_gzt(self, component_types, user_components):
		GZT_TEMPLATE = '''encoding "utf8";
		import "base.proto";
		import "articles_base.proto";
		import "facttypes.proto";
		TAuxDicArticle "тип_компонента"
		{{
			{0}
		}}
		TAuxDicArticle "компонент_пользователя"
		{{
			{1}
		}}
		TAuxDicArticle "APRO"
		{{
		    key = {{"данный" gram="A"}}
		}}
		TAuxDicArticle "компоненты"
		{{
		    key = {{ "tomita:grammar.cxx" type=CUSTOM }}
		}}
		'''
		component_types = self._format_to_dict_keys(component_types)
		user_components = self._format_to_dict_keys(user_components)
		gzt = GZT_TEMPLATE.format(component_types, user_components)
		return gzt

	def _format_to_dict_keys(self, keys):
		KEY_TEMPLATE = "key = {{\"{0}\"}}"
		COMMA = ','

		res = ''
		n = len(keys)
		for i in range(n-1):
			res += KEY_TEMPLATE.format(keys[i]) + COMMA
		if n > 0:
			res += KEY_TEMPLATE.format(keys[n-1])
		return res

	def run_tomita(self, text, component_types=DEFAULT_COMPONENTS, user_components=[], clear=True):
		f = codecs.open(self.session_files_base_path + '.txt', 'w', 'utf-8')
		f.write(text)
		f.close()

		print(component_types)
		print(user_components)

		f = codecs.open(self.session_files_base_path + '.gzt', 'w', 'utf-8')
		f.write(self._build_gzt(component_types, user_components))
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
		os.remove(self.session_files_base_path + '.gzt')
		os.remove(self.session_files_base_path + '.gzt.bin')



