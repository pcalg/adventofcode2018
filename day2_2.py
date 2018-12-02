# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 11:37:29 2018

@author: Pieter
"""

import pandas as pd
from pathlib import Path
import os

from timeit import default_timer as timer



file_location = Path(os.getcwd())

df_words = pd.read_csv(file_location / 'inputday2.txt', header=None, names=['words'])

word_lst = df_words['words'].tolist()


start = timer()

def first_equal(words):
    words_seen = set()
    
    for word in words:
        if word in words_seen:
            return True, word
        words_seen.add(word)

    return False, ""

def remove_idx_list(idx, words):
    result = list()
    
    for word in words:
        result.append(word[0: idx] + word[idx+1:])
    return result
        
        
def find_first_equal(words):   
    max_len = len(words[0])
    
    for idx in range(0, max_len):    
        tmp_words = remove_idx_list(idx, words)
        
        res, word = first_equal(tmp_words)
        
        if res:
            return word
    return ""
    

word = find_first_equal(word_lst)

print(word)

end = timer()

print(end - start)