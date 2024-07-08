import json
import os

file_path = './dataset/legal_passages.json'

with open (file_path,'r', encoding='utf-8') as inputfile:
    inputdata = json.load(inputfile)

query_id = ""
query_text = ""

extracted_data = []

for law in inputdata:
    law_id = law['id']
    for article in law['articles']:
        article_id = article['id']
        article_text = article['text']
        extracted_data.append({
            'query_id': query_id,
            'query_text': query_text,
            'relevant_article': {
                'article_id': article_id,
                'law_id': law_id,
                'article_text': article_text
            }
        })

query_file_path = 'dataset/query_file.json'
with open(query_file_path, 'w', encoding='utf-8') as outputfile:
    json.dump(extracted_data, outputfile, ensure_ascii=False, indent=4)        
