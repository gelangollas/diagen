from diagen.utils.extraction.TomitaManager import *
from .ComponentsConvertor import convert_components_to_code
import string
import random

def convert_text_to_code(text):
	components = extract_components(text)
	relations = extract_relations(text, components)
	code = convert_components_to_code(components, relations)

	return code

def extract_components(text):
	session_name = get_random_name()
	tomita = TomitaManager(session_name)
	components = tomita.run_tomita(text)
	return components

def extract_relations(text, components):
	return []

def get_random_name(n=17):
	RANDOM_CHARS = string.ascii_letters + string.digits
	return ''.join([random.choice(RANDOM_CHARS) for i in range(n)])


if __name__ == '__main__':
	sample = 'модуль пользовательского окна. семантический модуль. модуль для рисования.'
	print(convert_text_to_code(sample))