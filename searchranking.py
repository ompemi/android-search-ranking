#!/usr/bin/python

"""
Retrieves the ranking position of an android application in Google Play, for the
given keywords and countries

@author: Omar Pera <https://github.com/ompemi>
"""

import sys
import optparse

import requests
from lxml import html

def get_search_ranking(package, keyword, country, ranking_limit):
    """
    Web scrapper for Google Play search results, that returns the ranking position
     for a given application package name.

    Returns:
        An integer with the ranking position, or 0 if not found
    """
    for url, offset in market_search_url_pager(keyword, country, ranking_limit):
        r = requests.get(url)
        tree = html.fromstring(r.content)

        apps = tree.cssselect('li[data-docid]')
        for position, app in enumerate(apps):
            if app.get('data-docid').strip() == package:
                return offset + position + 1

    return 0

def market_search_url_pager(keyword, country, ranking_limit, num_items_per_page=24):
    """Generator that returns the Google Play url, for each results page"""
    url = 'https://play.google.com/store/search?q=%s&c=apps&sort=1&num=%d&hl=%s' % \
        (keyword, num_items_per_page, country)
    offset = 0
    for num_pages in xrange((ranking_limit / num_items_per_page) + 1):
        url_page = url + "&start=%d" % offset
        yield url_page, offset
        offset += num_items_per_page

def main(package, countries, keywords, ranking_limit):
    print "Package: %s" % package
    for keyword in  keywords:
        print "Keyword: %s" % keyword
        for country in countries:
            ranking = get_search_ranking(package, keyword, country, ranking_limit)
            if ranking:
                print '\t#%d (%s)' % (ranking, country)
            else:
                print '\tNot found in top #%d (%s)' % (ranking_limit, country)


if __name__ == '__main__':
    desc = """Retrieve the ranking position for an android application in Google Play, based on search term(s)

    Example:
        $ python searchranking.py -p com.androidsx.smileys -k whatsapp,smileys -c en,es
            Package: com.androidsx.smileys
            Keyword: whatsapp
                #7 (en)
                #5 (es)
            Keyword: smileys
                #1 (en)
                #1 (es)
    """

    parser = optparse.OptionParser(version='%prog version 1.0', description=desc)
    parser.add_option('-c', '--countries', help='Google Play Countries to search for', dest='countries',
        default="es, en", metavar='<COUNTRY1>,<COUNTRY2>..')
    parser.add_option('-l', '--limit', help='Maximum ranking position to search for', dest='ranking_limit',
        default=50)
    parser.add_option('-k', '--keywords', help='Keywords to search for', dest='keywords',
        metavar='<KEYWORD1>,<KEYWORD2>..')
    parser.add_option('-p', '--package', help='Package name of the application', dest='package')
    (opts, args) = parser.parse_args()

    # Making sure all mandatory options appeared.
    mandatories = ['package', 'keywords']
    for m in mandatories:
        if not opts.__dict__[m]:
            print "Mandatory option is missing: %s\n" % m
            parser.print_help()
            sys.exit(-1)

    countries_input = map(lambda c: c.strip(), opts.countries.split(","))
    keywords_input = map(lambda k: k.strip(), opts.keywords.split(","))

    main(opts.package, countries_input, keywords_input, opts.ranking_limit)