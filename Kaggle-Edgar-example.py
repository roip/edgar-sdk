# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 15:14:14 2023

@author: roipa
using the following example from Kaggle
https://www.kaggle.com/code/svendaj/extracting-data-from-sec-edgar-restful-apis
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json
import requests

with open("company_tickers.json", "r") as f:
    CIK_dict = json.load(f)
    
CIK_dict.keys()
CIK_dict["columns"]
print("Number of company records:", len(CIK_dict["data"]))
CIK_dict["data"][:5]    # first 5 records
CIK_df = pd.DataFrame(CIK_dict["data"], columns=CIK_dict["columns"])
CIK_df
# finding company row with given ticker
ticker = "AAPL"
CIK_df[CIK_df["ticker"] == ticker]
CIK = CIK_df[CIK_df["ticker"] == ticker].cik_str.values[0]
CIK
# finding companies containing substring in company name
substring = "oil"
CIK_df[CIK_df["title"].str.contains(substring, case=False)]

#company submissions 
url = f"https://data.sec.gov/submissions/CIK{str(CIK).zfill(10)}.json"
url

headers = {
    "User-Agent": "admin@roipaul.com",  # Replace with your user agent
    "Accept": "application/json"
  }
#this might not work behind a vpn
response = requests.get(url, headers=headers)

company_filings = response.json()
company_filings.keys()
company_filings["addresses"]
company_filings["filings"]["recent"].keys()
company_filings["filings"]["recent"]
company_filings_df = pd.DataFrame(company_filings["filings"]["recent"])
company_filings_df
company_filings_df[company_filings_df.form == "10-K"]

#Accessing specific filing document
access_number = company_filings_df[company_filings_df.form == "10-K"].accessionNumber.values[0].replace("-", "")
file_name = company_filings_df[company_filings_df.form == "10-K"].primaryDocument.values[0]

url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{access_number}/{file_name}"
url
# dowloading and saving requested document to working directory
req_content = requests.get(url, headers=headers).content.decode("utf-8")

with open(file_name, "w") as f:
    f.write(req_content)
    
    
#XBRL Company Concepts 

url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(CIK).zfill(10)}.json"
url

company_facts = requests.get(url, headers=headers).json()

# get the current assets values as reported over time and make it pandas DataFrame
curr_assets_df = pd.DataFrame(company_facts["facts"]["us-gaap"]["AssetsCurrent"]["units"]["USD"])
curr_assets_df

# get just values reported in valid frame and plot them
curr_assets_df[curr_assets_df.frame.notna()]

import plotly.express as px
pd.options.plotting.backend = "plotly" 

#this doesnt work for some reason, probably need to install something
curr_assets_df.plot(x="end", y="val", 
                    title=f"{company_filings['name']}, {ticker}: Current Assets",
                   labels= {
                       "val": "Value ($)",
                       "end": "Quarter End"
                   })

# let's retrieve current assets for comparision with company facts API
url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{str(CIK).zfill(10)}/us-gaap/AssetsCurrent.json"
url

curr_assets_dict = requests.get(url, headers=headers).json()
curr_assets_dict.keys()
curr_assets_dict["tag"]
curr_assets_dict["units"]["USD"][:5]
# this should be resulting in same DataFrame as retrieved through companyfacts API and selected through taxonomy us-gaap, AssetsCurrent concept/tag and units USD
curr_assets_df = pd.DataFrame(curr_assets_dict["units"]["USD"])
curr_assets_df

#Getting one fact from requested period/frame 
#cell: https://www.kaggle.com/code/svendaj/extracting-data-from-sec-edgar-restful-apis?scriptVersionId=105603576&cellId=37
# Let's retrieve all data about current assets in Q4 of 2021
fact = "AssetsCurrent"
year = 2021
quarter = "Q1I"

url = f"https://data.sec.gov/api/xbrl/frames/us-gaap/{fact}/USD/CY{year}{quarter}.json"
url
curr_assets_dict = requests.get(url, headers=headers).json()
curr_assets_dict.keys()

# let's convert all data of requested period to pandas dataframe
curr_assets_df = pd.DataFrame(curr_assets_dict["data"])
curr_assets_df.sort_values("val", ascending=False)
