# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:56:51 2023

to change environment click the bottom right "completions:conda" 
and change to the relevant environment 

help about spyder https://docs.spyder-ide.org/3/editor.html

@author: roipa
"""

import streamlit as st
import pandas as pd
import json

file = open("company_tickers.json", "r")
data = json.load(file)
print(json.dumps(data, indent=4))

df = pd.DataFrame({
    "first_column": [1,2,3],
    "second_column": [4,5,6]})

st.write(df)

#cmd > streamlit run c:\source\python\spyder\hello.py