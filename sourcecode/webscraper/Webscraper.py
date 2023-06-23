import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from webscraper.get_short_text import getShortText
import codecs


# --------------------------------- VARIABLES -------------------------------- #
#offical_languages = {
#    'English': 'en',
#    'German': 'de',
#    'Spanish': 'es',
#    'Italian': 'it',
#    'Gaelic': 'ga',
#    'French': 'fr'
#}

offical_languages_dataframe = pd.read_excel(r'./sourcecode/webscraper/Abbreviations.xlsx')
offical_languages = dict(zip(offical_languages_dataframe['Language'], offical_languages_dataframe['Version 1']))


# --------------------------------- SCRAPING --------------------------------- #
def get_website_text(websiteUrl, template):

    if template == "short":
        return getShortText(websiteUrl)
    #elif template == "middle":
    #    return getMiddleText(websiteUrl)
    #elif template == "long":
    #    return getLongText(websiteUrl)

    #page = requests.get(websiteUrl)
    #soup = BeautifulSoup(page.content, "html.parser")
    
    #results = soup.find(id="main-content")
    #list_elements = results.find_all("li", class_="ecl-timeline__item")

    #titles = []

    #for list_element in list_elements:
    #    title_element = list_element.find("div", class_="ecl-timeline__title")
        
    #    content_element = list_element.find("div", class_="ecl-timeline__content")
    #    paragraph_element = content_element.find("p")
        
        #print(title_element.text.strip())
        #print(paragraph_element.text.strip())

    #    titles.append(title_element.text.strip())

    #return titles


# ------------------------------- START METHOD ------------------------------- #
def start_scraping(filename="webscraper"):
    languageList = []
    sentenceList = []
    languageAbbreviationList = []
    combinationDictionary = {}

    f = codecs.open(os.path.abspath(os.curdir) + '/sourcecode/files/' + filename + ".txt", "w", encoding='utf-16')

    for language,language_abbreviation in offical_languages.items():
        url = "https://european-union.europa.eu/institutions-law-budget/institutions-and-bodies/types-institutions-and-bodies_" + language_abbreviation
        
        text = get_website_text(url, "short")
    
        languageList.append(language)
        languageAbbreviationList.append(language_abbreviation)
        sentenceList.append(text)
        combinationDictionary[language] = text

        f.write(url)
        f.write("\n")
        f.write(language)
        f.write("\n")
        f.write(text)
        f.write("\n")
        f.write("---------")
        f.write("\n")
        
    f.close()
    return languageList, languageAbbreviationList, sentenceList, combinationDictionary



