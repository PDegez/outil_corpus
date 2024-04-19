#!/Documents/Cours/outil_de_traitement_de_corpus/env_selenium/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 00:45:41 2024
@author: pauline

Lemmatizer le corpus avec spacy depuis un format json,
export en format csv ou json
"""
import spacy, argparse, json
from scraping_corpus import write_json, write_csv
  

def main(args):
        
    load_model = spacy.load("en_core_web_sm")

    with open(args.input_file, 'r', encoding='utf-8') as file:
        corpus = json.load(file)
    
    for review in corpus['reviews'] :
       traitement = load_model(review['review_body'])
       review['review_body'] = " ".join([token.lemma_ for token in traitement])
    
    if args.csv:
        write_csv(corpus, args.output_file)
    else:
        write_json(corpus, args.output_file)
    
    return print("fin du script")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lemmatizer")
    parser.add_argument("-c", "--csv", action="store_true",
                        help="output en csv")
    parser.add_argument("input_file", help="Chemin de l'output")
    parser.add_argument("output_file", help="Chemin de l'output")
    args = parser.parse_args()
    
    main()