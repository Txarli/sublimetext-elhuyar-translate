import sublime, sublime_plugin
import urllib.request as request
import contextlib

LANGUAGE_SETTING_NAME = 'Language'
BASQUE_URL_NAME = 'E'
SPANISH_URL_NAME = 'G'

def change_language(view, language):
    view_settings = view.settings()
    view_settings.set(LANGUAGE_SETTING_NAME, language)

class SublimeElhuyarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        word = []
        for sel in sels:
            if not sel.empty():
                word = self.view.substr(sel)
                position = sel.end()

        string_to_write = ' --> ' + self.getElhuyarTranslation(word)
        self.view.insert(edit, position, string_to_write)

    def getElhuyarTranslation(self, word):
        # We create the url string to use the Elhuyar api
        language = self.view.settings().get(LANGUAGE_SETTING_NAME)
        url_str = 'http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?sarrera=' + word + '&mota=sarrera&term_hizkuntza=' + language + '&aplik_hizkuntza='

        # We open and save to a string the url
        with contextlib.closing(request.urlopen(url_str)) as file_handle:
            file_handle_str = file_handle.read().decode("latin-1")
        print (type(file_handle_str))

        # The translation is inside the tag <dt class="ordaina" lang="es"><strong></strong></dt>
        # We parse the HTML file to find that tag
        data_start_tag = '<dt class="ordaina" lang="es"><strong>'
        data_end_tag = '</strong></dt>'
        data_start_pos = file_handle_str.index(data_start_tag) + len(data_start_tag)
        data_end_pos = file_handle_str.index(data_end_tag)
        translation = file_handle_str[data_start_pos:data_end_pos].strip()
        return translation

class ChangeToBasqueCommand(sublime_plugin.TextCommand):
    """docstring for SourceBasqueCommand"""
    def run(self, edit):
        change_language(self.view, BASQUE_URL_NAME)
        print ('Source language changed to Basque')

class ChangeToSpanishCommand(sublime_plugin.TextCommand):
    """docstring for SourceBasqueCommand"""
    def run(self, edit):
        change_language(self.view, SPANISH_URL_NAME)
        print ('Source language changed to Spanish')

