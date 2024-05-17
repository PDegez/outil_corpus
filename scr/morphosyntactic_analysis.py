#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:06:43 2024
@author: pauline

Annotation morphosyntaxique (lemme et pos) des commentaires depuis un fichier 
json. Le résultat de l'annotation est un fichier json ou csv.

Parameters
----------
input_file : str
    chemin vers le fichier input json
output_file : str
    chemin du fichier output
-c : option format csv
    output en format csv (format json par défaut)
-l : option lemmatize only
    lance seulement le lemmatiseur, au lieu de l'annotation complète'

Returns
-------
Corpus annoté dans un fichier json ou csv
"""

import argparse
import json
from dataclasses import dataclass

import spacy
from scraping_corpus import write_csv, write_json


@dataclass
class Token:
    """dataclasse pour l'annotation morphosyntaxique des tokens:

    Attributes:
    ----------
    raw : str
        token sous sa forme brute
    lemma : str
        forme lemme du token
    pos : str
        pos du token
    """

    raw: str
    lemma: str
    pos: str


def main(args):
    load_model = spacy.load("en_core_web_sm")

    with open(args.input_file, "r", encoding="utf-8") as file:
        corpus = json.load(file)

    if args.lemmatizer:
        for review in corpus["reviews"]:
            traitement = load_model(review["review_body"])
            review["review_body"] = " ".join([token.lemma_ for token in traitement])

    else:
        for review in corpus["reviews"]:
            traitement = load_model(review["review_body"])
            review["review_body"] = " ".join(
                [token.lemma_ + "_" + token.pos_ for token in traitement]
            )

    if args.csv:
        write_csv(corpus, args.output_file)
    else:
        write_json(corpus, args.output_file)

    return print("fin du script")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="morphosyntaxic analysis")
    parser.add_argument("-c", "--csv", action="store_true", help="output en csv")
    parser.add_argument(
        "-l", "--lemmatizer", action="store_true", help="lemmatize only"
    )
    parser.add_argument("input_file", help="Chemin de l'output")
    parser.add_argument("output_file", help="Chemin de l'output")
    args = parser.parse_args()

    main(args)
