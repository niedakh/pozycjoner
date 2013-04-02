pozycjoner: a python module for scraping position of public transport vehicles from different vendors
==========

Work in progress from Wroclaw, Poland where the public transport is so bad, people are actually interested in harvesting data to protect themselves from public transport's suckage.

Current TODO:
- check for some backend ideas
- write some API documentation
- *in progress* define nearest station, delay time and other possible data in the Position API (maybe change it to Status?)
- **done** extra data in backends, esp. time the data was received (what standard?) and attach extra data to results
- **done** define an API structure with generlized Position class, use standard classess for latlng & dat
- **done** implement Przewozy Regionalne sp.z.o.o.'s data source  - data source: kursowania.przewozyregionalne.pl
- **done** implement MPK Wroclaw's data source - data source: pasazer.mpk.wroc.pl


This software is under the Affero GPL v.3 licence. I will gladdly allow anyone to use it commercially with no cost, just e-mail me about it, perhaps ask me to grab a coffee together or chat on IRC (networking is a good payment).

If you are happy with my work, feel free to reward me ([Skinner says positive reinforcement works](http://en.wikipedia.org/wiki/Reinforcement#Positive_and_negative)) by a [PLN donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=5KCTBA8GMYR76&lc=PL&item_name=Piotr%20Szyma%c5%84ski&item_number=pozycjoner&currency_code=PLN&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted), [USD donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=5KCTBA8GMYR76&lc=PL&item_name=Piotr%20Szyma%c5%84ski&item_number=pozycjoner&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted) or an [EUR donation](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=5KCTBA8GMYR76&lc=PL&item_name=Piotr%20Szyma%c5%84ski&item_number=pozycjoner&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted) for a beer or a coke.
