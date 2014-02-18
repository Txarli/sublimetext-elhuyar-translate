import sublime, sublime_plugin
import urllib.request as request
from urllib.error import HTTPError as http_error
import contextlib

'''
    Parameter definitions
'''
# The name for the source language setting
LANGUAGE_SETTING_NAME = 'Language'

# The letters that should appear in the Elhuyar url for the source language
BASQUE_URL_NAME = 'E'
SPANISH_URL_NAME = 'G'

# Tags the translation is between of
DATA_START_TAG = '<dt class="ordaina" lang="es"><strong>'
DATA_END_TAG = '</strong></dt>'

'''
    Global functions
'''
def change_language(view, language):
    view_settings = view.settings()
    view_settings.set(LANGUAGE_SETTING_NAME, language)

'''
    Plugin commands
'''
class SublimeElhuyarCommand(sublime_plugin.TextCommand):
    '''Command that performs the request to the Elhuyar dictionary'''
    def run(self, edit):
        sels = self.view.sel()
        word = []
        for sel in sels:
            if not sel.empty():
                word = self.view.substr(sel)
                position = sel.end()

        string_to_write = ' --> ' + self.get_elhuyar_request(word)
        self.view.insert(edit, position, string_to_write)

    def get_elhuyar_request(self, word):
        # We create the url string to use the Elhuyar api
        language = self.view.settings().get(LANGUAGE_SETTING_NAME)
        url_str = 'http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?sarrera=' + word + '&mota=sarrera&term_hizkuntza=' + language + '&aplik_hizkuntza='

        # We open and save to a string the url
        try:
            with contextlib.closing(request.urlopen(url_str)) as file_handle:
                file_handle_str = file_handle.read().decode("latin-1")
                return parse_elhuyar_translation(file_handle_str)
            print (type(file_handle_str))
        except http_error as e:
            sublime.error_message("Server error. Does that word exist?")
            return None

    def parse_elhuyar_translation(self, source):
        # The translation is inside the tag <dt class="ordaina" lang="es"><strong></strong></dt>
        # We parse the HTML file to find that tag
        data_start_pos = file_handle_str.index(DATA_START_TAG) + len(DATA_START_TAG)
        data_end_pos = file_handle_str.index(DATA_END_TAG)
        translation = file_handle_str[data_start_pos:data_end_pos].strip()
        return translation

class ChangeToBasqueCommand(sublime_plugin.TextCommand):
    """Command that change source language to Basque"""
    def run(self, edit):
        change_language(self.view, BASQUE_URL_NAME)
        print ('Source language changed to Basque')

class ChangeToSpanishCommand(sublime_plugin.TextCommand):
    """Command that change source language to Spanish"""
    def run(self, edit):
        change_language(self.view, SPANISH_URL_NAME)
        print ('Source language changed to Spanish')

