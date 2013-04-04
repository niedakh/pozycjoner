pozycjoner: a python module for scraping position of public transport vehicles from different vendors
==========

Work in progress from Wroclaw, Poland where the public transport is so bad, people are actually interested in harvesting data to protect themselves from public transport's suckage.

Current TODO:
- check for some backend ideas
- *in progress* write unit tests 
- *in progress* write some API documentation
- *in progress* define nearest station, delay time and other possible data in the Position API (maybe change it to Status?)
- **done** extra data in backends, esp. time the data was received (what standard?) and attach extra data to results
- **done** define an API structure with generlized Position class, use standard classess for latlng & dat
- **done** implement Przewozy Regionalne sp.z.o.o.'s data source  - data source: kursowania.przewozyregionalne.pl
- **done** implement MPK Wroclaw's data source - data source: pasazer.mpk.wroc.pl


This software is under the Affero GPL v.3 licence. I will gladdly allow anyone to use it commercially with no cost, just e-mail me about it, perhaps ask me to grab a coffee together or chat on IRC (networking is a good payment).

If you are happy with my work, feel free to reward me ([Skinner says positive reinforcement works](http://en.wikipedia.org/wiki/Reinforcement#Positive_and_negative)) by a [PLN donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=5KCTBA8GMYR76&lc=PL&item_name=Piotr%20Szyma%c5%84ski&item_number=pozycjoner&currency_code=PLN&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted), [USD donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=5KCTBA8GMYR76&lc=PL&item_name=Piotr%20Szyma%c5%84ski&item_number=pozycjoner&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted) or an [EUR donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=5KCTBA8GMYR76&lc=PL&item_name=Piotr%20Szyma%c5%84ski&item_number=pozycjoner&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted) for a beer or a coke.


Example outputs:

Przewozy Regionalne
==========
**Available lines:**
<pre>

    ['66431', '33216', '2043', '129', '30134/5', '91444/5', '22031', '41214', '121', '1036', '19027', '66341', '32128', '70123', '77949', '7774
    8', '70122/3', '3335/4', '4023', '88353', '66239', '17', '128', '77746']
</pre>

**Positions of first three lines:**
<pre>

    [
       {
          'mode':'train',
          'provider':'pl.przewozyregionalne',
          'pos':{
             'lat':'51.637630000',
             'lng':'16.142913300'
          },
          'date':1365108829.0,
          'line':'66431'
       },
       {
          'mode':'train',
          'provider':'pl.przewozyregionalne',
          'pos':{
             'lat':'50.035695000',
             'lng':'19.974590000'
          },
          'date':1365108837.0,
          'line':'33216'
       },
       {
          'mode':'train',
          'provider':'pl.przewozyregionalne',
          'pos':{
             'lat':'50.002943300',
             'lng':'22.703246700'
          },
          'date':1365108838.0,
          'line':'2043'
       }
    ]
</pre>


MPK Wroclaw
==========
**Available lines:**
<pre>

    ['a', 'c', 'd', 'k', 'n', '100', '103', '105', '107', '109', '110', '113', '114', '115', '116', '118', '119', '120', '122', '125', '126',
    '127', '128', '129', '130', '131', '132', '133', '134', '136', '140', '141', '142', '144', '145 ', '146', '147', '149', '240', '241', '243',
    '245', '246', '247', '249', '250', '251', '253', '255', '257', '259', '403', '406', '409', '435', '1', '2', '3', '4', '5', '6', '7', '8', 
    '9', '0l', '0p', '10', '11', '14', '15', '17', '20', '23', '24', '31 plus', '32 plus', '33 plus', '305', '310', '319', '325', '331', '346',
     '602', '607', '609', '612']
</pre>

**MPK A**
<pre>

    [
       {
          'mode':'bus',
          'provider':'pl.wroc.mpk',
          'date':1365109363.0,
          'pos':{
             'lng':17.031440734863,
             'lat':51.102634429932
          },
          'line':'A'
       },
       {
          'mode':'bus',
          'provider':'pl.wroc.mpk',
          'date':1365109363.0,
          'pos':{
             'lng':16.978332519531,
             'lat':51.094039916992
          },
          'line':'A'
       },
       {
          'mode':'bus',
          'provider':'pl.wroc.mpk',
          'date':1365109363.0,
          'pos':{
             'lng':17.062620162964,
             'lat':51.132480621338
          },
          'line':'A'
       }
    ]
</pre>
