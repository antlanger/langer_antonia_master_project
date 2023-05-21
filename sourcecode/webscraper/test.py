import requests
import os
from bs4 import BeautifulSoup

offical_languages = {
    'English': 'en',
}

def get_website_text(websiteUrl):

    page = requests.get(websiteUrl)
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(id="main-content")
    list_elements = results.find_all("div", class_="ecl")

    titles = []

    for list_element in list_elements:
        para = list_element.find_all("p")
        print(para)
        print("\n")
        print("-----")
        print("\n")

    #for list_element in list_elements:
    #    title_element = list_element.find("div", class_="ecl-timeline__title")
    #    
    #    content_element = list_element.find("div", class_="ecl-timeline__content")
    #    paragraph_element = content_element.find("p")
        
        #print(title_element.text.strip())
        #print(paragraph_element.text.strip())

    #    titles.append(title_element.text.strip())

    return titles


# ------------------------------- START METHOD ------------------------------- #

for language,language_abbreviation in offical_languages.items():
    url = "https://european-union.europa.eu/principles-countries-history/principles-and-values/aims-and-values_" + language_abbreviation
    text = get_website_text(url)
    

        