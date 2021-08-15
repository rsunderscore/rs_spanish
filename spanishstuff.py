# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:18:39 2020

@author: Rob 

+ 11/4/20 done - function to clean colons from participles that were stored with test verbs
+ 11/4/20 moved web stuff into own module
+ 1/23/21 fixed issue when there are multiple answers had to provide all
+    added function to remove a bad entry from the cache shelf
- bug: if the verb is close spanishdict site will auto-correct and this 
    program associates it with whatever was entered
    need to update in web.py module

"""
#import requests
import pandas as pd
#from bs4 import BeautifulSoup
import html5lib
import re, os, sys, shelve
from time import sleep
from random import  shuffle#choice,
from itertools import product
from datetime import time, datetime
from spanish import web

pd.set_option('display.max_columns',999)#don't show ellipses
CACHEPTH = "."#os.path.join(os.environ['pythonpath'], 'spanish')
CACHENM = 'spshelf'
#CACHE = os.path.join(CACHEPTH, CACHENM)
conjurl = r'https://www.spanishdict.com/conjugate/'
conjurl2 = r'https://conjugar-verbos.com/contraer/'#layout is much different
defurl = r'https://www.dictionary.com/browse/'
transurl = r'https://www.spanishdict.com/translate/amanecer'
irregurl = r'https://conjugar-verbos.com/lista-de-verbos-irregulares/{}/'#.format('a')
tenses = "subjunctive, imperative, continuous, perfect, perfect subjunctive".split(",")
moodlist = ['Indicative', 'Subjunctive', 'Imperative', 'Continuous (Progressive)', 'Perfect', 'Perfect Subjunctive']
columns = "nan present preterit im0perfect imperfect2 future".split()
bookorder =['present', 'imperfect', 'preterit', 'future', 'conditional', 'present subj', 'imperfect subj',
            'perfect indicative', 'past perfect indicative', "preterit perfect", "future perfect",
            "conditional perfect", "present perfect", "past perfect subjunctive",
            'imperative', 'past participle','present participle' ]
aliases={'present participle': 'gerund', 'conditional':'simple potential', 'past perfect indicative':'pluperfect indicative',
         "preterit perfect":'past anterior', 'future perfect':'future anterior',
         'present perfect': 'past subjunctive', 'past perfect subjunctive':'pluperfect subjunctive'}
subjs = ['yo', 'tu', 'el/ella/usted','nosotros', 'vostros', 'ustedes/ellas/ellos']
ends = ['er', 'ir', 'ar']
#cache verbs that will be used a lot (haber, ir, ser, estoy, sentir, hacer, etc...)
#note: some verbs only have singular and plural forms - no variation for yo, tu, etc...
#note: Present participle phrases and gerund phrases are easy to confuse because
# they both begin with an ing word. The difference is the function that they provide
# in a sentence. A present participle phrase will always act as an adjective while 
# a gerund phrase will always behave as a noun.
terms = {'gerund':'a form that is derived from a verb but that functions as a noun',
         'present participle':'eng: the form of a verb, ending in -ing'}


#%% programmatic conjucation for regular verbs
#read the conjugation tables from file - rules for all tenses moods
#esp_conj.ods and spanish stuff .html in documents folder 
# need to export these to a python friendly format
def conj(verb):
    if verb[-2:] == 'ar':
        pass#implement rules here
        {'ends1': ['o', 'as','a', 'amos','áis']}
    result = None
    return result

#%% getting conjugations from the web
def get_cache_words():
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        words = list(s) 
    return words
def get_cache_stats():
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        words = list(s)
        print("{} verbs are stored".format(len(words)))
        maxprint = 10 if len(words) > 9 else len(words)
        print(words[:maxprint])
        
        #need a way to check if every verb has the same keys
        #put them in a set and then diff the sets
        for x in words:
            print("{}".format(list(s[x].keys())))

def get_all_tenses():
    biglist = list()
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        for k in s.keys(): #workds
            for m in s[k].keys(): #moods
                biglist.extend(s[k][m].columns)
    return list(set(biglist))

def fix_colon_in_cache():
    #problem with participles
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        for k in s.keys(): #words
            for m in s[k].keys(): #moods
                if ':' in " ".join(s[k][m].columns):
                    #can't change in place - need to pull out and re-add
                    #s[k][m].columns = [x.replace(':','') for x in s[k][m].columns]
                    c = s[k]
                    c[m].columns = [x.replace(':','') for x in c[m].columns]
                    s[k] = c
                    print(k, m, c[m])
            
def rem_cache_entry(verb):
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        s.pop(verb)
    return s

def print_cache_entry(verb):
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        entry = s[verb]
    print_entry(entry)
    return None

def print_entry(conjdict):
        
    for x in conjdict.keys():
        print(f"***************{x}****************")
        print(conjdict[x])
    return None

def get_conj(verb):
    conj = get_conj_from_shelf(verb)
    if not conj:
        print('not found in local cache')
        res = input("fetch from web(y/n)? ")
        if res == 'y':
            print("fetching and caching")
            conj = web.get_conj_from_web(verb)
    return conj

def get_conj_from_shelf(verb):
    
    with shelve.open(os.path.join(CACHEPTH, CACHENM)) as s:
        conj=s.get(verb)
    
    return conj

#check for a local conjugation

def print_conjdict(html):
    conjdict = web.get_tables_from_html(html)
    for x in conjdict.keys():
        print("*"*10, f"{x}", "*"*10, sep='\t\t')
        print(conjdict[x])
    return conjdict

#ñ
#res[6]
##### MAIN #####
def main():
    html=web.html_from_file()
    assert len(html) > 0
    conjdict=web.get_tables_from_html(html)
    print(conjdict.keys())
    s=shelve.open(os.path.join(CACHEPTH, CACHENM))
    s['ser'] = conjdict
    s.close()
    
    s=shelve.open(os.path.join(CACHEPTH, CACHENM))
    print(list(s))

    
#%% testing   
def look_for_groups(d1):
    rx = re.compile(r'(.{0,100}subjunctive.{0,20})',re.I)
    mo = rx.search(str(d1))
    mo.groups()

#extra line
#%% read files
def read_config():
    from configparser import ConfigParser
    c = ConfigParser(strict=False)
    c.read('words.conf', encoding ='utf8')#should be utf8
    #has problems with certain spanish characters?
    sorted(c['DEFAULT'].keys())
    for x in c['DEFAULT'].keys(): #everythin is a string 
        v = c['DEFAULT'][x]
        try:
            v = float(v) if "." in v else int(v)
        except Exception as e:
            print(e)
            from dateutil.parser import parse, ParserError
            try:
                v=parse(v)
            except ParserError as e:
                print(e.with_traceback())
                print(dir(e))
        print(f"{x} has value {v} of type {type(v)}")

def read_vocab():
    with open('spanish stuff.html', 'r') as f:
        lines = f.read()
        
    ss = web.BeautifulSoup(lines, features='lxml')
    print(ss.prettify()[:500])
    altcodes = pd.read_html(lines)[0] # first table should be alt codes
    
    #[ (s.findPreviousSibling('h1').text, s.text) for s in ss.findAll('p')]
    def get_words(ss):
        for s in ss.findAll('p'):
            if len(s.text) < 2: continue
            try:
                t=s.findPreviousSibling('h2').text
                print(s.text, t)
            except AttributeError:
                print(s.text, None)
                
    def get_category(s):
        t=s.findPreviousSibling('h2')
        ttext = t.text if t else None
        return ttext
    allwords = pd.DataFrame([ (get_category(s), s.text) for s in ss.findAll('p') if len(s.text) >1],
                 columns=['Category','Text'])
    allwords2 = allwords[pd.notnull(allwords['Category'])]
    
    
    #split the words and meanings into a df and join back with the orig
    #out = allwords['Text'].apply(lambda x: pd.Series(x.split("=")) )#, index=['key', 'val']
    out = allwords2['Text'].str.split('=', expand=True)
    out.columns=['Q','A']
    allwords3 = allwords2.join(out)
    #if there are multiple options for response split them into an array
    allwords3['A'] = allwords3['A'].str.replace('[\n\t]',' ').str.strip()
    allwords3['Q'] = allwords3['Q'].str.replace('[\n\t]',' ').str.strip()
    #'/' is sometimes used to split other things not just diff answers
    # need to standardize the separator
    allwords3[allwords3['A'].str.contains('/',na=False)]
    
    return allwords3, altcodes

def endless_vocab():
    
    while True:
        aw2 = aw[aw['Category'].str.contains('words',False)].sample(1)
        w = aw2.iloc[0]
        print("\n", w['Q'], end="")
        r = input("what's the answer -- ")
        if len(r)<1:
            break
        if re.match(r'quit',r, re.I):
            print('matched quit string')
            break
        if re.search( r, w['A'], re.I) != None:
            print("CORRECT", w['A'])
        else: 
            print("we were looking for -- ", w['A'])
        
        
def test_read_vocab():
    aw, ac = read_vocab()
    aw.Category.value_counts()
    aw[aw['Category'].str.contains('keybo',False, regex=True,)]
    aw2 = aw[aw['Category'].str.contains('words',False)].sample(10)
    for w in aw2.itertuples():
        #print(w.Q)
        w = w._asdict()#underscore method to index by name
        print("\n", w['Q'], end="")
        r = input("what's the answer -- ")
        if len(r)<1:
            break
        if re.match(r'quit',r, re.I):
            print('matched quit string')
            break
        if re.search( r, w['A'], re.I) != None:
            print("CORRECT", w['A'])
        else: 
            print("we were looking for -- ", w['A'])
    
def read_odf():
    #engine = odf requires odfpy
    sheets = pd.read_excel("esp_conj.ods", engine="odf", skiprows=1)#pd.read_excel("the_document.ods", engine="odf")


    
#need a function that reads these rules and applies them
#type(sheets)
#%% game stuff
#have a leaderboard with name and date?
#TODO: need a way of hiding the anwer after the next question
def test_conjgame():
    #next verbs to get: traer,  llevar, llegar, alimentar, tomar, comer, poder
    get_cache_stats()
    get_cache_words()
    c = conjgame()
    c.conjdict.keys()
    c.valid_moods
    c.q_tenses
    c.play_game()
    c.verb = 'estar'
    c.play_game()
    c.verb='ir'
    c.play_game()
    c.verb='haber'
    c.play_game()
    c.verb='ser'
    
class conjgame():
    """moved key functions into class - need to test
    """
    
    def __init__(self, verb='ser'):
        self.score=0
        self._verb=verb
        self.questions=10
        self.valid_moods=['Indicative', 'Subjunctive', 'Imperative', 'Continuous (Progressive)', 'Perfect', 'Perfect Subjunctive', 'participles']
        self.q_moods = ['Indicative']
        #['Present', 'Future', 'Preterite', 'Past', 'Affirmative', 'Conditional', 'Imperfect 2', 'Imperfect', 'Negative']
        self.q_tenses = ['Present', 'Preterite', 'Future','Past','Conditional','Imperfect']
        self.conjdict = dict()
        self.spain = False
        self.irr = False #allow irregular verbs to be selected     
        self.load_conjdict(self._verb) #
        self.testlist=pd.DataFrame()
    
    @property
    def verb(self):
        #print('getting verb')
        return self._verb
    
    @verb.setter
    def verb(self, verb):
        print(f'setting verb to {verb}')
        self._verb=verb
        self.load_conjdict(self._verb)
        
    def load_conjdict(self, verb):
        print(f"loading conjdict for {verb}")
        self.conjdict = get_conj(self.verb)
        if len(self.conjdict) <1:
            print("failed to load conjdict")
        
    def gen_testlist(self):
        
        #[word for sentence in text for word in sentence]
        #[list(c.conjdict[k].columns) for k in c.conjdict.keys()]
        #[w for i in _ for w in i]'
        #TODO: fix - there ares still colos on some of them e.g. Present: Past:
        #alltenses={i for k in self.conjdict.keys() for i in self.conjdict[k].columns}
        tenselist = self.q_tenses
        print("generating testlist")
        #moods = list(self.conjdict.keys())
        full_list = pd.DataFrame()
        for x in self.q_moods:
            #print(x)
            cur =self.conjdict[x]
            ### fails here when run from cmdline - works elsewhere
            # error is that DataFrame has no attribute '_data'
            print(f"x is {x} {self.conjdict.keys()}")
            print(f"cur is length {len(cur)}")
            res=pd.DataFrame(product(cur.index, cur.columns), columns=['subj','tense'])
            res['mood']=x
            full_list=full_list.append(res)
        full_list = full_list[full_list['tense'].apply(lambda x: x in tenselist)]
        #print(full_list)
    
        if self.spain == False:
            full_list = full_list[full_list['subj']!='vosotros']
            #full_list['subj'].value_counts()
        
        #handle case when_full list is shorter than question
        #reindex the full_list when padding out
        while(len(full_list) < self.questions):
            full_list=full_list.append(full_list)
        full_list.index = range(len(full_list))
        #full_list=full_list.reindex(range(len(full_list)))#error duplicate axis
        self.testlist = full_list.sample(self.questions)
        self.testlist['answer']=self.testlist.apply(self.get_ans,1)

    def get_ans(self, row):
        (subj,tense,mood) = row['subj'], row['tense'], row['mood']
        #print(subj,tense,mood, c.conjdict[mood][tense][subj])
        return self.conjdict[mood][tense][subj]
        
    def play_game(self):
        #use a fixed list of words or generate with yield(endless mode)?

        if len(self.testlist) < self.questions:
            self.gen_testlist()
        score = 0
        rounds=0
        print(f"verb is {self.verb}")
        #modified to handle cases when answer is multiple (ha,hay)
        while(len(self.testlist) > 0):
            curq = self.testlist.sample(1).iloc[0]
            anslist = curq['answer'].split(',')
            print(f"¿{curq['subj']} ________ ({curq['tense']} {curq['mood']})?")
            res=input("¿? ")
            rounds+=1
            if res in anslist:# curq['answer']:
                score+=1
                if len(anslist) > 1:
                    anslist.remove(res)
                    print(f"other answers {' or '.join(anslist)}")
                self.testlist = self.testlist.drop(curq.name)
            elif res == '':
                rounds-=1
                break
            else:
                #show answer for 5 seconds then erase and continue
                sys.stdout.write(f"{curq['subj']} {curq['answer']} ")
                sys.stdout.flush()
                for i in range(5,0,-1):
                    sys.stdout.write(str(i))
                    sleep(1)
                    sys.stdout.write("\b \b")
                #input()
                sys.stdout.write("\r"+" "*80+ "\r\r")#use len(answer) instead?
                sys.stdout.flush()
                print()#go to next line
        #score will always be 10 unless rules change or quit early
        if rounds > 0:
            print(f"Well done! {score} 10 correct answers {rounds} rounds for a score of {conjgame.score_method_2(score,rounds, self.questions)}")#max1000 


    def do_question(self, verb):
        conjdict = get_conj(verb)
        testlist=  list()
        for x in subjs:
            testlist.extend(x.split("/"))
        shuffle(testlist) # do a random order
        
        subj = testlist.pop()
        
        res = input("¿{} ________ ?".format( subj))#right-alt = altgr(intl) + / = ¿ ¡
        if res== 'test':
            print("Correct (+1)")
            self.score+=1
        else:
            print("xxxxx")
            testlist.append(subj)
            shuffle(testlist)
        print("test")
        
    @classmethod            
    def score_method_1(clss, score,rounds):
        return 1000*score/rounds
    
    @staticmethod   
    def score_method_2( score,rounds, max_questions):
        #max score is 10000 for 10 of 10 questions in 10 rounds
        #x2 +mx = y
        #function that yields max at 10 rounds then decreases
        #[(x,20*x-x**2) for x in range(20)] peak of 100 at round 10
        #[(x,.2*x-(x**2)/100) for x in range(20)] peak of 1 at round 10
        #need to be able to change based on c.questions
        #q = 10
        #(2*q*x-x**2)/100 #inverted parabola with peak at 10 and intercept 0,0 and 2q,0
        
        def mymult(q,r):
            from math import log10, log, e
            if r > q:
                return (2*q*r-r**2)/q**2
            else:#if rounds > max_questions - don't decrease as much - approach but never hit 0
                return (2*q*r-r**2)/q**2
        return mymult(max_questions,rounds) * score *1000
        
#%% CLI formatting - works until the cell exits

def clistuff():
    time.now()
    for i in range(10,1,-1):
        sys.stdout.write(datetime.now().time().strftime('%X'))
        sys.stdout.flush()
        sleep(.5)
        sys.stdout.write('\r')
        sys.stdout.flush()

def countdown(secs=10):
    try:
        for i in range(secs,1,-1):
            sys.stdout.write(str(i))
            sys.stdout.flush()
            sleep(1)
            #\b is backspace but doesn't erase
            sys.stdout.write('\r     \r\r')#erase and go to beginning
            sys.stdout.flush()
    except KeyboardInterrupt as e:
        print(e)
        
