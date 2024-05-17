#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:30:05 2024
@author: pauline

Ce script converti un corpus depuis un fichier json ou csv en un format dataset
avant de l'imprimer en sortie standard

Parameters
----------
input_file : str
    chemin vers le fichier input json ou csv

Returns
-------
corpus : Dataset
    print du corpus sous forme de dataset dans la sortie standard
"""

import argparse

import pandas as pd
from datasets import Dataset


def main(chemin_input):
    chemin = args.input_file
    print(chemin[-4:])
    if str(chemin[-4:]) == ".csv":
        data = pd.read_csv(chemin, delimiter=",")
    elif chemin[-5:] == ".json":
        data = pd.read_json(chemin)
    else:
        return print("Ce script prend un csv ou un json en entrée")
    dataset = Dataset.from_pandas(data)
    print(dataset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="transformer en dataset")
    parser.add_argument("input_file", help="Chemin de l'input")
    args = parser.parse_args()

    main(args)
