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

class Position:
    
    """ TODO:description """
    
    def __init__(self, line_id, company_id, lat, lng, mode, received, extra_data):
            self.line = line_id
            self.provider = company_id
            self.pos = {
                'lat' : lat,
                'lng' : lng
            }
            self.mode = mode
            self.date = received 
            self.extra = ""

    def __repr__(self):
        return {
            'line': self.line,
            'provider': self.provider,
            'pos': self.pos,
            'mode': self.mode,
            'date': self.date,
            'extra': self.extra
        }.__repr__()