# -*- coding cp1250 -*-
from collections import defaultdict
import requests
import re
from bs4 import BeautifulSoup

class Dict(object):
    
    def __init__(self,url="http://pl.bab.la/slownik/angielski-polski/"):
        self.Dict = defaultdict(int)
        self.url = url

    def seturl(self,url):
        self.url = url
        
    def _get_html_page(self,url):
        """Just to fetch url source into a string"""
        req = requests.get(url)
        return req

    def _chckifWord(self,obj):
        """"""
        return type(obj) == str
    
    def _chckifList(self,obj):
        """"""
        return type(obj) == list
    
    def addWord(self,obj):
        """obj: string/list/tuple."""
        if self._chckifWord(obj) and obj not in self.Dict:
            self.Dict[obj]
            
        elif self._chckifList(obj):
            for word in obj:
                self.Dict[word]

    def output(self):
        return self.translate(info=False,output=True)

    def _wrapper(self,word):
        """just to wrapp smthng"""
        url = self.url + word
        return self._get_html_page(url)

    def _searchDuplicates(self,File):
        existingTranslations = [word[:-1] for word in File.readlines() if word.isupper()]
        return existingTranslations

    def _write_data(self,data):
        try:
            with open('translation.txt','r+') as f:
                alreadyWritten = self._searchDuplicates(f)
                toWrite = ''
                for word, translation in self.Dict.iteritems():
                    if word.upper() not in alreadyWritten:
                        toWrite += translation.encode('cp1250','replace')
                f.write(toWrite)
                
        except IOError:
            f = open('translation.txt','w')
            return self._write_data(data)
    
    def __str__(self):
        finalTranslation = ''
        for word, translation in self.Dict.iteritems():
            finalTranslation += translation.encode('cp1250','replace')
        print finalTranslation
        return finalTranslation


    def translate(self,hits=5,info=True,output=False):
        """hits: int - how many translation of words we wanna get.
           info: bool - True/False, depends on if we wanna print a message (True) or return dict (False)"""
        for key in self.Dict:
            matches = hits
            if self.Dict[key] is 0:
                url = self._wrapper(key)
                print(url.url)
                soup = BeautifulSoup(url.content,"html.parser")
                general_data = soup.findAll('div',{'class':'result-block'})[0].children
                translated_block = '\n' + key.upper() + '\n' # Creating a title, considering uppercased word we r translating
                for element in general_data:
                    if matches > 0:
                        try:
                                word2translate = element.find('div',{'class':'span6 result-left'}).text
                                translation = element.find('div',{'class':'span6 result-right row-fluid'}).text
                                translated_block += ('\n' + word2translate + '\n'
                                                          + translation + '\n')
                        except TypeError:
                            matches += 1
                            pass
            
                    self.Dict[key] = translated_block
                    matches -= 1
        if output:
            try:
                self._write_data(translated_block)
            except:
                self._write_data('')
        if info == True:
            return self.__str__()
                
    
if __name__ == "__main__":
    d = Dict()
    d.addWord("got")
    d.addWord(['turkey',"kill"])
    d.translate(info=True,output=True)
