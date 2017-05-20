from .Component import *
import pymorphy2
import re

def cluster(extracted_components):
	extr_comp = extracted_components
	comparer = _ComponentComparer(extr_comp)

	# строим граф, где вершины - компоненты
	# ребро между компонентами проводится, если компаратор посчитает компоненты тождественными
	n = len(extr_comp)
	to = [[] for _ in range(n)]

	for i in range(n):
		for j in range(i+1, n):
			if comparer.equals(extr_comp[i], extr_comp[j]):
				to[i].append(j)
				to[j].append(i)

	# обходим граф и помечаем каждую компоненту связности уникальным индексом
	was = [-1]*n
	set_id = 0
	for i in range(n):
		if was[i] == -1:
			_dfs(i, set_id, was, to)
			set_id += 1

	# группируем компоненты связности по массивам
	component_sets = [[] for _ in range(set_id)]
	for i, c in enumerate(extr_comp):
		idx = was[i]
		component_sets[idx].append(c)

	#получаем для каждого множества извлеченных компонентов один тождественный им всем
	components = _build_components_from_sets(component_sets)
	return components

def _dfs(u, color, used, to):
	if used[u] != -1:
		return
	used[u] = color

	for v in to[u]:
		_dfs(v, color, used, to)

def _build_components_from_sets(sets):
	components = []
	for one_set in sets:
		components.append(_build_component_from_set(one_set))

	return components

def _build_component_from_set(one_set):
	comp = Component()
	comp.extracted_components = one_set
	comp.descr = " "

	for c in one_set:
		if c.pointer:
			continue

		if len(c.name) > 0:
			comp.name = c.name

		if len(c.type) > 0 and c.type != 'default':
			comp.type = c.type

		if len(c.descr) > len(comp.descr):
			comp.descr = c.descr

	return comp


class _ComponentComparer:

	def __init__(self, components):
		self.cache = {}
		self.components = components
		self.components_index = {}
		self.morph = pymorphy2.MorphAnalyzer()
		for i, component in enumerate(components):
			self.components_index[component] = i

	def equals(self, c1, c2):
		if self.cache.get((c1, c2)) == None:
			self._compare(c1, c2, cache_result=True)
		return self.cache[(c1, c2)]

	def _compare(self, c1, c2, cache_result=True):
		result = False

		#сравнение по именам компонентов
		if self._have_names(c1, c2) and self._name_compare(c1, c2):
			result = True
		
		#если один из компонентов выполняет указательную функцию
		#то узнать, указывает ли описание одного компонента на другой
		if not result and ((c1.pointer or c2.pointer) and self._is_one_point_to_other(c1, c2)):
			result = True
		
		#сравнение по описанию компонентов
		if not result and not self._have_names(c1, c2) and (not (c1.pointer and c2.pointer) and self._description_compare(c1, c2)):
			result = True
		
		if cache_result:
			self.cache[(c1, c2)] = result
			self.cache[(c2, c1)] = result

		return result

	def _name_compare(self, c1, c2):
		return c1.name == c2.name

	def _have_names(self, c1, c2):
		if len(c1.name) == 0 or len(c2.name) == 0:
			return False
		return True

	def _is_one_point_to_other(self, c1, c2):
		if not (c2.pointer and c2.sentence_number - c1.sentence_number <= 2 and c2.sentence_number >= c1.sentence_number):
			return False

		if not c1.type == c2.type:
			return False

		i1, i2 = self.components_index[c1], self.components_index[c2]
		i = i2-1
		while i > i1:
			if self.components[i].type == c2.type:
				return False
			i -= 1

		return True

	def _is_service_part_of_speech(self, word):
		tag = self.morph.parse(word)[0].tag
		if 'PRCL' in tag or 'PREP' in tag or 'CONJ' in tag:
			return True
		return False 

	def _description_compare(self, c1, c2):
		if c1.type != c2.type:
			return False

		if c1.descr == c2.descr:
			return True

		descr_words1 = set(re.findall(r"[\w']+", c1.descr))
		descr_words2 = set(re.findall(r"[\w']+", c2.descr))

		if len(descr_words1) > len(descr_words2):
			descr_words1, descr_words2 = descr_words2, descr_words1

		non_serv_words1 = 0
		non_serv_words2 = 0
		match = 0

		for word in descr_words1:
			if self._is_service_part_of_speech(word):
				non_serv_words1 += 1
				continue 

			if word in descr_words2:
				match += 1

		for word in descr_words2:
			if self._is_service_part_of_speech(word):
				non_serv_words2 += 1

		if len(descr_words2) - non_serv_words2 >= match*2:
			return False
		return True
