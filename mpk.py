import requests
from bs4 import BeautifulSoup

class MPKWroclawPositionier:
    """ TODO:description """
    
    def __init__(self):
        self.mpk_url = 'http://pasazer.mpk.wroc.pl/bus_gps/position'
        
        self.provider = 'MPKWroclaw'
        self.mpk_list_url = 'http://pasazer.mpk.wroc.pl/jak-jezdzimy/mapa-pozycji-pojazdow'
        
        
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
    
  
if __name__ == "__main__":
    mpk = MPKWroclawPositionier()
    print("Available lines:")
    print(mpk.getAvailableLines())
