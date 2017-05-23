from html.parser import HTMLParser
from enum import Enum

class ParseMode(Enum):
    DEFAULT = 1
    COLLECT_TEXT = 2
    COLLECT_TERMINALS = 3


class TomitaOutputLeadParser(HTMLParser):        
    
    def __init__(self):
        super(TomitaOutputLeadParser, self).__init__()
        # в качестве инициализации
        self._init()

        self._handle_starttag_functions = {
        ParseMode.COLLECT_TEXT: self._handle_starttag_collect_text_mode,
        ParseMode.COLLECT_TERMINALS: self._handle_starttag_collect_term_mode
        }

        self._handle_endtag_functions = {
        ParseMode.COLLECT_TEXT: self._handle_endtag_collect_text_mode,
        ParseMode.COLLECT_TERMINALS: self._handle_endtag_collect_term_mode
        }

        self._handle_data_functions = {
        ParseMode.COLLECT_TEXT: self._handle_data_collect_text_mode,
        ParseMode.COLLECT_TERMINALS: self._handle_data_collect_term_mode
        }
    
    def handle_starttag(self, tag, attrs):
        self._handle_starttag_functions[self.mode](tag, attrs)

    def handle_endtag(self, tag):
        self._handle_endtag_functions[self.mode](tag)

    def handle_data(self, data):
        self._handle_data_functions[self.mode](data)

            
    def get_terminals(self, html_text):
        self._init()
        self.mode = ParseMode.COLLECT_TERMINALS
        self.feed(html_text)
        return self.terminals

    def get_text(self, html_text):
        self._init()
        self.mode = ParseMode.COLLECT_TEXT
        self.feed(html_text)
        return self.text

    def _init(self):
        self.mode = ParseMode.DEFAULT
        self.buffer = ''
        self.need_to_catch = False
        self.terminals = {}
        self.fictitious_tag = True
        self.text = ''

    def _handle_starttag_collect_text_mode(self, tag, attrs):
        pass

    def _handle_endtag_collect_text_mode(self, tag):
        if tag == 'h':
            self.need_to_catch = True

    def _handle_data_collect_text_mode(self, data):
        if self.need_to_catch:
            self.text += data

    def _handle_starttag_collect_term_mode(self, tag, attrs):
        if tag == 'n' or tag == 'd' or tag == 't':
            if self.fictitious_tag:
                self.fictitious_tag = False
                return
            
            self.need_to_catch = True
            for attr in attrs:
                if 'n' in attr[0]:
                    self.buffer = attr[0]

    def _handle_endtag_collect_term_mode(self, tag):
        pass

    def _handle_data_collect_term_mode(self, data):
        if self.need_to_catch:
            self.terminals[self.buffer] = data
            self.need_to_catch = False
