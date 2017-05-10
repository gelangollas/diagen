from diagen.utils.extraction.Component import *

def convert_components_to_code(components, relations):
	endl = '\n'
	code = '@startuml' + endl

	for component in components:
		code += convert_component_to_code(component) + endl

	code += endl

	for relation in relations:
		code += convert_relation_to_code(relation)
	code += endl + '@enduml'

	return code

def convert_component_to_code(component):
	return '[' + str(component) + ']'

def convert_relation_to_code(relation):
	return ''