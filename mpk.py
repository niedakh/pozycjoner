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
from position import Position
from time import mktime
from positioner import Positionier

## @class MPKWroclawPositionier
#
#  A positioner module for the MPK Wroclaw sp. z.o.o. data source.
#  It uses data from http://pasazer.mpk.wroc.pl and provides information about
#  active lines at the moment, and position of each line or lines. 
#
#  Data available from MPK Wroclaw include:
#    - gps position of the line
#    - transport mode of the line i.e. bus/train/tram
#
##
class MPKWroclawPositionier(Positionier):
    """ TODO:description """
    
    def __init__(self):
        self.mpk_url = 'http://pasazer.mpk.wroc.pl/position.php'
        self.provider = 'MPKWroclaw'
        self.provider_id = 'pl.wroc.mpk'
        self.mpk_list_url = 'http://pasazer.mpk.wroc.pl/jak-jezdzimy/mapa-pozycji-pojazdow'
        self.dateparser = pdt.Calendar(pdt.Constants())
        
    ##
    # Get information about which MPK lines are available to
    # query position information, fetches all available without
    # filtering whether they are active at the time.
    #
    # @return list<string> containing ids (each id is a string) of lines
    #
    ##
        
    def getAvailableLines(self):
        session = requests.session()
        mpk_data_page = requests.get(self.mpk_list_url)
        if (mpk_data_page.status_code != 200):
            mpk_data_page.raise_for_status()
        
        mpk_data_tree = BeautifulSoup(mpk_data_page.text)
        
        # data of available lines is stored in the DOM tree in elements:
        # <li class="bus_line">A</li>
        # we are therefore searching for li.bus_lines text child element
        # we want it lowercased because that howe the MPK's javascript does this
        return [line.text.lower() for line in mpk_data_tree.find_all("li", "bus_line")]

    

    def getPosition(self, line_number):
        lines = []
        if isinstance(line_number, int):
            lines.append(str(line_number).lower())
        elif isinstance(line_number, str):
            lines.append(line_number.lower())
        elif isinstance(line_number,list):
            for i in line_number:
                lines.append(str(i).lower())
        
        # The POST request expects an urlencoded version of
        # busList[bus][]=line number, like an array in PHP, ex:
        # busList[bus][]=5&busList[bus][]=6 etc.
        #
        # Because the Request API expects a dictionary, we creeate a
        # dictionary with one key and put a lines array as the value
        # the Requests API should convert this to a list of key=value pairs
        payload = {'busList[bus][]': lines}
        session = requests.session()
        r = requests.post(self.mpk_url, data=payload)
                          
        if (r.status_code != 200):
            r.raise_for_status()    
        else:
            # http header has a specific date format, parser needed
            received = self.dateparser.parseDateText(r.headers['Date'])
            return [ self. parseDataItem(x,received) for x in r.json()]
    
    # MPK returns a json in the following format
    #
    #   @param string received
    #
    # {'x': 51.107200622559 /lat/, 'y': 17.033378601074 /lng/,
    #  'k': '2635053' /some internal id - dunno?/,
    #  'name': '4' /line number or id /,
    #  'type': 'tram' /might also be 'bus' or 'train'/}
    def parseDataItem(self, item, received):
        return Position(item['name'], self.provider_id, item['x'], item['y'], item['type'], mktime(received), {'k': item['k']})
        
    
  
if __name__ == "__main__":
    mpk = MPKWroclawPositionier()
    lines = mpk.getAvailableLines()
    print("Available lines:")
    print(lines)
    
    print("MPK 241:")
    print(mpk.getPosition(241))
    
    print("MPK A:")
    print(mpk.getPosition('A'))
    
    print("MPK all:")
    print(mpk.getAllPositions())