#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:14:31 2024
@author: pauline

Extraction de 50 commentaires sur le jeu "Starfield" depuis sa page steam
vers un fichier json ou csv

Parameters
----------
output_file : str
    chemin du fichier output.
-c : option
    output en format csv (format json par défaut)

Returns
-------
Corpus dans un fichier json ou csv
"""

import argparse
import csv
import datetime
import json

import requests


def get_100_reviews(url):
    """récupération de 100 commentaires.

    Parameters
    ----------
    url : str
        l'url de la page steam du jeu (ici Starfield)

    Returns
    -------
    reviews : list[dict]
        liste de dictionnaire où chaque dictionnaire est un commentaire qui
        contient les paire clés-valeurs suivantes :

            "customer_id" : str
                identifiant steam de l'auteur du commentaire
            "helpful_vote" : int
                nombre de fois que ce commentaire a été voté comme utile
            "product_id" : str
                identifiant steam du jeu
            "product_title" : str
                titre du jeu. Ici, "Starfield"
            "review_body" : str
                corps textuel du commentaire
            "review_date": str(
                datetime.datetime.fromtimestamp(review['timestamp_created']))
                date d'écriture du commentaire
            "review_id" : str
                identifiant steam du commentaire
            "score" : bool
                score attribué par le commentateur (positif = 1, négatif = 0)
            "steam_purchase" : bool
                indique si le commentateur a acheté le jeu sur steam
            "received_for_free" : bool
                indique si le commentateur a reçu le jeu gratuitement
    """

    reviews = []

    # Critères que les commentaires doivent respecter pour etre retenus :
    # -> format json
    # -> commentaires rédigés en anglais
    # -> commentaires rédigés dans les 365 derniers jours
    # -> commentaires positifs et négatifs
    # -> nombre de commentaire à grap (ici 100 : maximum grabable sans ajouter
    # de curseur)

    options = {
        "json": 1,
        "language": "english",
        "day_range": 365,
        "review_type": "all",
        "num_per_page": 100,
    }

    # récupération du contenu au format json avec request
    retour = requests.get(url, params=options, headers={"User-Agent": "Mozilla/5.0"})
    reviews = retour.json()["reviews"]

    return reviews


def reformatage(reviews: list[dict]) -> list:
    """formatage des reviews, élagage et équilibrage pour garder un nombre
    équivalent de reviews positives et négatives (25 de chaaque).

    Parameters
    ----------
    reviews : list[dict]
        liste de dictionnaires où chaque dictionnaire est un commentaire
        (see also l'output de la fonction get_100_reviews pour les détails
         sur les clés et valeurs')

    Returns
    -------
    reviews_eq : list[dict]
        une liste de 50 dictionnaires, 25 correspondants à des commentaires
        positifs et leurs métadonnées, 25 correspondants à des commentaires
        négatifs et leurs métadonnées"""

    # adaptation des données pour s'approcher du corpus à émuler :
    # -> récupération des données équivalentes
    # -> suppression des données non pertinentes

    reviews_reformatees = [
        {
            "customer_id": str(review["author"]["steamid"]),
            "helpful_vote": review["votes_up"],
            "product_id": "1716740",
            "product_title": "Starfield",
            "review_body": review["review"],
            "review_date": str(
                datetime.datetime.fromtimestamp(review["timestamp_created"])
            ),
            "review_id": review["recommendationid"],
            "score": int(review["voted_up"]),
            "steam_purchase": review["steam_purchase"],
            "received_for_free": review["received_for_free"],
        }
        for review in reviews
    ]

    # équilibrage : 25 reviews positives et 25 review negatives
    pos_rev = []
    neg_rev = []
    for review in reviews_reformatees:
        if review["score"] == 1 and len(pos_rev) < 25:
            pos_rev.append(review)
        if review["score"] == 0 and len(neg_rev) < 25:
            neg_rev.append(review)

    review_eq = pos_rev + neg_rev

    return review_eq


def write_csv(data: list[dict], output_file):
    """enregistrement des reviews en csv.

    Parameters
    ----------
    data : list[dict]
        liste de dictionnaire où chaque dictionnaire est un commentaire et ses
        métadonnées
    output_file : str
        chemin vers le fichier output

    Returns
    -------
    Print et création d'un fichier csv"""

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "customer_id",
                "helpful_vote",
                "product_id",
                "product_title",
                "review_body",
                "review_date",
                "review_id",
                "score",
                "steam_purchase",
                "received_for_free",
            ]
        )
        for review in data:
            writer.writerow(review.values())

    return print(f"{len(data)} reviews dans {output_file}.")


def write_json(data: list[dict], output_file):
    """enregistrement des reviews en json;

    Parameters
    ----------
    data : list[dict]
        liste de dictionnaire où chaque dictionnaire est un commentaire et ses
        métadonnées
    output_file : str
        chemin vers le fichier output

    Returns
    -------
    Print et création d'un fichier json
    """

    with open(output_file, "w") as file:
        reviews = {"reviews": data}
        json.dump(reviews, file, indent=2)

    return print(f"{len(data)} reviews dans {output_file}.")


def main(args):
    url = "https://store.steampowered.com/appreviews/1716740?json=1"
    brut = get_100_reviews(url)
    reviews_formatees = reformatage(brut)

    if args.csv:
        write_csv(reviews_formatees, args.output_file)
    else:
        write_json(reviews_formatees, args.output_file)

    return print("fin du script")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extraction de 50 commentaires steam")
    parser.add_argument("-c", "--csv", action="store_true", help="output en csv")
    parser.add_argument("output_file", help="Chemin de l'output")
    args = parser.parse_args()

    main(args)
