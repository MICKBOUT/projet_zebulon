
"""
spécifiaction tour
tour_1 :
    cooldown entre chaque balle :
        0,8 (75 tire par seconde)
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

tour_2 :
    cooldown entre chaque balle :
        1 (60 tire par seconde)
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
"""

tour_1 = [0.8, 200, False, None, False, 3]
tour_2 = [1, 250, True, None, False, 3]

stat_tour = [tour_1, tour_2]
