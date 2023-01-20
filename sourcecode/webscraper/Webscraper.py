import requests
from bs4 import BeautifulSoup

offical_languages = {
    'English': 'en',
    'German': 'de',
    'Spanish': 'es',
    'Italian': 'it',
    'Gaelic': 'ga',
    'French': 'fr'
}


def get_website_text(websiteUrl, language):
    url = websiteUrl+language
    print('### WEBSITE-NAME: ' + url)

    page = requests.get(url)
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
    for language,language_abbreviation in offical_languages.items():
        text = get_website_text("https://european-union.europa.eu/principles-countries-history/history-eu_", language_abbreviation)
        print(language)
        print(text)
        print('------------------------------------------------')



if __name__ == "__main__" :
        start_scraping()
