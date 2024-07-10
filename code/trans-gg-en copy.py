import json
from deep_translator import GoogleTranslator

file_path = 'dataset/query_file.json'
translated_file_path = 'dataset/transed-gg-en.json'

with open(file_path, 'r', encoding ='utf-8') as inputfile:
    data = json.load(inputfile)

def gg_translation(text):

    translated = GoogleTranslator(source = 'auto', target = 'en').translate(text)
    return translated

def translate_text(text):
    max_length = 5000
    if len(text) <= max_length:
        return gg_translation(text)
    else:
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        translated_parts = [gg_translation(part) for part in parts]
        return ''.join(translated_parts)
    
for query in data:
    relevant_article = query.get('relevant_article', {})

    if 'law_id' in relevant_article:
        relevant_article['law_id'] = translate_text(relevant_article['law_id'])


for query in data:
    relevant_article = query.get('relevant_article', {})

    if 'article_text' in relevant_article:
        relevant_article['article_text'] = translate_text(relevant_article['article_text'])
    

with open(translated_file_path, 'w', encoding='utf-8') as outputfile:
    json.dump(data, outputfile, ensure_ascii = False, indent = 4)