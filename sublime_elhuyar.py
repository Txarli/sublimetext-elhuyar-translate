import sublime, sublime_plugin
import urllib.request
from xml import etree

class SublimeElhuyarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        word = []
        for sel in sels:
            if not sel.empty():
                word = self.view.substr(sel)
                position = sel.end()

        #string_to_write = ' --> ' + self.getElhuyarTranslation(word)
        self.getElhuyarTranslation(word)
        #self.view.insert(edit, position, string_to_write)

    def getElhuyarTranslation(self, word):
        # We create the url string to use the Elhuyar api
        url_str = 'http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?sarrera=' + word + '&mota=sarrera&term_hizkuntza=G&aplik_hizkuntza='

        # We open and save to a string the url
        file_handle = urllib.request.urlopen(url_str)
        file_handle_str = file_handle.read().decode("latin-1")
        print (type(file_handle_str))

        # The translation is inside the tag <dt class="ordaina" lang="es"><strong></strong></dt>
        # We parse the HTML file to find that tag
        html = 1
        target = None
        encoding = 'utf-8'
        parser = etree.XMLParser(recover=True)
        parser.entity["nbsp"] = chr(160)
        parser.feed(file_handle_str)
        parser.close()
        tree = etree.fromstring(file_handle_str, parser=parser)
        dt = tree.find("dt/strong")
        print(dt.text())
        return dt.text()