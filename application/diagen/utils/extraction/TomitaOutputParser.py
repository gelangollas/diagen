from xml.dom import minidom
from .TomitaOutputLeadParser import *
from .Component import *

class TomitaOutputParser:
    
    def __init__(self, path):
        self.xmldoc = minidom.parse(path)
        
    def get_components(self):
        components = []
        for comp in self.xmldoc.getElementsByTagName('Component'):
            components.append(self.__construct_component(comp))
        return components

    def get_sentences(self):
        leads = self.xmldoc.getElementsByTagName('Lead')
        sentences = []

        html_parser = TomitaOutputLeadParser()
        for lead in leads:
            html_text = self.__extract_component_attribute(lead, 'text')
            sentences.append(html_parser.get_text(html_text))

        return sentences


    
    def __construct_component(self, component_xml):
        to_construct = ExtractedComponent()
        to_construct.type = self.__extract_component_element(component_xml, 'Type').lower()
        to_construct.name = self.__extract_component_element(component_xml, 'Name')
        to_construct.descr = self.__extract_component_element(component_xml, 'Description').lower()
        to_construct.pointer = self._bool(self.__extract_component_element(component_xml, 'Pointer'))
        to_construct.sentence_id = int(self.__extract_component_attribute(component_xml, 'LeadID'))
        to_construct.sentence_number = int(self.__extract_component_attribute(component_xml, 'sn'))
        to_construct.first_word = int(self.__extract_component_attribute(component_xml, 'fw'))
        to_construct.last_word = int(self.__extract_component_attribute(component_xml, 'lw'))
        to_construct.text_pos = int(self.__extract_component_attribute(component_xml, 'pos'))
        to_construct.length = int(self.__extract_component_attribute(component_xml, 'len'))
        to_construct.text = self.__extract_component_text(component_xml)
        return to_construct

    def _bool(self, string):
        if string != '0':
            return True
        return False

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
