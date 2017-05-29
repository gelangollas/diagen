from diagen.utils.extraction.ComponentsExtractor import extract_components
from diagen.utils.extraction.RelationsExtractor import extract_relations
import string
import random
import re

def convert_text_to_code(text, component_types, component_names):
	components = extract_components(text, component_types, component_names)
	relations = extract_relations(text, components)
	code = _convert_components_to_code(components, relations)
	print('*********')
	return code

def _convert_components_to_code(components, relations):
	endl = '\n'
	aliases = ComponentAliasManager()

	code = '@startuml' + endl

	for component in components:
		print(str(component))
		code += _convert_component_to_code(component)
		code += ' as ' + aliases.get_alias(component) + endl
		if len(component.name) != 0 and len(component.descr) > 1:
			code += 'note right of ' + aliases.get_alias(component) + endl
			code += component.type + ' ' + component.descr + endl
			code += 'end note' + endl

	code += endl

	for relation in relations:
		print(relation)
		code += aliases.get_alias(relation.first_comp) + ' --> '
		code += aliases.get_alias(relation.second_comp) + ' : '
		code += relation.descr + endl
	code += endl + '@enduml'

	return code

def _convert_component_to_code(component):
	text = '[' + str(component) + ']'
	return text

def _convert_relation_to_code(relation):
	text = get_alias(relation.first_comp) + ']' + ' --> '
	text += '[' + str(relation.second_comp) + '] :' + relation.descr
	return text


class ComponentAliasManager:

	def __init__(self):
		self.aliases = {}
		self.counter = 0

	def get_alias(self, component):
		if self.aliases.get(component) == None:
			self._build_alias(component)
		return self.aliases[component]

	def _build_alias(self, component):
		result = ""
		if len(component.name) > 0:
			result = self._build_alias_from_name(component.name)
		else:
			result = self._build_common_alias()
		self.aliases[component] = result

	def _build_alias_from_name(self, name):
		words = re.findall(r"[\w]+", name)
		res = ''
		for word in words:
			res += word.title()
		return res

	def _build_common_alias(self):
		self.counter += 1
		return 'Alias' + str(self.counter)

if __name__ == '__main__':
	sample = 'модуль пользовательского окна. семантический модуль. модуль для рисования.'
	print(convert_text_to_code(sample))