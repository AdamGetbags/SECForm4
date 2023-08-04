# -*- coding: utf-8 -*-
"""

SEC Form 4 Filing Scraper
@author: AdamGetbags

"""

# import modules
import requests
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup

singleRow = []
allRows = []

# create request header
headers = {'User-Agent': "email@address.com"}

# get all companies data
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# review response / keys
print(companyTickers.json().keys())

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']

# parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                     orient='index')

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(
                           str).str.zfill(10)

# review data
print(companyData[:1])

cik = companyData[0:1].cik_str[0]

# get company specific filing metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
    )

# review json 
print(filingMetadata.json().keys())
filingMetadata.json()['filings']
filingMetadata.json()['filings'].keys()
filingMetadata.json()['filings']['recent']
filingMetadata.json()['filings']['recent'].keys()

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(
             filingMetadata.json()['filings']['recent']
             )

# review columns
allForms.columns
allForms[['accessionNumber', 'reportDate', 'form']].head(50)

# form 4 metadata
allForms.iloc[0]

# reformat accession number
sampleAccessionNumber = allForms[:1]['accessionNumber'][0].replace('-','')
# document number
sampleDocumentNumber = allForms[:1]['primaryDocument'][0]

# get requests for form
formRequest = requests.get('https://www.sec.gov/Archives/edgar/data/' + 
                           str(directCik) + '/' +
                           sampleAccessionNumber + '/' + 
                           sampleDocumentNumber,
                           headers=headers)

soup = BeautifulSoup(formRequest.text, 'html.parser')

tableHTML = soup.find_all('table')[15]

# TODO - review table header data
headerInfo = tableHTML.find_all('thead')

# get all table row data
for data in tableHTML.find_all('tbody'):
    rows = data.find_all('tr')
    print(rows)
    
# for each row on form, make a list with cell values 
for row in rows:
    for i in range(0,len(row.find_all('td'))):
        singleRow.append(row.find_all('td')[i].text)
        print(row.find_all('td')[i].text)
    allRows.append(singleRow)
    singleRow = []

# # parse html tree
# tree = html.fromstring(formRequest.content)
# # dir(tree)

# # table elements
# allTables = tree.xpath('//table')