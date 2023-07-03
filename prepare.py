import chardet
import os
import re
def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc
target_word="Example"
filename = 'Question-Scrapper/Questiondata/index.txt'
my_encoding = find_encoding(filename)
data=[]
directory ="Question-Scrapper/Questiondata/"
def preprocess(document_text): 
    terms = [term.lower() for term in document_text.strip().split()[1:]] 
    return terms

#this will remove chaacters and separed the words
def preprocess1(document_text):
    terms = []
    for term in document_text.strip().split()[1:]:
        cleaned_term = re.sub(r'[^a-zA-Z]+', ' ', term)
        cleaned_term = cleaned_term.strip()
        if cleaned_term:
            terms.extend(cleaned_term.lower().split())
    return terms
for i in range(1,2406):
    data_lines = ""
    with open(directory+str(i)+"/"+str(i)+".txt",'r') as text:
        for line in text:
            
            if target_word in line:
                break  # Stop copying lines if the target word is found
            data_lines+= line.strip()
        data.append(preprocess1(data_lines))


with open(filename, 'r', encoding=my_encoding) as f:
    lines = f.readlines()




vocab = {} 
documents = []
for index, line in enumerate(lines):
    tokens = preprocess(line)
    data_token=data[index]
    documents.append(tokens+data_token)
    # documents.append(data_token)
    data_token=set(data_token)
    tokens = set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1
    for dtoken in data_token:
        if dtoken not in vocab:
            vocab[dtoken] = 1
        else:
            vocab[dtoken] += 1

vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

print('Number of documents: ', len(documents))
print('Size of vocab: ', len(vocab))
print('Sample document: ', documents[2])

with open('tf-idf/vocab.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

with open('tf-idf/idf-values.txt', 'w') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

with open('tf-idf/documents.txt', 'w') as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))


inverted_index = {}
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

with open('tf-idf/inverted-index.txt', 'w') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
