
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
#cooldow, range, pénétration, effect tire, dégat de zone, dégat des tire, index balle, cost upgrade next lv 
tour_1 = [(40, 200, False, None, False, 20, 0, 350), (20, 200, False, None, False, 20, 0, 500), (10, 200, False, None, False, 20, 0, None)]
tour_2 = [(100, 250, True, None, False, 50, 1, 600), (80, 250, True, None, False, 75, 1, 1200), (120, 250, True, None, False, 100, 1, None)]
tour_3 = [(200, 500, False, None, True, 20, 2, 350), (150, 500, False, None, True, 20, 2, 500), (100, 500, False, None, True, 20, 2, None)]
tour_4 = [(40, 200, False, None, False, 20, 0, 350), (20, 200, False, None, False, 20, 0, 500), (10, 200, False, None, False, 20, 0, None)]
tour_5 = [(40, 200, False, None, False, 20, 0, 350), (20, 200, False, None, False, 20, 0, 500), (10, 200, False, None, False, 20, 0, None)]
tour_6 = [(40, 200, False, None, False, 20, 0, 350), (20, 200, False, None, False, 20, 0, 500), (10, 200, False, None, False, 20, 0, None)]
stat_tour = [tour_1, tour_2, tour_3, tour_4, tour_5, tour_6]