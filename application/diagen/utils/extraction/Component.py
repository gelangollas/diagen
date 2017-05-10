

class ExtractedComponent:
    
    def __init__(self):
        self.text = ""
        self.type = ""
        self.name = ""
        self.descr = ""
        self.pointer = False
        self.sentence_number = 0
        self.first_word = 0
        self.last_word = 0
        self.text_pos = 0
        self.length = 0
    
    def __str__(self):
        return self.text


class ExtractedRelation:

	def __init__(self):
		self.descr = ''
		self.name = ''
		self.type = ''
		self.first_comp = None
		self.second_comp = None