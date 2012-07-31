Android search ranking
======================

Retrieves the ranking position of an android application in Google Play, for the given keywords and countries.

Requeriments
------------

* lxml
* requests

Installation
--------

```bash
git clone git://github.com/ompemi/android-search-ranking.git
cd android-search-ranking
virtualenv ~/.virtualenvs/market
source ~/.virtualenvs/market/bin/activate
pip install -r requirements.txt 
```
Usage 
-------

```bash
python searchranking.py -p com.androidsx.smileys -k whatsapp,smileys -c en,es
    Package: com.androidsx.smileys
    Keyword: whatsapp
      #7 (en)
      #5 (es)
    Keyword: smileys
      #1 (en)
      #1 (es)
```
