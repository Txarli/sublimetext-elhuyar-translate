import sublime, sublime_plugin
import urllib.request
from html.parser import HTMLParser

class SublimeElhuyarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        word = []
        for sel in sels:
            if not sel.empty():
                word = self.view.substr(sel)
                position = sel.end()

        string_to_write = " --> " + word
        print(type(string_to_write))
        self.view.insert(edit, position, string_to_write)

    def getElhuyarPage(self, word, translation):
        # We create the url string to use the Elhuyar api
        url_str = 'http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?sarrera=hola&mota=sarrera&term_hizkuntza=G&aplik_hizkuntza='

        # We open and save to a string the url
        file_handle = urllib.request.urlopen(url_str)
        file_handle_str = fileHandle.read().decode("utf-8")

        # The translation is inside the tag <dt class="ordaina" lang="es"><strong></strong></dt>
        # We parse the HTML file to find that tag
        

