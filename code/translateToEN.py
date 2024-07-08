import json 
from googletrans import Translator

translator = Translator()

file_path = 'dataset/query_file.json'
translated_file_path = 'dataset/query_file_translated.json'

with open(file_path, 'r', encoding ='utf-8') as inputfile:
    data = json.load(inputfile)

# translate function
def translate_text(text, src = 'vi', dest ='en'):
    try:
        translated = translator.translate(text, src = src, dest = dest)
        return translated.text

    except Exception as e:
        print(f"Error translating text: {text}. Error: {e}")
        return text


for query in data:
    relevant_article = query.get('relevant_article', {})

    if 'law_id' in relevant_article:
        relevant_article['law_id'] = translate_text(relevant_article['law_id'])

    if 'article_text' in relevant_article:
        relevant_article['article_text'] = translate_text(relevant_article['article_text'])
    

with open(translated_file_path, 'w', encoding='utf-8') as outputfile:
    json.dump(data, outputfile, ensure_ascii = False, indent = 4)
