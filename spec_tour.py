
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
    prix :
        300
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
    prix :
        500
    cost upgrade:
        600, 1200

tour_3 et plus:
    duplication de la tour  1 pour tester des fonctionalité dans le code
        """

tour_1 = [40, 200, False, None, False, 20, 0, (350, 500)]
tour_2 = [80, 250, True, None, False, 50, 1, (600, 1200)]
tour_3 = [40, 200, False, None, False, 20, 0, (350, 500)]
tour_4 = [40, 200, False, None, False, 20, 0, (350, 500)]
tour_5 = [40, 200, False, None, False, 20, 0, (350, 500)]
tour_6 = [40, 200, False, None, False, 20, 0, (350, 500)]
stat_tour = [tour_1, tour_2, tour_3, tour_4, tour_5, tour_6]