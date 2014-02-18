import sublime, sublime_plugin
import urllib.request as request
from urllib.error import HTTPError as http_error
import contextlib
import re

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

    def parse_elhuyar_translation(self, source):
        # The translation is inside the tag <dt class="ordaina" lang="es"><strong></strong></dt>
        # We parse the HTML file to find that tag

        data_start_pos = [m.start() + len(DATA_START_TAG) for m in re.finditer(DATA_START_TAG, source)]
        data_end_pos = [m.start() for m in re.finditer(DATA_END_TAG, source)]

        if len(data_start_pos) == len(data_end_pos):
            options = [source[data_start_pos[i]:data_end_pos[i]].strip() for i in range(len(data_start_pos))]
            
        print(options)
        translation = self.select_parsed_words(options)
        return translation

    def get_elhuyar_request(self, word):
        # We create the url string to use the Elhuyar api
        language = self.view.settings().get(LANGUAGE_SETTING_NAME)
        url_str = 'http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?sarrera=' + word + '&mota=sarrera&term_hizkuntza=' + language + '&aplik_hizkuntza='
        headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}

        # We open and save to a string the url
        try:
            with contextlib.closing(request.urlopen(url_str, timeout=3)) as file_handle:
                file_handle_str = file_handle.read().decode("latin-1")
                return self.parse_elhuyar_translation(file_handle_str)
        except http_error as e:
            sublime.error_message("Server error. Does that word exist? Did you choose the correct source language?")
            return None

    def on_chosen(self, index):
        return index

    def select_parsed_words(self, options):
        selection = sublime.active_window().show_quick_panel(options, self.on_chosen)
        return options[selection]

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

