import math
import chardet
import re
#to find encoding
def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc
my_encoding = find_encoding('Question-Scrapper/Questiondata/index.txt')
documents =[]
inverted_index ={}
vocab = {}
final_link=[]
orig_doc=[]


#for links
with open('Question-Scrapper/Questiondata/Qindex.txt', 'r') as file:
    final_link= file.readlines()
#for headings
with open('Question-Scrapper/Questiondata/index.txt', 'r', encoding=my_encoding) as file:
    for line in file: 
        pattern = r"\d+\.\s*"  
        line = re.sub(pattern, "", line)
        line = line.strip() 
        orig_doc.append(line)

with open('tf-idf/documents.txt', 'r') as file:
    documents= file.readlines()
documents = [document.strip().split() for document in documents]

with open('tf-idf/vocab.txt', 'r') as f:
        terms = f.readlines()
with open('tf-idf/idf-values.txt', 'r') as f:
        idf_values = f.readlines()

for (term,idf_value) in zip(terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())

with open('tf-idf/inverted-index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        list = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = list
#we will get term freq value, using inverted index
def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values
def get_idf_value(term):
    return math.log((1+len(documents))/(1+vocab[term]))

def calculate_sorted_order_of_documents(query_terms):
    pot_links = []  

    potential_documents = {}
    for term in query_terms:
        try:
            tf_values_by_document = get_tf_dictionary(term)
            idf_value = get_idf_value(term)
            for document in tf_values_by_document:
                if document not in potential_documents:
                    potential_documents[document] = tf_values_by_document[document] * idf_value
                else:
                    potential_documents[document] += tf_values_by_document[document] * idf_value
        except KeyError:
            continue

    for document in potential_documents:
        potential_documents[document] /= len(query_terms)

    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

    for document_index in potential_documents:
        title = orig_doc[int(document_index)]
        url = final_link[int(document_index)].strip()
        pot_links.append((title, url))  

    return pot_links


def get_links(query):
    query_terms = [term.lower() for term in query.strip().split()]
    return calculate_sorted_order_of_documents(query_terms)

# query_string = input('Enter your query: ')
# # query_s = [term.lower() for term in query_string.strip().split()]

# print(get_links(query_string))

