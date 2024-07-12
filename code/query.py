import json
import os

file_path1 = './dataset/test.json'
file_path2 = './dataset/legal_passages.json'
query_file_path = 'dataset/test_query_file.json'

with open (file_path1,'r', encoding='utf-8') as inputfile1:
    inputdata1 = json.load(inputfile1)

with open (file_path2,'r', encoding='utf-8') as inputfile2:
    inputdata2 = json.load(inputfile2)

extracted_data = []

for query1 in inputdata1:
    example_id = query1['example_id']
    # label_id = query1['label']
    statement = query1['statement']

    relevant_articles = []
    for data1 in query1['legal_passages']:
        law_id = data1['law_id']
        article_id = data1['article_id']
        
        for query2 in inputdata2:
            passages_id = query2['id']
            if law_id == passages_id:
                for data2 in query2['articles']:
                    articles_id = data2['id']
                    articles_text = data2['text']
                    if article_id == articles_id:
                        map_articles = {"law_id": law_id, "article_id": article_id, "article_text": articles_text}
        relevant_articles.append(map_articles)

    extracted_data.append({
                        'query_id': example_id,
                        # 'label': label_id,
                        'query_text': statement,
                        'relevant_article': relevant_articles
                        })               

with open(query_file_path, 'w', encoding='utf-8') as outputfile:
    json.dump(extracted_data, outputfile, ensure_ascii=False, indent=4)        

