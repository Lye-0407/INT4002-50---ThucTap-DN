import json
from deep_translator import GoogleTranslator

file_path = 'dataset/query_file.json'
translated_file_path = 'dataset/transed-gg-en.json'

with open(file_path, 'r', encoding ='utf-8') as inputfile:
    data = json.load(inputfile)

'''
def pre_processing(text):
    text = text.replace("\n", " ")
    return " ".join(text.split())
def gg_translation(data_input):    
    return GoogleTranslator(source='auto', target='en').translate(pre_processing(data_input))
'''

def gg_translation(data_input):    
    return GoogleTranslator(source='auto', target='en').translate((data_input))

for query in data:
    relevant_article = query.get('relevant_article', {})

    if 'law_id' in relevant_article:
        relevant_article['law_id'] = gg_translation(relevant_article['law_id'])

    if 'article_text' in relevant_article:
        relevant_article['article_text'] = gg_translation(relevant_article['article_text'])
    

with open(translated_file_path, 'w', encoding='utf-8') as outputfile:
    json.dump(data, outputfile, ensure_ascii = False, indent = 4)