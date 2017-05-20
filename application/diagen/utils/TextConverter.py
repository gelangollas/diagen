from diagen.utils.extraction.TomitaManager import *
from diagen.utils.extraction.Component import *
from diagen.utils.extraction.ComponentsClusterizer import cluster
import string
import random

def convert_text_to_code(text):
	components = _extract_components(text)
	relations = _extract_relations(text, components)
	code = _convert_components_to_code(components, relations)
	return code

def _extract_components(text):
	session_name = _get_random_name()
	tomita = TomitaManager(session_name)
	extracted_components = tomita.run_tomita(text)
	components = cluster(extracted_components)
	return components

def _extract_relations(text, components):
	return []

def _get_random_name(n=17):
	RANDOM_CHARS = string.ascii_letters + string.digits
	return ''.join([random.choice(RANDOM_CHARS) for i in range(n)])

def _convert_components_to_code(components, relations):
	endl = '\n'
	code = '@startuml' + endl

	for component in components:
		code += _convert_component_to_code(component) + endl

	code += endl

	for relation in relations:
		code += _convert_relation_to_code(relation)
	code += endl + '@enduml'

	return code

def _convert_component_to_code(component):
	return '[' + str(component) + ']'

def _convert_relation_to_code(relation):
	return ''

if __name__ == '__main__':
	sample = 'модуль пользовательского окна. семантический модуль. модуль для рисования.'
	print(convert_text_to_code(sample))