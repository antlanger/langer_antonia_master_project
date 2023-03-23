import requests
import sys
from bs4 import BeautifulSoup
from textobject import *



offical_languages = {
    'English': 'en',
    'German': 'de',
    'Spanish': 'es',
    'Italian': 'it',
    'Gaelic': 'ga',
    'French': 'fr'
}


def get_website_text(websiteUrl):
    print('### WEBSITE-NAME: ' + websiteUrl)

    page = requests.get(websiteUrl)
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(id="main-content")
    list_elements = results.find_all("li", class_="ecl-timeline__item")

    titles = []

    for list_element in list_elements:
        title_element = list_element.find("div", class_="ecl-timeline__title")
        
        content_element = list_element.find("div", class_="ecl-timeline__content")
        paragraph_element = content_element.find("p")
        
        #print(title_element.text.strip())
        #print(paragraph_element.text.strip())

        titles.append(title_element.text.strip())

    return titles

    
def start_scraping():
    elementList = []

    f = open("scraping_01.txt", "a")

    for language,language_abbreviation in offical_languages.items():
        url = "https://european-union.europa.eu/principles-countries-history/history-eu_" + language_abbreviation
        text = get_website_text(url)
        
        textElement = TextObject(url, language, text)
        elementList.append(textElement)

        f.write(url)
        f.write("\n")
        f.write(language)
        f.write("\n")
        f.write(text[0])
        f.write("\n")
        f.write("---------")
        f.write("\n")
        
    f.close()
    return elementList



if __name__ == "__main__" :
        scrapedElements = start_scraping()
