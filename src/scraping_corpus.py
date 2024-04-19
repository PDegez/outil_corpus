#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 15:14:31 2024
@author: pauline

Extraction de 50 commentaires sur le jeu "Starfield" depuis sa page steam.
Utilisation de request
"""
import argparse, requests, json, csv


# récupérer 50 reviews :
def get_50_reviews(url):
    reviews = []
        
    # Critères que les commentaires doivent respecter pour etre retenus :
    # -> format json
    # -> commentaires rédigés en anglais
    # -> commentaires rédigés dans les 365 derniers jours
    # -> commentaires positifs et négatifs
    # -> nombre de commentaire à grap
    options = {
            'json' : 1,
            'language' : 'english',
            'day_range' : 365,
            'review_type' : 'all',
            'num_per_page' : 50
            }
    
    # récupération du contenu avec request
    retour = requests.get(
        url,
        params=options,
        headers={'User-Agent': 'Mozilla/5.0'})
    reviews = retour.json()['reviews']
    
    return reviews


def reformatage(reviews:list[dict])->list:
    
    reviews_reformatees = [
        {
            "customer_id" : str(review['author']['steamid']),
            "helpful_vote" : review['votes_up'],
            "product_id" : "1716740",
            "product_title" : "Starfield",
            "review_body" : review['review'],
            "review_date": review['timestamp_created'],
            "review_id" : review['recommendationid'],
            "score" : int(review['voted_up']),
            "steam_purchase" : review['steam_purchase'],
            "received_for_free" : review['received_for_free']
            } 
        for review in reviews
        ]
    
    return reviews_reformatees
    

def main(args):
    
    url = "https://store.steampowered.com/appreviews/1716740?json=1"
    brut = get_50_reviews(url)
    reviews_formatees = reformatage(brut)
    
    if args.csv :
        with open(args.output_file, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["customer_id", "helpful_vote", "product_id", "product_title",
                 "review_body", "review_date", "review_id", "score",
                 "steam_purchase", "received_for_free"
                             ])
            for review in reviews_formatees :
                writer.writerow(review.values())

    else:
        with open(args.output_file, "w") as file:
            reviews = {'reviews':reviews_formatees} 
            json.dump(reviews, file, indent=2)

    return print(f"Les reviews sont dans le fichier {args.output_file}")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extraction de 50 commentaires steam")
    parser.add_argument("-c", "--csv", action="store_true",
                        help="output en csv")
    parser.add_argument("output_file", help="Chemin de l'output")
    args = parser.parse_args()
    
    main(args)

