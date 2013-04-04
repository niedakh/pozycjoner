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
from position import Position
from time import mktime

## @class PrzewozyRegionalnePositionier
#  A positioner module for the Przewozy Regionalne sp. z.o.o. data source.
#  It uses data from http://kursowania.przewozyregionalne.pl and parses them
#  using BeautifulSoup & some regexp ninja magic to provide information about
#  active lines at the moment, and position of each line or lines. It also
#  gathers information about: timestamp of the gps position receiving.
#
#
#  Data available from Przewozy Regionalne include:
#    - gps position of the train
#    - datetime of recording the position
#    - nearest station
#    - scale of delay (none, 5m, 10m, 20m, more)
#    - nearest station
#    - line information (starting station - ending station)
##
 
class PrzewozyRegionalnePositionier:
    """ TODO:description """
    
    def __init__(self):
        self.data_url = 'http://82.160.42.14/opoznienia/'
        self.provider = 'Przewozy Regionalne sp. z.o.o.'
        self.provider_id = 'pl.przewozyregionalne'
        self.dateparser = pdt.Calendar(pdt.Constants())
        self.type = 'train'
        
    def returnDataTree(self):
        #test_file = open(os.path.dirname(__file__)+'\\testdata\\pkppr.htm', encoding='utf-8')
        #return test_file.read()
    
        session = requests.session()
        data_page = requests.get(self.data_url)
        
        if (data_page.status_code != 200):
            data_page.raise_for_status()
        else:
            return data_page.content
        
    ##
    # Parse a data item scrapped from PrzewozyRegionalne website.
    #
    # @param list item
    #   the parsed item with structure of:
    #   - item[0][0]: string line id
    #   - item[0][1]: float latitude
    #   - item[0][2]: float longitude
    #   - item[0][3]: string relation information (start - end)
    #   - item[0][4]: enum<string> delay information (enum: planowo, x min., ponad 30 min.)
    #   - item[0][5]: nearest train station (not sure if nearest or nearest en route)
    #   - item[0][6]: gps position recording time
    #           
    #
    # @return dict Position 
    #   dictionary containing information about the item[0][0] line with extra information
    #   available as: TODO...
    ##
    def parseDataItem(self, item):
        # print(item)
        if (item != []):
            return Position(item[0][0], self.provider_id, item[0][1], item[0][2], self.type, mktime(datetime.strptime(item[0][6], "%Y-%m-%d %H:%M:%S").timetuple()),
                        {
                            'raw': item                            
                        }
                        )
        return None


    ##
    # Get information about which Przewozy Regionalne trains are currently
    # on their way and are reporting their GPS positions
    #
    # @return list<string> containing ids (each id is a string) of lines
    #           which are currently active and reporting GPS positions
    #
    ##

    def getAvailableLines(self):
       
        data_tree = BeautifulSoup(self.returnDataTree())
        
                
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
                     for line_link in data_tree.find_all(href=link_regexp)]

        return lines 
    
    def getAvailablePositions(self):
       
        #data_tree = self.returnDataTree()
        data_tree = BeautifulSoup(self.returnDataTree())
        table = data_tree.find('table','opoznienia')
        items = table.contents.__repr__().split("<tr")
        
        # see documentation in getAvailableLines()
        link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=([^\+]+).*@([0-9\.]+),([0-9\.]+).*<td[^<]*>(.+)</td><td[^<]*>(.+)</td><td[^<]*>(.+)</td><td[^<]*>(.+)</td>',re.DOTALL | re.IGNORECASE)
        
        ret = [self.parseDataItem(link_regexp.findall(item)) for item in items[2:]]
        # items has an items[0] containing the <thead> before first <tr>
        # and items[1] the first <tr> containing the header of the table
        # therefore an empty table will result in [None,None] being returned
        return ret
        
        
    ##
    # Get the Position of a Przewozy Regionalne train or trains
    # that are currently on their way and are reporting their GPS positions
    #
    # @param line_number integer, string, list<integer> or list<string> containing
    #           a list of ids of trains
    #
    # @return list<Position> containing information about position etc. for the lines
    #           which ids were in line_number and are still active and reporting GPS
    #           postitions
    #
    # @sa Position, parseDataItem
    ##
    def getPosition(self, line_number):
        data_tree = BeautifulSoup(self.returnDataTree())
        table = data_tree.find('table','opoznienia')
        items = table.contents.__repr__().split("<tr")
        
        # see documentation in getAvailableLines()
        line_number_string = str(line_number)
        if (type(line_number) == type([])):
            # getting a line1|line2|line3 - an matching expression for alternative of line ids
            line_number_string = "|".join([str(x) for x in line_number])
    
        # see documentation in getAvailableLines()
        #link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=('+line_number_string+')\++@([0-9\.]+),([0-9\.]+)')
        link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=('+line_number_string+')\++.*@([0-9\.]+),([0-9\.]+).*<td[^<]*>(.+)</td><td[^<]*>(.+)</td><td[^<]*>(.+)</td><td[^<]*>(.+)</td>',re.DOTALL | re.IGNORECASE)
        
        ret = []
        for item in items:
            res = link_regexp.findall(item)
            if (res != []):
                item = self.parseDataItem(res)
                if (item != None):
                    ret.append(item)
        
        if (ret == []):
            return None
        
        return ret
    
  
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
    