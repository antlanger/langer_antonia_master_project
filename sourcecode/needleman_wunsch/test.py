language = [
    'Deutsch',
    'Englisch',
    'Französisch',
    'Spanisch',
    'Italienisch',
    'Finnisch'
]
 
sentences = [
    'Das ist das Leben',
    'This is life',
    'C\'est la vie',
    'Así es la vida',
    'Questa è vita',
    'Tämä on elämää'
]

combinations = {
    'Deutsch':'Das ist das Leben',
    'Englisch':'This is life',
    'Französisch':'C\'est la vie',
    'Spanisch':'Así es la vida',
    'Italienisch':'Questa è vita',
    'Finnisch':'Tämä on elämää'   
}

for x in language:
    print(x)
    print(combinations.get(x))
    #print(combinations[x])