import requests
from bs4 import BeautifulSoup
import os

def getLongText(websiteUrl):
    page = requests.get(websiteUrl)
    soup = BeautifulSoup(page.content, "html.parser")
        
    results = soup.find(id="block-ewcms-theme-main-page-content")
    list_texts = results.find_all("div", class_="ecl-u-mb-2xl")

    list_texts.pop(3)
    list_texts.pop(11)
    list_texts.pop(11)


    #print(list_texts)

    paragraph_texts = []

    # ------- First section start
    list_item_texts = list_texts[0].find_all("div", class_="ecl")
    paragraphs_0 = list_item_texts[0].find_all("p")
    paragraphs_0.pop(5)
    paragraphs_0.pop(7)

    lists_0 = list_item_texts[0].find_all("ul")
    paragraph_and_list_item_0 = []
    li_list_items_0 = []

    for paragraph_0 in paragraphs_0:
        paragraph_and_list_item_0.append(paragraph_0.getText())

    li_list_items_0_raw = lists_0[0].find_all("li")

    for li_list_item_0 in li_list_items_0_raw:
        li_list_items_0.append(li_list_item_0.getText())
            
    li_list_items_0_0 = []
    li_list_items_0_0.append(li_list_items_0[0])
    li_list_items_0_0.append(li_list_items_0[1])
    li_list_items_0_0.append(li_list_items_0[2])
    li_list_items_0_0.append(li_list_items_0[3])

    li_list_items_0_0_text = ', '.join(li_list_items_0_0)
        
    paragraph_and_list_item_0.insert(4, li_list_items_0_0_text)
    paragraph_and_list_item_0.insert(5, ".")

    li_list_items_0_raw = lists_0[1].find_all("li")
    for li_list_item_0 in li_list_items_0_raw:
            li_list_items_0.append(li_list_item_0.getText())
            
    li_list_items_0_1 = []
    li_list_items_0_1.append(li_list_items_0[0])
    li_list_items_0_1.append(li_list_items_0[1])
    li_list_items_0_1.append(li_list_items_0[2])
    li_list_items_0_1.append(li_list_items_0[3])

    li_list_items_0_0_text = ', '.join(li_list_items_0_1)
        
    paragraph_and_list_item_0.insert(7, li_list_items_0_0_text)
    paragraph_and_list_item_0.insert(8, ".")

    list_texts.pop(0)

    # ------- First section end

    for list_text in list_texts:
        list_item_texts = list_text.find_all("div", class_="ecl")

        for list_item_text in list_item_texts:
            paragraphs = list_item_text.find_all("p")
            paragraph_text = ""

            paragraph_count = len(paragraphs)
            for paragraph in paragraphs:
                if 'https://www.ema.europa.eu/en/news-events/therapeutic-areas-latest-updates/viral-diseases' in str(paragraph):
                    break
                paragraph_text = paragraph_text + " " + paragraph.getText()
        
            paragraph_texts.append(paragraph_text)

    long_text = ' '.join(paragraph_and_list_item_0) + ' '.join(paragraph_texts)
    no_words = len(long_text.split())
    print(no_words)

    middle_text_file = open(os.path.abspath(os.curdir) + '/sourcecode/files/' + "long_text_file.txt", "w")
    middle_text_file.write(long_text)
    middle_text_file.close() 

    return long_text




