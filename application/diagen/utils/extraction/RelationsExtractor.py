from .Component import *
import pymorphy2
import re
import time

def extract_relations(text, components):
	relations = []
	n = len(components)
	for i in range(n):
		for j in range(i+1, n):
			res, rel = _try_find_relations(text, components[i], components[j])
			if res:
				relations.extend(rel)
	return relations

def _try_find_relations(text, c1, c2):
	is_found = False
	relations = []

	extr1 = c1.extracted_components
	extr2 = c2.extracted_components
	n1 = len(extr1)
	n2 = len(extr2)
	i1, i2 = 0, 0

	while i1 < n1 and i2 < n2:
		sn1 = extr1[i1].sentence_number
		sn2 = extr2[i2].sentence_number

		if sn1 == sn2:
			res_found, relation = _try_find_relation_in_sentence(text, extr1[i1], extr2[i2])
			if res_found:
				relations.append(relation)
				is_found = True
			i1 += 1
			i2 += 1
		elif sn1 > sn2:
			i2 += 1
		else:
			i1 += 1

	return is_found, relations

def _try_find_relation_in_sentence(text, c1, c2):
	if c1.text_pos > c2.text_pos:
		c1, c2 = c2, c1
	i = c1.text_pos + c1.length
	j = c2.text_pos
	text_between_components = text[i:j]
	print(text_between_components)

	words = re.findall(r"[\w']+", text_between_components)

	for word in reversed(words):
		if _is_relation_verb(word):
			return True, Relation(word, c1.prototype, c2.prototype)

	return False, None

analyzer = pymorphy2.MorphAnalyzer()
def _is_relation_verb(word):
	tag = analyzer.parse(word)[0].tag
	if 'VERB' in tag:
		return True
	return False