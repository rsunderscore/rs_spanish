# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:40:51 2020

@author: Rob

### 11/9/20: fixed - can't find cache unless run from package directory
### BUG: 
"""
import argparse

import spanishstuff as sp

def main():
    parser = argparse.ArgumentParser('run spanish game')
    parser.add_argument("--verb", type=str, default='estar', help='set verb for game'   )
    parser.add_argument("--cache", action='store_true', help="print cache information")
    parser.add_argument("-p", '--play', action='store_true', help="play the game")
    parser.add_argument("--cpth", nargs='?', help='path to cache file')
    args = parser.parse_args()
    
    print(f"cache location is {sp.CACHEPTH} {sp.CACHENM}")
    
    if args.play:
        print(f"play is {args.play}")
        print(args.verb)
        c = sp.conjgame(args.verb)
        #print(c.conjdict)
        #print('testlist',c.testlist, sep='\n')
        #c.gen_testlist()
        c.play_game()
    
    if args.cache:
        sp.get_cache_stats()
        
    if args.cpth:
        print(f"cpth is {args.cpth}")

      
    


if __name__ == "__main__": main()