from xml.dom import minidom

class TomitaOutputParser:
    """TODO"""
    
    def __init__(self, path):
        self.xmldoc = minidom.parse(path)
        
    def get_components(self):
        components = []
        for comp in self.xmldoc.getElementsByTagName('Component'):
            components.append(self.__construct_component(comp))
        return components
    
    def __construct_component(self, component_xml):
        to_construct = ExtractedComponent()
        to_construct.type = self.__extract_component_element(component_xml, 'Type')
        to_construct.name = self.__extract_component_element(component_xml, 'Name')
        to_construct.descr = self.__extract_component_element(component_xml, 'Description')
        to_construct.pointer = bool(self.__extract_component_element(component_xml, 'Pointer'))
        to_construct.sentence_number = int(self.__extract_component_attribute(component_xml, 'sn'))
        to_construct.first_word = int(self.__extract_component_attribute(component_xml, 'fw'))
        to_construct.last_word = int(self.__extract_component_attribute(component_xml, 'lw'))
        to_construct.text_pos = int(self.__extract_component_attribute(component_xml, 'pos'))
        to_construct.length = int(self.__extract_component_attribute(component_xml, 'len'))
        to_construct.text = self.__extract_component_text(component_xml)
        return to_construct
    
    def __extract_component_attribute(self, component_xml, attr_name):
        return component_xml.attributes[attr_name].value
    
    def __extract_component_element(self, component_xml, el_name):
        el =  component_xml.getElementsByTagName(el_name)
        if len(el) == 0:
            return ""
        return el[0].attributes['val'].value
    
    def __extract_component_text(self, component_xml):
        lead_id_needed = self.__extract_component_attribute(component_xml, 'LeadID')
        leads = self.xmldoc.getElementsByTagName('Lead')
        
        html_text = ''
        for lead in leads:
            lead_id = self.__extract_component_attribute(lead, 'id')
            if lead_id == lead_id_needed:
                html_text = self.__extract_component_attribute(lead, 'text')
                break
                
        if html_text == '':
            return ''
        
        html_parser = TomitaOutputLeadParser()
        lead_terminals = html_parser.get_terminals(html_text)
        
        component_terminals = self.__extract_component_attribute(component_xml, 'FieldsInfo')
        component_terminals = component_terminals.split(';')[:-1]
        
        result = ''
        for term in component_terminals:
            result += lead_terminals[term] + ' '
        
        return result


######


from html.parser import HTMLParser

class TomitaOutputLeadParser(HTMLParser):        
    
    def __init__(self):
        super(TomitaOutputLeadParser, self).__init__()
        self.buffer = ''
        self.need_to_catch = False
        self.terminals = {}
        self.fictitious_tag = True
    
    def handle_starttag(self, tag, attrs):
        if tag == 'n' or tag == 'd' or tag == 't':
            if self.fictitious_tag:
                self.fictitious_tag = False
                return
            
            self.need_to_catch = True
            for attr in attrs:
                if 'n' in attr[0]:
                    self.buffer = attr[0]

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.need_to_catch:
            self.terminals[self.buffer] = data
            self.need_to_catch = False
            
    def get_terminals(self, html_text):
        self.feed(html_text)
        return self.terminals


#####


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





#####

parser = TomitaOutputParser('../tomita/output.xml')
components = parser.get_components()
for comp in components:
    print(comp)