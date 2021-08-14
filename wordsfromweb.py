#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 23:31:28 2021

@author: rob
"""

import requests, re
import pandas as pd
from bs4 import BeautifulSoup


URLS = {'articles':r'http://bbc.com/mundo', 'scandal': r'http://judgeforyourselves.com/info'}

def myget(url):
    #get a page a do some rudimentary clean-up
    r = requests.get(url)
    assert r.status_code == 200 #throw assertion error if get failed
    h = r.content #bytes string
    s = BeautifulSoup(h)
    s = remscript(s)
    #verify all script tags deleted
    assert len(s.find_all('script')) == 0
    return s


def remscript(s):
    #remove all script tags
    for x in s.findAll('script'):
        x.decompose()
    return s # since the object is modified in-place
    #this return is not strictly necessary

def article_links(s):
    matches = s.find_all('a', href=re.compile(r'/mundo/noticias',re.I))
    return matches

def links_list(m):
    return [(x['href'], x.text) for x in m]

def article_links_full(s):
    return links_list(article_links(s))

def all_links(s):
    return  s.find_all('a', href=True)

def mundostuff(s):
    theurl = URLS['articles']
    s = myget(theurl)
    ll = links_list(article_links(s))
    ldf = pd.DataFrame(ll, columns=['url','text'])
    ldf['text'] = ldf['text'].str.strip()
    ldf['furl'] = ldf['url'].apply(lambda x: x if x[0] =='h' else (theurl+x).replace('mundo/mundo','mundo')   )
    link = ldf['furl'][0]
    
    s2 = myget(link)
    for t in s2.find_all('path'):
        t.decompose()
    s2
    #remove empty div tags???
    for d in s2.find_all('div'):
        if len(d.get_text(strip=True)) ==0:
            d.extract()
    #article text is always in the maint tag
    e = s2.find('main')
    for sec in e.find_all('section'):
        print(sec.find(re.compile('^h[1-6]$')).get_text(strip=True))
    e.get_text()[:300]
def _scratch(s):

    len(s.find_all('img'))
    s.find('head')
    matches = s.find_all('a', href=re.compile(r'/mundo/noticias',re.I))
    m2 = s.find_all('link')
    len(m2)
    len(matches)
    
    link = s.find('a')
    link.attrs['href']

def show_members(obj):
    return [x for x in dir(obj) if x[0] !='_']
