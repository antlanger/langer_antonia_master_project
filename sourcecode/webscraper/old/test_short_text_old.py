import requests
from bs4 import BeautifulSoup
import os


page = requests.get("https://european-union.europa.eu/principles-countries-history/principles-and-values/aims-and-values_de")
soup = BeautifulSoup(page.content, "html.parser")
    
results = soup.find(id="block-ewcms-theme-main-page-content")

#list_headings = results.find_all("h2", class_="ecl-u-type-heading-2")
#value_heading = list_headings[1].text.strip()
#print(value_heading)

list_texts = results.find_all("div", class_="ecl")
value_text = list_texts[1].text.strip()
#print(value_text)



#short_text = value_heading + value_text
short_text = value_text

no_words = len(short_text.split())
print("SHORT - Number of words: " + str(no_words))

## Write into a file
short_text_file = open(os.path.abspath(os.curdir) + '/sourcecode/files/' + "short_text_file.txt", "w")
short_text_file.write(short_text)
short_text_file.close()