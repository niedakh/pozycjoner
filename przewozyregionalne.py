# pozycjoner: a python module for scraping position of public
# transport vehicles from different vendors
# https://github.com/niedakh/pozycjoner/
#
# Copyright (C) 2013  Piotr Szymanski <niedakh@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#    
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup
import parsedatetime as pdt
from datetime import datetime
import os,sys
import re

class PrzewozyRegionalnePositionier:
    """ TODO:description """
    
    def __init__(self):
        self.pkppr_url = 'http://82.160.42.14/opoznienia/'
        self.provider = 'PrzewozyRegionalne'
        self.dateparser = pdt.Calendar(pdt.Constants())
        
    def returnDataTree(self):
        #session = requests.session()
        # pkppr_data_page = requests.get(self.mpk_list_url)
        
        test_file = open(os.path.dirname(__file__)+'\\testdata\\pkppr.htm', encoding='utf-8')
        
        #if (mpk_data_page.status_code != 200):
        #    pkppr.raise_for_status()
        return test_file.read()
    
    def parseDataItem(self, item):
        return {
            'linia' : item[0],
            'lat': item[1],
            'lng': item[2]
        }
        
    def getAvailableLines(self):
       
        pkppr_data_tree = BeautifulSoup(self.returnDataTree())
        
                
        # data of available lines is stored in the DOM tree in the table.opoznienia, ex:
        # <tr id="tabela-n1 or tabela-n2">
        # 
        #    <td><a href="GOOGLE_MAPS_URL_WITH_POSITIONS" target="_blank">TRAIN_ID</a></td>
        #    <td>Poznan Glowny (18:50) - Kepno (22:01)</td>
        #    <td class="mw">15 min.</td> - delay
        #    <td>Solec Wielkopolski            </td> - closest station
        #    <td>2013-03-31 19:57:05</td> - data recording time
        ##</tr>
        #
        # The GOOGLE_MAPS_URL_WITH_POSITIONS looks like this:
        # http://maps.google.pl/maps?q=77532+++++@52.096100000,17.327171700&amp;t=m&amp;dirflg=r&amp;z=12
        # we can clearly see it is a format of:
        # http://maps.google.pl/maps?q=TRAIN_ID+++++@LAT,LNG
        # so what we basically need to scrape are all table.opoznienia tr a 
                
        link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=([^\+]+)')
        
        lines = [ link_regexp.match(line_link['href']).groups()[0]
                     for line_link in pkppr_data_tree.find_all(href=link_regexp)]

        return lines 
    
    def getAvailablePositions(self):
       
        pkppr_data_tree = BeautifulSoup(self.returnDataTree())
        
        # see documentation in getAvailableLines()
        link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=([^\+]+).*@([0-9\.]+),([0-9\.]+)')
        
        positions = [ self.parseDataItem(link_regexp.match(line_link['href']).groups())
                     for line_link in pkppr_data_tree.find_all(href=link_regexp)]

        return positions
    
    def getPosition(self, line_number):
        pkppr_data_tree = BeautifulSoup(self.returnDataTree())
        
        # see documentation in getAvailableLines()
        line_number_string = str(line_number)
        if (type(line_number) == type([])):
            line_number_string = "|".join([str(x) for x in line_number])
        
        link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=('+line_number_string+')\++@([0-9\.]+),([0-9\.]+)')
        
        if (pkppr_data_tree.find_all(href=link_regexp) == []):
            return [] # TODO: throw an error here
        else:
            # TODO: fix with common position API
            if (type(line_number) == type([])):
                return [ self.parseDataItem(link_regexp.match(line_link['href']).groups())
                     for line_link in pkppr_data_tree.find_all(href=link_regexp)]
            else:
                return self.parseDataItem((link_regexp.match(pkppr_data_tree.find_all(href=link_regexp)[0]['href']).groups()))
        
    
    
  
if __name__ == "__main__":
    pkppr = PrzewozyRegionalnePositionier()

    print("Available lines:")
    print(pkppr.getAvailableLines())
    
    print("PR 91432/3:")
    print(pkppr.getPosition('91432/3'))
    
    print("PR 91432/3 & 1116:")
    print(pkppr.getPosition(['91432/3',1116]))
    
    print("Positions of all available lines:")
    print(pkppr.getAvailablePositions())
    