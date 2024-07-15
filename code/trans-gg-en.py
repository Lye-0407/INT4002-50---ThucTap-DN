import re
import string
import json
from deep_translator import GoogleTranslator

file_path = 'dataset/query_file.json'
translated_file_path = 'dataset/transed-gg-en.json'

with open(file_path, 'r', encoding ='utf-8') as inputfile:
    data = json.load(inputfile)
  
def extract_clause(text):                                          

    lines = text.split("\n")                                                                        # split by \n      

    lines = [line for line in lines if line != ""]                                                  # remove empty lines

    if re.match(r"^([0-9]+)\. (.*)$", lines[0]):                                                    # if line[0] start with number
        title = None                                                                                # Title is None

        clauses = []
        current_clause = None

        for line in lines:                                                                          # Use regex to match number
            match_number = re.match(r"^([0-9]+)\. (.*)$", line)
            match_alphabet = re.match(r"^([a-z]\)|^\u0111\)) (.*)$", line)

            if match_number:                                                                        # if current clause is not None
                if current_clause is not None:
                    clauses.append(current_clause)

                current_clause = {                                                                  # Use regex to match alphabet
                    "clause_id": match_number.group(1),
                    "clause": match_number.group(2),
                    "sub_clauses": []
                }
            elif match_alphabet:                                                                    # Use regex to match alphabet
                current_clause["sub_clauses"].append(match_alphabet.group(2))                       # create new sub clause
            else:                                           
                current_clause["sub_clauses"].append(line)                                          # create new sub clause
        clauses.append(current_clause)                                                              # create new sub clause
        return {
            "title": title,
            "clauses": clauses
        }
    else:                                                                                           # if line[0] does not start with number
        title = lines[0]                                    
        clauses = []
        current_clause = None                                                                       # first index i that line[i] start with number
        first_index = 0
        for i in range(len(lines)):
            if re.match(r"^([0-9]+)\. (.*)$", lines[i]):
                first_index = i
                break
        if first_index == 0:                                                                        # if first_index == 0: that mean remaining lines does not start with number
            return {
                "title": title,                                                                     # so we just return title and remaining lines as sub_clauses of clause_id = 0
                "clauses": [
                    {
                        "clause_id": "0",
                        "clause": None,
                        "sub_clauses": lines[1:]
                    }
                ]
            }

        else:                                                                                       # from 1 to first_index - 1 is sub_clauses of clause_id = 0
            clauses.append({
                "clause_id": "0",
                "clause": None,
                "sub_clauses": lines[1:first_index]
            })
            for line in lines[first_index:]:                                                        # Loop remaining lines 
                match_number = re.match(r"^([0-9]+)\. (.*)$", line)                                 # Use regex to match number
                match_alphabet = re.match(r"^([a-z]\)|^\u0111\)) (.*)$", line)
                if match_number:                            
                    if current_clause is not None:                                                  # if current clause is not None
                        clauses.append(current_clause)                                              # create new clause
                    current_clause = {
                        "clause_id": match_number.group(1),
                        "clause": match_number.group(2),
                        "sub_clauses": []
                    }
                elif match_alphabet:                                                                # Use regex to match alphabet
                    current_clause["sub_clauses"].append(match_alphabet.group(2))                 # create new sub clause
                else:                                       
                    current_clause["sub_clauses"].append(line)                                           # create new sub clause
            clauses.append(current_clause)                                                          # add last clause

            return {
                "title": title,
                "clauses": clauses
            }
        
def gg_translation(text):
    if text is None:
        return ""
    return GoogleTranslator(source = 'auto', target = 'en').translate(text) 

def flatten_json(nested_json):
    out = {}
    
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def split_article_text(article_text, delimiter="\n\n"):
    return article_text.split(delimiter)

def join_article_text(article_list, delimiter="\n\n"):
    return delimiter.join(article_list)

for query in data:

    split_text_list = []

    query['query_text'] = gg_translation(query['query_text'])

    for relevant_article in query['relevant_article']:

        relevant_article['law_id'] = gg_translation(relevant_article['law_id'])

        relevant_article['article_text'] = (split_article_text(relevant_article['article_text']))

        for article_text in relevant_article['article_text']:

            article_text = gg_translation(article_text)

            split_text_list.append(article_text)

    relevant_article['article_text'] = join_article_text(split_text_list)

with open(translated_file_path, 'w', encoding='utf-8') as outputfile:
    json.dump(data, outputfile, ensure_ascii = False, indent = 4)