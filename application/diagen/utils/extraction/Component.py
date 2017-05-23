

class ExtractedComponent:
    
    def __init__(self):
        self.text = ""
        self.type = ""
        self.name = ""
        self.descr = ""
        self.pointer = False
        self.sentence_number = 0
        self.sentence_id = 0
        self.first_word = 0
        self.last_word = 0
        self.text_pos = 0
        self.length = 0
        self.prototype = None
    
    def __str__(self):
        return self.text


class Relation:

    def __init__(self, descr='', first_comp=None, second_comp=None):
        self.descr = descr
        self.first_comp = first_comp
        self.second_comp = second_comp

    def __str__(self):
        text = "Relation between:\n    "+str(self.first_comp)
        text += '\n    '+str(self.second_comp) + '\n with description: ' + self.descr
        return text


class Component:

    def __init__(self):
        self.type = ""
        self.name = ""
        self.descr = ""
        self.extracted_components = []

    def __str__(self):
        if len(self.name) > 0:
            text = self.type + " " + self.name
        else:
            text = self.type + " " + self.descr

        #debug info
        '''text += '\n'
        for c in self.extracted_components:
            text += str(c) + '\n'
        print(text + '\n')'''

        return text