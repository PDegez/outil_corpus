## OUTILS DE TRAITEMENT DE CORPUS ##

# TD1 #

Tache choisie : classification
Corpus choisi : amazon_us_reviews (Hugging-Face)


A PROPOS DU CORPUS :

Il s'agit d'un corpus de langue anglaise (100M<n<1B).


Cependant, Amazon étant un site marchand international, l'anglais représenté peut différer en fonction de la zone géographique (Amazon US, amazon UK, Australie etc) mais aussi, de façon moins prévisible, de l'identité du commentateur (anglais natif / l2)
Le corpus est un ensemble de commentaires postés par des clients sur le site marchand Amazon.
Il est subdivisé en sous parties en fonction du type d'object sur lequel portent les commentaires. Ex :

- Apparel_v1_00 (vêtement)

- Automotive_v1_00 (pièce de voiture, accessoire de voiture etc)

- Baby_v1_00 (objets en lien avec la petite enfance)

- Beauty_v1_00 (produit de beauté)

- Book_v1_00 (livre)

- ...


Chaque commentaire sous son format d'entrainement est un dictionnaire dont les clés sont communes à toutes les subdivisions du corpus :

- "customer_ID"        numéro d'identification du client   (str)

- "helpful_votes"      combien de fois ce commentaire a été taggué comme utile (int32)

- "marketplace"        l'endroit géographique du marketplace   (str)

- "product_category"   catégorie de produit (baby, apparel etc...) (str)

- "product_id":        numéro du produit (str)

- "product_parent"     numéro du produit parent        -> ? pas plus d'informations données (str)

- "product_title"      nom du produit (str)

- "review_body"        corpus du commentaire (str)

- "review_date"        date du commentaire (str)

- "review_headline"    titre du commentaire (str)

- "review_id"          ID du commentaire (str)

- "star_rating"        nombre d'étoile (score donné par le client au produit qu'il commente) (int32)

- "total_votes"        nombre total de vote reçu par le commentaire (positif ou négatif) (int32)

- "verified_purchase"  0/1 (classification label)

- "vine"               0/1 (classification label)  "review was written in the vine programm"


Le programme Vine est mis en place par Amazon pour favoriser le nombre de commentaire utiles en proposant aux commentateurs régulièrements notés comme "pertinents/utiles" de recevoir des produits gratuitement en échange d'un commentaire de qualité (quelle que soit la polarité du commentaire. Le but n'est pas nécessairement promotionnel)


Ce corpus a été créer afin de servir à l'entrainement sur plusieurs taches:

- Text classification

    - commentaire positif / négatif / neutre

    - commentaire légitime ou "faux" commentaire (détection de bots / intention "promotionnelle" dans le commentaire)

    - commentaire de qualité (helpful / not helpful)

- Fill mask

    - entrainer un modèle à deviner un mots en fonction de ses voisins

- text generation

    - apprendre à un modèle à écrire un avis positif, négatif

    - apprendre à un modèle à écrire un commentaire utile



Les sous-tâches :

- text scoring : appariement d'un texte et d'un score (combien d'étoile ce commentaire va-t-il avoir ?)

- language modeling

- masked language modeling



! Ce corpus n'est plus disponible sur Hugging Face ("Defunct: Dataset "amazon_us_reviews" is defunct and no longer accessible due to the decision of data providers.") bien qu'ayant servi à entrainer plusieurs modèles (16 sont répertoriés sur hugging face), dont par exemple :

- DataMonkey   classifier les commentaires en commentaire de 1 à 5 étoiles

- Beaucoup de modèle de génération textuelle, comme le modèle praveenseb (nom du créateur ?) qui permet de générer des commentaires, ainsi qu'une note (nombre d'étoile) et un titre cohérents avec le commentaire.


Projection :
Récréer un corpus d'avis sur un site marchand (steam ?) dans le but d'entrainer un modèle sur une classe de classification ou text scoring.

- langue anglais ou français (à décider)

- un type de produit (livre ? jeux vidéos ? Films ?)


