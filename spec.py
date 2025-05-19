
"""
spécifiaction tour
tour_1 :
    cooldown entre chaque balle :
        40 tick entre chaque tire (1,33 tire par seconde)
    range : 
        200px
    Tire a tavers les énemies
        Non
    effect des tire (geler, renentie, ect) :
        Non
    dégat de zone :
        Non
    dégat par tire :
        3 dmg par tire 
    index balle:
        0
    cost upgrade:
        350, 500
tour_2 :
    cooldown entre chaque balle :
        60 tick entrer chaque tire (1 tire par seconde)
    range:
        250 pixel
    Tire a tavers les énemies
        Oui
    effect des tire (geler, renentie, ect) :
        Non
    dégat de zone :
        Non
    dégat par tire :
        3 dmg par tire
    index balle:
        1
    cost upgrade:
        600, 1200

tour_3 et plus:
    duplication de la tour  1 pour tester des fonctionalité dans le code
        """
#cooldow, range, pénétration, effect tire, dégat des tire, index balle, cost upgrade next lv 
tour_1 = [(40 , 200, False, None, 20, 0, 350, 0), (20 , 400, False, None, 20, 0, 500 , 0), (10 , 600, False, None, 20 , 0, None, 0)]
tour_2 = [(100, 250, False, None, 50, 1, 600, 0), (80 , 250, False, None, 75, 1, 1200, 0), (120, 250, False, None, 100, 1, None, 0)]
tour_3 = [(100, 400, False, None, 20, 2, 500, 1), (100, 400, False, None, 20, 2, 500 , 1), (100, 400, False, None, 20 , 2, None, 1)]
tour_4 = [(40 , 200, False, None, 20, 0, 350, 0), (20 , 200, False, None, 20, 0, 500 , 0), (10 , 200, False, None, 20 , 0, None, 0)]
tour_5 = [(40 , 200, False, None, 20, 0, 350, 0), (20 , 200, False, None, 20, 0, 500 , 0), (10 , 200, False, None, 20 , 0, None, 0)]
tour_6 = [(40 , 200, False, None, 20, 0, 350, 0), (20 , 200, False, None, 20, 0, 500 , 0), (10 , 200, False, None, 20 , 0, None, 0)]
stat_tour = (tour_1, tour_2, tour_3, tour_4, tour_5, tour_6)

#degat, vitesse, degat de zone, index image, index son
balle_1 = [20, 20, False, 0]
balle_2 = [50, 20, False, 1]
balle_3 = [60, 8 , 120 , 2]
stat_balle = (balle_1, balle_2, balle_3)

#speed, vie, degat, animation 
escargot = [1, 50  , 1, False]
poulet =   [2, 75  , 1, False]
bee =      [3, 75  , 1, False]
bear =     [2, 250 , 1, True]
rhino =    [1, 1000, 1, False]
oiseau =   [3, 200 , 1, True ]
stat_ennemie = (escargot, poulet, bee, bear, rhino, oiseau)
index_ennemie = {"escargot" : 0, "poulet" : 1, "bee" : 2, "bear" : 3, "rhino" : 4, "oiseau": 5}

"""
Forme demandée de la variable vague_predefinie:

vague_predefinie est une variable qui comporte des listes,
ces listes sont associées aux vagues du jeu. ex: la première liste de vague_predefinie correspond à la première vague du jeu.

dans ces listes, on retrouve les différentes chaînes d'ennemis qui seront spawn durant le jeu.
une chaîne d'ennemi correspond à [nom de l'ennemi, nb_d'ennemi, nb de ms entre chaque spawn]

donc je vais prendre pour exemple la première vague.
dans la première vague, il y a deux chaines d'ennemis,
la première chaîne est "["escargot", 10, 1000]", cela signifie que 10 escargots spawneront avec 1000ms de décallage.



Les points forts de ce système:
- On peut creer et personnaliser une grande diversité de vagues différentes
- On peut très bien faire spawn un type d'ennemi plusieurs fois et plus ou moins espacés
- Les vagues peuvent durer plus ou moins longtemps
- y'en a d'autres mais flemme

Les points faibles :
- On ne peut pas alterner successivement les types d'enemis dans une même chaine.
ex : On peut pas faire une chaine qui alterne escargot, poulet escargot, poulet.
fin en soit on peut le faire mais faudrai configurer le nb d'ennemi de chaque chaine = 1 mais ça ferait pleins de chaîne et en plus c'est super genant de faire ça
"""
"""
annimaux : 
"escargot"
"poulet"
"bee"
"bear"
"rhino"
"""
vague_predefinie = [
[
    ["escargot", 5, 1000]

],
[
    ["poulet", 20, 1000],
    ["poulet", 5, 1000]
],
[
    ["poulet", 20, 1000],
    ["poulet", 5, 1000]
],
[
    ["poulet", 20, 1000],
    ["poulet", 5, 1000]
],
[
    ["poulet", 20, 1000],
    ["poulet", 5, 1000]
],
[
   ["poulet", 20, 1000],
    ["poulet", 5, 1000]
]
]