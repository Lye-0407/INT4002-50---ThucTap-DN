import re
import string
import json
from deep_translator import GoogleTranslator

file_path = 'dataset/query_file.json'
translated_file_path = 'dataset/transed-gg-en.json'

with open(file_path, 'r', encoding ='utf-8') as inputfile:
    data = json.load(inputfile)

# Remove unnecessary characters
def clean_text_for_segmentation(text: str) -> str:
    text = re.sub(r'\[\d+\]', ' ', text)

    # Remove /n, /t
    text = re.sub(r'[\n\t]', ' ', text)

    # Remove 1. 2. 3. ... ~1.000.000
    text = re.sub(r'\b\d+\.\s+', ' ', text)

    # Remove a) b) c) ...
    text = re.sub(r'[a-zđ]\)', ' ', text)

    # Remove punctuation
    # text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove leading and trailing spaces
    text = text.strip()

    # Lowercase
    text = text.lower()

    return text

def search(law_id, article_id, query_file):
    for relevant_article in query_file:
        if relevant_article["law_id"] == law_id:
            for article_id in relevant_article:
                if relevant_article["article_id"] == article_id:
                    return {
                        "query_id": query_file["query_id"],
                        "query_text": query_file["query_text"],
                        "law_id": law_id,
                        "article_id": article_id,
                        "article_text": relevant_article["article_text"],
                        "article_clause":relevant_article["article_clause"]
                    }
    return {
        "query_id": None,
        "query_text": None,
        "law_id": law_id,
        "article_id": article_id,
        "article_text": None,
        "article_clause": None
    }
    
def extract_clause(text):
    # split by \n
    lines = text.split("\n")

    # remove empty lines
    lines = [line for line in lines if line != ""]

    # if line[0] start with number
    if re.match(r"^([0-9]+)\. (.*)$", lines[0]):
        # Title is None
        title = None

        clauses = []
        current_clause = None

        for line in lines:
            # Use regex to match number
            match_number = re.match(r"^([0-9]+)\. (.*)$", line)
            match_alphabet = re.match(r"^([a-z]\)|^\u0111\)) (.*)$", line)

            if match_number:
                # if current clause is not None
                if current_clause is not None:
                    clauses.append(current_clause)

                # create new clause
                current_clause = {
                    "clause_id": match_number.group(1),
                    "clause": match_number.group(2),
                    "sub_clauses": []
                }
            # Use regex to match alphabet
            elif match_alphabet:
                # create new sub clause
                current_clause["sub_clauses"].append(
                    match_alphabet.group(2)
                )

            else:
                # create new sub clause
                current_clause["sub_clauses"].append(
                    line
                )

        # add last clause
        clauses.append(current_clause)

        return {
            "title": title,
            "clauses": clauses
        }

    # if line[0] does not start with number
    else:
        # Title is first line
        title = lines[0]

        clauses = []
        current_clause = None

        # first index i that line[i] start with number
        first_index = 0

        for i in range(len(lines)):
            if re.match(r"^([0-9]+)\. (.*)$", lines[i]):
                first_index = i
                break

        # if first_index == 0: that mean remaining lines does not start with number
        # so we just return title and remaining lines as sub_clauses of clause_id = 0
        if first_index == 0:
            return {
                "title": title,
                "clauses": [
                    {
                        "clause_id": "0",
                        "clause": None,
                        "sub_clauses": lines[1:]
                    }
                ]
            }

        else:
            # from 1 to first_index - 1 is sub_clauses of clause_id = 0
            clauses.append({
                "clause_id": "0",
                "clause": None,
                "sub_clauses": lines[1:first_index]
            })

            # Loop remaining lines
            for line in lines[first_index:]:
                # Use regex to match number
                match_number = re.match(r"^([0-9]+)\. (.*)$", line)
                match_alphabet = re.match(r"^([a-z]\)|^\u0111\)) (.*)$", line)

                if match_number:
                    # if current clause is not None
                    if current_clause is not None:
                        clauses.append(current_clause)

                    # create new clause
                    current_clause = {
                        "clause_id": match_number.group(1),
                        "clause": match_number.group(2),
                        "sub_clauses": []
                    }
                # Use regex to match alphabet
                elif match_alphabet:
                    # create new sub clause
                    current_clause["sub_clauses"].append(
                        match_alphabet.group(2)
                    )

                else:
                    # create new sub clause
                    current_clause["sub_clauses"].append(
                        line
                    )

            # add last clause
            clauses.append(current_clause)

            return {
                "title": title,
                "clauses": clauses
            }
        
def gg_translation(text):
    if text is None:
        return ""
    return GoogleTranslator(source = 'auto', target = 'en').translate(text)

for query in data:
    relevant_article = query.get('relevant_article', {})
    print(relevant_article)
    break
    if 'law_id' in relevant_article:
        relevant_article['law_id'] = gg_translation(relevant_article['law_id'])
    
    for article_text in relevant_article:
        article_text = extract_clause(article_text)

        print("print article after segmentation")
        print("ARTICLE TEXT", article_text)

        if 'title' in article_text:
            article_text['title'] = gg_translation(article_text['title'])

        if 'clauses' in article_text:
            
            for clause in article_text['clauses']:
                print(clause)
                clause = gg_translation(clause['clause'])

            # for sub_clauses in article_text['clauses']: 
            #     sub_clauses = gg_translation(sub_clauses)

        if 'article_clause' in relevant_article:
            relevant_article['article_clause'] = gg_translation(relevant_article['article_clause'])    

# with open(translated_file_path, 'w', encoding='utf-8') as outputfile:
#     json.dump(data, outputfile, ensure_ascii = False, indent = 4)