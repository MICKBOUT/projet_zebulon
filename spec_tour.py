
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
"""

tour_1 = [40, 200, False, None, False, 20, 0]
tour_2 = [80, 250, True, None, False, 50, 1]

stat_tour = [tour_1, tour_2]
