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


class PrzewozyRegionalnePositionierTest(PrzewozyRegionalnePositionier):
    def returnDataTree(self):
        test_file = open(os.path.dirname(__file__)+'\\pkppr.htm', encoding='utf-8')
        return test_file.read()
    

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.positioner = PrzewozyRegionalnePositionierTest()
        
    def testGetAvailableLines(self):
        expected = ['46931/0', '41034', '115', '30126/7', '70142/3', '60237', '60228', '40028', '51024/5',
                    '67937', '5027', '78125', '78327', '77522', '67939', '66234', '91225', '85430', '1033',
                    '2027', '12036/7', '76226', '77537', '4336/7', '623', '2441', '89727', '89142', '24', '97131/0',
                    '6623', '6121/0', '97028', '89728', '7530/1', '15201', '88645', '23439', '2038', '77938/9',
                    '87126', '88524', '3325/4', '120', '4228', '77738', '78445', '78137', '55116/7', '2031/0',
                    '5734/5', '55262/3', '60123/2', '76824/5', '7044', '44290', '64246', '30134/5', '57110/1',
                    '97129/8', '8726', '97145/4', '4015', '1028', '220152', '66730', '89125', '66123', '4332/3',
                    '42207/6', '22', '36122/3', '88142', '22141', '20347', '30324/5', '97029', '70525/4', '88932/3',
                    '7043', '17227', '60326', '87328', '6434', '60823', '6426', '1330/1', '32438', '1112', '1035',
                    '2040', '12038/9', '8724/5', '5037', '23145', '7124', '67225', '46939', '46937/6', '7024',
                    '46201', '51124', '44251', '44233', '51236', '20342', '78443', '4334/5', '7863124/5', '46217',
                    '21038/9', '64210']
        self.assertEqual(self.positioner.getAvailableLines, expected)

    
    
    
if __name__ == '__main__':
    unittest.main()