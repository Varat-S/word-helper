import csv
from nltk.corpus import wordnet as wn
def get_wordnet_examples(word):
    examples = []
    for syn in wn.synsets(word):
        examples.extend(syn.examples())
    return examples if examples else None

def get_tatoeba_examples(word, file_path = "data\eng_sentences.tsv"):
    examples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) >= 3 and row[1] == 'eng':
                sentence = row[2].strip()
                if word.lower() in sentence.lower():
                    examples.append(sentence)
    return examples if examples else None

def get_example_sentences(word):
    all_examples=[]
    wn_examples = get_wordnet_examples(word)
    tato_examples = get_tatoeba_examples(word)
    if tato_examples:
        all_examples.extend(tato_examples)
    if wn_examples:
        all_examples.extend(wn_examples)
    if all_examples:
        return all_examples