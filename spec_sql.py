import sqlite3
from collections import defaultdict

#importation du ficher sql
conn = sqlite3.connect('game_data.db')
c = conn.cursor()

#stat_tour
c.execute('SELECT * FROM tours')
stat_tour = {}
for row in c.fetchall():
    tour_num = row[1]
    if tour_num not in stat_tour:
        stat_tour[tour_num] = []
    stat_tour[tour_num].append(tuple(row[3:]))

#stat_balle
c.execute("SELECT damage, speed, range, image_index FROM balles")
balles = [tuple(row) for row in c.fetchall()]
stat_balle =  tuple(balles)

#state ennemie
c.execute("SELECT speed, hp, damage, animation, argent_drop FROM ennemis")
ennemis = [tuple(row) for row in c.fetchall()]
stat_ennemie =  tuple(ennemis)

#vague_predefinie
c.execute("SELECT wave_num, enemy_name, count, delay_ms FROM vagues")
vagues_dict = defaultdict(list)
for wave_num, name, count, delay in c.fetchall():
    vagues_dict[wave_num].append([name, count, delay])
vague_predefinie = [vagues_dict[i+1] for i in range(len(vagues_dict))]

conn.close()

if __name__ == "__main__":
    print("stat_tour :")
    for keys, values in stat_tour.items(): print(keys, values)
    print("stat_balle :", stat_balle)
    print("stat_ennemie :", stat_ennemie)
    print("vague_predefinie :")
    for ligne in vague_predefinie: print(ligne)