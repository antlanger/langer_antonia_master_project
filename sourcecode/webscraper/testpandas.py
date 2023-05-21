import pandas as pd



dataframe = pd.read_excel(r'./sourcecode/webscraper/Abbreviations.xlsx')

print(dict(zip(dataframe['Language'], dataframe['Version 1'])))