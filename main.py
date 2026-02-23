import pygame
import math
from spec_sql import stat_tour, stat_balle, \
    stat_ennemie, vague_predefinie

# Initialisation
pygame.init()
pygame.display.set_caption("V1 Tower Defense")
clock = pygame.time.Clock()

son = True
music = True
pause = False
running = True
mode_placement = False
mode_ameliorer = False
volume = 0.6

# screen
frame_rate = 60
screen_longeur = 1600
screen_hauteur = 900
# Résolution officielle
screen = pygame.display.set_mode((screen_longeur, screen_hauteur))

# map
map_image = pygame.image.load("map/map.png").convert()
map_rect = map_image.get_rect(topleft=(0, 0))
background_planks = pygame.image.load(
    "assets/background/planks_background.jpg").convert()

# image ennemie
ennemi_escargot_image = (
    pygame.image.load("assets/enemi/escargot.png").convert_alpha(),
    pygame.image.load("assets/enemi/escargot_toucher.png").convert_alpha()
)
ennemi_poulet_image = (
    pygame.image.load("assets/enemi/poulet.png").convert_alpha(),
    pygame.image.load("assets/enemi/poulet_toucher.png").convert_alpha()
)
ennemi_bee_image = (
    pygame.image.load("assets/enemi/bee.png").convert_alpha(),
    pygame.image.load("assets/enemi/bee_toucher.png").convert_alpha()
)
ennemi_rhino_image = (
    pygame.image.load("assets/enemi/rhino.png").convert_alpha(),
    pygame.image.load("assets/enemi/rinho_toucher.png").convert_alpha()
)

ennemi_ours_image = (
    (
        pygame.image.load("assets/enemi/bear_1.png").convert_alpha(),
        pygame.image.load("assets/enemi/bear_2.png").convert_alpha(),
        pygame.image.load("assets/enemi/bear_3.png").convert_alpha()),
    (
        pygame.image.load("assets/enemi/bear_toucher_1.png").convert_alpha(),
        pygame.image.load("assets/enemi/bear_toucher_2.png").convert_alpha(),
        pygame.image.load("assets/enemi/bear_toucher_3.png").convert_alpha())
)

ennemie_oiseau_image = (
    (
        pygame.image.load("assets/enemi/oiseau_1.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_2.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_3.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_4.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_5.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_6.png").convert_alpha()),
    (
        pygame.image.load("assets/enemi/oiseau_toucher_1.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_toucher_2.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_toucher_3.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_toucher_4.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_toucher_5.png").convert_alpha(),
        pygame.image.load("assets/enemi/oiseau_toucher_6.png").convert_alpha())
)
# Background image
background_v1 = pygame.image.load("assets/tour/background_v1.png").convert()

pygame.mixer.music.load("assets/sound/background_audio.ogg")
pygame.mixer.music.play(-1)

# Dans le cas ou la variable plus haut est régler sur False
if not son or not music:
    pygame.mixer.music.pause()

# Icone
vie_image = pygame.image.load("assets/button/coeur.png").convert_alpha()

# Boutton
path = "assets/button/"
load_ctm = pygame.image.load  # load custom
bouton_reset_image = load_ctm(f"{path}/reset.png").convert_alpha()
bouton_plus_image = load_ctm(f"{path}/plus.png").convert_alpha()
bouton_moins_image = load_ctm(f"{path}/moins.png").convert_alpha()
bouton_accelere_image = load_ctm(f"{path}/accelere.png").convert_alpha()
bouton_vendre_tour_image = load_ctm(
    f"{path}/vendre_la_tour.png").convert_alpha()
bouton_setting_image = load_ctm(f"{path}/setting.png").convert_alpha()
bouton_play_image = load_ctm(f"{path}/boutton_jouer.png").convert_alpha()
bouton_valider_image = load_ctm(f"{path}/valider.png").convert_alpha()
bouton_exit_placer_image = load_ctm(f"{path}/croix_fermer.png").convert_alpha()
bouton_son_on_image = load_ctm(f"{path}/son.png").convert_alpha()
bouton_son_off_image = load_ctm(f"{path}/muet.png").convert_alpha()
bouton_music_on_image = load_ctm(f"{path}/music_on.png").convert_alpha()
bouton_music_off_image = load_ctm(f"{path}/music_off.png").convert_alpha()

son_image = bouton_son_on_image if son else bouton_son_off_image
music_image = bouton_music_on_image if music else bouton_music_off_image

# Ecran noir opaque pour le menu pause
ecran_noir_opaque = pygame.Surface((1600, 900)).convert()
ecran_noir_opaque.fill((0, 0, 0))
ecran_noir_opaque.set_alpha(128)

# Event
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1000)

# Font
font = pygame.font.Font(None, 130)
font_prix = pygame.font.Font(None, 75)
font_amiliorer = pygame.font.Font(None, 39)

# Son
son_vente_tour = pygame.mixer.Sound("assets/sound/son_vente_tour.mp3")
son_refus = pygame.mixer.Sound("assets/sound/erreur.mp3")
son_tour_placer = pygame.mixer.Sound("assets/sound/placement_tour.mp3")
son_tire = pygame.mixer.Sound("assets/sound/tour_tire.mp3")
son_cannon = pygame.mixer.Sound("assets/sound/cannon_tire.mp3")
son_liste = (son_tire, son_cannon)

liste_son_gen = [
    son_vente_tour,
    son_refus,
    son_tour_placer,
    son_tire,
    son_cannon
]

text_son = font.render(f"{int(volume * 10)}", True, (105, 78, 165))
text_son_rect = text_son.get_rect(center=(550, 320))

# Tour :
# Image améliorer tout
text_amiloorer_tour = font_amiliorer.render(
    "voulez vous améliorer la tour ?",
    True,
    "cyan",
    "black"
)

text_amiliorer_nv_max = font_amiliorer.render(
    "Tour niveau max",
    True,
    "cyan",
    "black"
)

text_lv_up_tour_rect = text_amiloorer_tour.get_rect(
    midtop=(1400, 605)
)
text_amiliorer_nv_max_rect = text_amiliorer_nv_max.get_rect(
    midtop=(1400, 605)
)

# image Tour
load_tour = [
    pygame.image.load("assets/tour/tour_1_lv1.png").convert_alpha(),
    pygame.image.load("assets/tour/tour_2_rouge.png").convert_alpha(),
    pygame.image.load("assets/tour/tour_3_lv1.png").convert_alpha(),
    pygame.image.load("assets/tour/bank_lv1.png").convert_alpha(),
    pygame.image.load("assets/tour/tour_4_lv1.png").convert_alpha(),
]

liste_tour = [(tour, tour.get_rect(topleft=(0, 0))) for tour in load_tour]

liste_upgrade = (
    (
        pygame.image.load("assets/tour/tour_1_lv2.png").convert_alpha(),
        pygame.image.load("assets/tour/tour_1_lv3.png").convert_alpha()),
    (
        pygame.image.load("assets/tour/tour_2_rouge_lv2.png").convert_alpha(),
        pygame.image.load("assets/tour/tour_2_rouge_lv3.png").convert_alpha()),
    (
        pygame.image.load("assets/tour/tour_3_lv2.png").convert_alpha(),
        pygame.image.load("assets/tour/tour_3_lv3.png").convert_alpha()),
    (
        pygame.image.load("assets/tour/bank_lv2.png").convert_alpha(),
        pygame.image.load("assets/tour/bank_lv3.png").convert_alpha()),
    (
        pygame.image.load("assets/tour/tour_4_lv2.png").convert_alpha(),
        pygame.image.load("assets/tour/tour_4_lv3.png").convert_alpha())
)

border = pygame.image.load("assets/tour/border.png").convert_alpha()
border_rect = border.get_rect(topright=(screen_longeur, 0))

description = (
    load_ctm("assets/description_tour/description_tour_1.png").convert(),
    load_ctm("assets/description_tour/description_tour_2.png").convert(),
    load_ctm("assets/description_tour/description_tour_3.png").convert(),
    load_ctm("assets/description_tour/description_tour_4.png").convert(),
    load_ctm("assets/description_tour/description_tour_5.png").convert(),
    load_ctm("assets/description_tour/description_tour_6.png").convert(),
)

# Reste des prix pour les tours non défini
liste_tour_prix = [300, 500, 750, 2500, 15000]

if len(liste_tour_prix) <= len(liste_tour):
    liste_tour_prix += ([-1] * (len(liste_tour) - len(liste_tour_prix)))

# Balles
vitesse_balle = (20, 20, 8, 20, 20, 20)
liste_image_balle = (
    pygame.image.load("assets/balle/balle_1.png").convert_alpha(),
    pygame.image.load("assets/balle/balle_2.png").convert_alpha(),
    pygame.image.load("assets/balle/balle_3.png").convert_alpha()
)

explosion = (
    pygame.image.load("assets/balle/explosion_1.png").convert_alpha(),
    pygame.image.load("assets/balle/explosion_2.png").convert_alpha(),
    pygame.image.load("assets/balle/explosion_3.png").convert_alpha(),
    pygame.image.load("assets/balle/explosion_4.png").convert_alpha(),
    pygame.image.load("assets/balle/explosion_5.png").convert_alpha(),
    pygame.image.load("assets/balle/explosion_6.png").convert_alpha(),
    pygame.image.load("assets/balle/explosion_7.png").convert_alpha()
)

# Divers:
# Pour éviter les variable non define.
# Ene fois dans la boucle, elle est update en temps réel.
mouse_tour_rect = pygame.Rect(0, 0, 75, 75)
setting_rect = pygame.Rect((300, 200, 600, 400))

# Hitbox chemin + point pour ennemie
liste_point_chemin = (
    (0, 410, 230, 465),
    (170, 170, 230, 465),
    (170, 170, 455, 230),
    (410, 170, 470, 550),
    (410, 480, 790, 550),
    (730, 330, 790, 550),
    (730, 330, 1200, 390)
)

hitbox_chemin = [
    pygame.Rect(x1, y1, x2 - x1, y2 - y1)
    for x1, y1, x2, y2 in liste_point_chemin
]

point_ennemie = (
    (200, 440),
    (200, 200),
    (440, 200),
    (440, 515),
    (760, 515),
    (760, 360),
    (1200, 360)
)


class Enemi(pygame.sprite.Sprite):
    def __init__(self, index_ennemie, image):
        super().__init__()
        # self.image prend la liste de toutes les iamges et après
        # dans la fonction afficher(), la bonne est afficher
        self.image = image
        (
            self.speed,
            self.vie,
            self.damage,
            self.animation,
            self.argent_rapporté
        ) = stat_ennemie[index_ennemie]
        # dans le cas ou l'image a des animation,
        # la premire image est dans la deuxième liste
        if self.animation:
            self.rect = self.image[0][0].get_rect(center=(0, 440))
        else:
            self.rect = self.image[0].get_rect(center=(0, 440))
        # le point vers lequelle l'ennemie se dirige
        self.index_point = 0
        # est ce que l'ennemie est loin ou pas sur la map
        self.distance = 0
        # permet de compter le nb de frame pour que l'ennelie soit toucher
        self.toucher = 0
        # un compteur qui permet de savoir sur quelle image est le joueur
        self.compteur = 0

    def update(self):
        x, y = self.rect.center
        # si la valeur abs est plus petit que la vitesse alors
        # on met la pos a la destination
        # car a la prochaine frame l'ennemie sera au point
        if abs(x - point_ennemie[self.index_point][0]) < self.speed:
            # associer la valeur de x au pt pour plus tard
            # la mettre sur la variable slef.pos
            x = point_ennemie[self.index_point][0]
        else:  # l'ennemie est encore loin du point
            if x < point_ennemie[self.index_point][0]:
                x += self.speed
            else:
                x -= self.speed

        if abs(y - point_ennemie[self.index_point][1]) < self.speed:
            y = point_ennemie[self.index_point][1]
        else:
            if y < point_ennemie[self.index_point][1]:
                y += self.speed
            else:
                y -= self.speed
        self.distance += self.speed
        self.rect.center = (x, y)

        if (x, y) == point_ennemie[self.index_point] != point_ennemie[-1]:
            self.index_point += 1
        elif (x, y) == point_ennemie[-1]:
            self.kill()
            Vie_joueur.enleve_vie(self.damage)

    def enlever_vie(self, vie):
        self.vie -= vie
        self.toucher = 7
        if self.vie <= 0:
            self.kill()
            argent_joueur.ajouter(self.argent_rapporté)

    def frame(self):
        self.compteur += 1
        if self.compteur // 10 >= len(self.image[0]):
            self.compteur = 0

    def afficher(self):
        if self.toucher > 0:
            self.toucher -= 1
            if self.animation:
                screen.blit(self.image[1][self.compteur // 10], self.rect)
            else:
                screen.blit(self.image[1], self.rect)
        else:
            if self.animation:
                screen.blit(self.image[0][self.compteur // 10], self.rect)
            else:
                screen.blit(self.image[0], self.rect)

        if self.animation:  # sert a changer la fram pour que l'ennemie bouge
            self.frame()


class Button():
    def __init__(self, pos, image):
        """
        classe pour les boutons, pos est un tuple de (x, y) evidemment
        """
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def is_overmouse(self, pos):
        return self.rect.collidepoint(pos)

    def afficher(self):
        screen.blit(self.image, self.rect)


class Vie():
    def __init__(self, vie, image):
        self.vie_initiale = vie
        self.vie = vie
        self.pos = (100, 800)
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.text = font.render(str(vie), True, (150, 0, 0))

    def ajoute_vie(self, n):
        self.vie += n

    def enleve_vie(self, n):
        self.vie -= n

    def reinitialiser_vie(self):
        self.vie = self.vie_initiale

    def update(self):
        self.text = font.render(str(self.vie), True, (150, 0, 0))

    def afficher(self):
        screen.blit(self.image, self.pos)
        screen.blit(self.text, (205, 810))


class Argent():
    def __init__(self, argent):
        self.rendu = False
        self.argent = argent
        self.text = font.render(f"{self.argent}$", True, "black")
        self.tick_clignotment = 0
        self.couleur = "black"
        self.pos = (800, 810)

    def ajouter(self, n):
        self.argent += n
        self.rendu = True

    def retirer(self, n):
        self.argent -= n
        self.rendu = True

    def definir(self, n):
        self.argent = n
        self.rendu = True

    def clignotement(self):
        self.tick_clignotment = 90

    def update(self):
        if self.tick_clignotment > 0:
            if int(self.tick_clignotment // 10) % 2 == 0:
                self.couleur = "black"
                self.rendu = True
            else:
                self.rendu = True
                self.couleur = "red"
            self.tick_clignotment -= 1

        if self.rendu is True:
            self.text = font.render(f"{self.argent}$", True, self.couleur)
            self.rendu = False

    def afficher(self):
        screen.blit(self.text, ((780, 810)))


class Vagues():
    def __init__(self):
        self.numero_vague = 0
        self.running = False
        self.compteur_vague_tick = 0
        self.text_vague = font.render("Vague 0", True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(topleft=(360, 810))

    def prochaine_vague(self):
        self.numero_vague += 1
        self.running = True
        if self.numero_vague <= 30:
            self.ennemis_a_spawn = vague_predefinie[self.numero_vague-1]

        self.text_vague = font.render(f"Vague {self.numero_vague}",
                                      True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(center=(600, 850))
        self.numero_chaine, self.ennemis_spawn_de_la_chaine = 0, 0

    def update_vague(self):
        self.compteur_vague_tick += 1  # vrais ticks (de vague), initialisé à 0
        pygame.time.set_timer(SPAWN_ENEMY,
                              self.ennemis_a_spawn[self.numero_chaine][2])
        # si le nombre d'ennemis deja spawn est inférieur à celui prévu:
        if self.ennemis_spawn_de_la_chaine < self.ennemis_a_spawn[
                                                 self.numero_chaine][1]:
            if self.ennemis_a_spawn[self.numero_chaine][0] == "escargot":
                groupe_enemie.add(Enemi(0, ennemi_escargot_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "poulet":
                groupe_enemie.add(Enemi(1, ennemi_poulet_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "bee":
                groupe_enemie.add(Enemi(2, ennemi_bee_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "bear":
                groupe_enemie.add(Enemi(3, ennemi_ours_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "rhino":
                groupe_enemie.add(Enemi(4, ennemi_rhino_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "oiseau":
                groupe_enemie.add(Enemi(5, ennemie_oiseau_image))
            self.ennemis_spawn_de_la_chaine += 1

        elif len(self.ennemis_a_spawn)-1 > self.numero_chaine:
            self.numero_chaine += 1
            self.ennemis_spawn_de_la_chaine = 0

    def stop_vague(self):
        self.compteur_vague_tick = 0

    def afficher(self):
        screen.blit(self.text_vague, self.rect_text_vague)


class Tour(pygame.sprite.Sprite):
    """
    cette class contien tout les tour avec leur emplacement sur le terrain,
    elle notament a fair apparaitre les tours sur le terrain
    et gerer leur fonctionnement (tire, ect)
    """
    def __init__(self, position, nb_tour=0):
        super().__init__()
        (
            self.cooldown,
            self.range,
            self.degat,
            self.index_balle,
            self.cost_upgrade,
            self.son
        ) = stat_tour[nb_tour + 1][0]

        self.index_tour = nb_tour
        self.ennemie = None  # sert a savoir si un enemie est viser ou non
        self.angle = 0
        self.tick_depuis_dernier_tire = 0
        self.niveau = 1
        self.image_upgrade = liste_upgrade[nb_tour]
        self.image_load = liste_tour[nb_tour][0]  # image associer a la tour
        self.image = self.image_load
        # rect qui sert de hitbow a la tour
        self.rect = self.image_load.get_rect(center=(position))
        self.rect_image_affichage = self.rect
        self.position = position
        self.rayon = self.rect.w//2

    def upgrade(self):
        self.niveau += 1
        argent_joueur.retirer(self.cost_upgrade)
        self.image = self.image_upgrade[self.niveau - 2]
        self.image_load = self.image
        self.rect_image_affichage = self.image.get_rect(center=(self.position))
        (
            self.cooldown,
            self.range,
            self.degat,
            self.index_balle,
            self.cost_upgrade,
            self.son
        ) = stat_tour[self.index_tour + 1][self.niveau - 1]

    def viser(self):
        if not self.ennemie not in groupe_enemie:
            self.ennemie = None
        tampon_ennemie = None
        for ennemie in groupe_enemie:
            distance = math.sqrt(
                ((self.rect.centerx - ennemie.rect.centerx)**2)
                + ((self.rect.centery - ennemie.rect.centery)**2))
            if distance <= self.range:
                if (tampon_ennemie is None
                   or ennemie.distance > tampon_ennemie.distance):
                    tampon_ennemie = ennemie

        if tampon_ennemie is not None:
            self.ennemie = tampon_ennemie
        else:
            self.ennemie = None
        # ne pas mettre de else a la place du if
        # car si le self.enemie est définie dans la boucle du dessus,
        # il faut qu'on puisse rentrer dans cette boucle
        if self.ennemie is not None:
            # formule qui calcule l'angle (counterclockwize)
            self.angle = math.atan2(
                self.ennemie.rect.centery - self.rect.centery,
                self.ennemie.rect.centerx - self.rect.centerx)
            deg = -math.degrees(self.angle)
            self.image = pygame.transform.rotate(self.image_load, deg)
            self.rect_image_affichage = self.image.get_rect(
                center=(self.position))

    def tirer(self):
        if self.range > 0:
            if self.tick_depuis_dernier_tire >= self.cooldown:
                if self.ennemie is not None:
                    groupe_balle.add(
                        Balle_tour(
                            self.index_balle, self.rect.center, self.angle))
                    if son:
                        son_liste[self.son].play()
                    self.tick_depuis_dernier_tire = 0
            else:
                self.tick_depuis_dernier_tire += 1
        else:
            if Systeme_Vague.running:
                if self.tick_depuis_dernier_tire >= self.cooldown:
                    argent_joueur.ajouter(self.degat)
                    self.tick_depuis_dernier_tire = 0
                self.tick_depuis_dernier_tire += 1

    def update(self):
        if self.range > 0:
            self.viser()
        self.tirer()

    def afficher(self):
        screen.blit(self.image, self.rect_image_affichage)


class Balle_tour(pygame.sprite.Sprite):
    def __init__(self, index_balle, position, angle: float):
        super().__init__()
        # self.zone = False si la tour ne fait pas de dégats de zone
        # ou la range des dégat dans le cas contraire

        # self.image = index de l'image dans la liste,
        # c'est le cas uniquement dans la fonction init
        self.degat_balle, self.speed, self.zone, self.image = stat_balle[
            index_balle]
        self.image = pygame.transform.rotate(
            liste_image_balle[self.image], - math.degrees(angle))
        # direction vers la quelle la balle ce dirige a chaque
        self.direction_x, self.direction_y = math.cos(angle), math.sin(angle)
        self.pos = list(position)
        self.rect = self.image.get_rect(center=position)
        self.en_vie = True

    def mouvement(self):
        self.pos[0] += self.direction_x * self.speed
        self.pos[1] += self.direction_y * self.speed
        self.rect.center = self.pos
        if not map_rect.colliderect(self.rect):
            self.kill()

    def collision_ennemie(self):
        for ennemie in groupe_enemie:
            if self.rect.colliderect(ennemie.rect):
                if self.zone:
                    for ennemie_zone in groupe_enemie:
                        if (math.sqrt(
                           (self.pos[0] - ennemie_zone.rect.centerx) ** 2
                           + (self.pos[1] - ennemie_zone.rect.centery) ** 2)
                           <= self.zone):
                            ennemie_zone.enlever_vie(self.degat_balle)
                    self.en_vie = False
                    self.animation = 0
                    self.image = explosion[0]
                    self.rect = self.image.get_rect(center=self.pos)

                else:
                    ennemie.enlever_vie(self.degat_balle)
                    self.kill()
                break  # fait en sorte que la balle touche un seul ennemie

    def explosion(self):
        self.image = explosion[self.animation // 2]
        self.animation += 1
        if self.animation // 2 >= len(explosion):
            self.kill()

    def update(self):
        if self.en_vie:
            self.mouvement()
            self.collision_ennemie()
        else:
            self.explosion()

    def afficher(self):
        screen.blit(self.image, self.rect)


class Hud_tour(pygame.sprite.Sprite):
    def __init__(self, tour_index):
        super().__init__()
        self.tour_index = tour_index
        self.taille_reel = liste_tour[tour_index][1].w
        self.image = pygame.transform.scale_by(
            liste_tour[tour_index][0], 180/self.taille_reel)
        self.prix = liste_tour_prix[tour_index]
        self.rect = pygame.Rect(
            map_rect.right + 200 * ((tour_index) % 2),
            (200 * (tour_index // 2)),
            200,
            200
        )
        # avec 4, on peut créer un cercle avec ce rayon et avoir la même taille
        self.rayon = self.taille_reel // 2
        self.prix = font_prix.render(
            f"{liste_tour_prix[tour_index]}$",
            True,
            (0, 255, 255)
        )
        self.description = description[tour_index]

    def ajouter_tour(self, position):
        groupe_tour.add(Tour(position, self.tour_index))

    def afficher(self):
        """
        permet d'avoir un meilleur controle sur l'affichage des tours,
        avec le background et le reste
        """
        pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(background_v1, self.rect)
        screen.blit(self.image, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(self.prix, (self.rect.left + 10, self.rect.bottom - 50))


# variriable gérer par les classes
bouton_reset = Button((740, 440), bouton_reset_image)
bouton_moins = Button((610, 250), bouton_moins_image)
bouton_plus = Button((750, 250), bouton_plus_image)
bouton_music = bouton_music_on_image.get_rect(topleft=(350, 450))
bouton_son = bouton_son_on_image.get_rect(topleft=(350, 250))
bouton_ameliorer_valider = Button((1250, 675), bouton_valider_image)
bouton_ameliorer_annuler = Button((1400, 675), bouton_exit_placer_image)
bouton_vendre_la_tour = Button((1200, 800), bouton_vendre_tour_image)
bouton_exit_placer = Button((1200, 772), bouton_exit_placer_image)
bouton_accelere = Button((1108, 800), bouton_accelere_image)
# bouton pour aller dans les paramètres
bouton_setting = Button((1125, 10), bouton_setting_image)
# bouton pour lancer une vague
bouton_play = Button((10, 800), bouton_play_image)

hud = pygame.sprite.Group()  # group pour gérer le hud de tour
for i in range(len(liste_tour)):
    hud.add(Hud_tour(i))
groupe_enemie = pygame.sprite.Group()  # Groupe d'ennemis
groupe_tour = pygame.sprite.Group()  # groupe avec les tour
groupe_balle = pygame.sprite.Group()  # groupe avec les balles
Vie_joueur = Vie(100, vie_image)  # classe pour gérer la vie
argent_joueur = Argent(500)  # classe qui défini l'argent du joueur
Systeme_Vague = Vagues()  # classe pour gérer le système de vague
tour_selec_ameliorer = None  # aucune tour n'est selectioner


def reset():
    """
    cette conction permet de reset le jeu
    """
    global groupe_enemie, groupe_tour, groupe_balle, Vie_joueur, argent_joueur
    global Systeme_Vague, mode_placement, mode_ameliorer, pause
    groupe_enemie = pygame.sprite.Group()  # Groupe d'ennemis
    groupe_tour = pygame.sprite.Group()  # groupe avec les tour
    groupe_balle = pygame.sprite.Group()  # groupe avec les balles
    Vie_joueur = Vie(100, vie_image)  # classe pour gérer la vie
    argent_joueur = Argent(500)  # classe qui défini l'argent du joueur
    Systeme_Vague = Vagues()  # classe pour gérer le système de vague
    mode_placement = False
    mode_ameliorer = False
    pause = False


def entrer_mode_placement(tour_input):
    """
    ce scripte sert a ce que cette partie du code ne soit pas copier coller
    plusieur fois mais plutôt regrouper dans un seul scripte
    Input :
        Element de la classe Hud_tour dans le groupe pygame.srrite.Groupe hud.
    Output :
        None
    fait rentrer le jeu dans le mode placement
    avec la tour selectionner en input
    """
    global mode_placement, Tour_selec_placmt, mouse_tour_rect, mouse_tour_rayon
    mode_placement = True
    Tour_selec_placmt = tour_input
    # le - tour_input.rayon
    # sert a ce que le sprite ne soit pas placer a la mauvaise frame
    # sans avoir a utiliser un .center car la calsse n'est pas encore défini,
    # il faudrais peut être regarder si une solution plus opti est possible
    # dans le future
    mouse_tour_rect = pygame.Rect(
        (mouse_pos[0] - tour_input.rayon, mouse_pos[1] - tour_input.rayon),
        liste_tour[Tour_selec_placmt.tour_index][1].size)
    mouse_tour_rayon = Tour_selec_placmt.rayon


def affichage_gen():
    """
    cette fonction sert a afficher tout ce que le jeu doit montrer au joueur
    cette fonction ne change aucune variable
    elle s'occupe uniquement d'afficher sur l'écran
    """
    screen.fill((239, 239, 145))  # fond jaune
    screen.blit(map_image, (0, 0))  # map
    affichage_jeu()
    affichage_ath()


def affichage_jeu():
    """
    permet d'afficher tout les éléments qui sont en lien avec le jeu
    (la map les ennemies, les tours, ect)
    """
    for ennemie in groupe_enemie:  # affichage des ennemies
        ennemie.afficher()

    for tour in groupe_tour:  # affichage des tour
        tour.afficher()

    for balle in groupe_balle:  # affichage des balles
        balle.afficher()
    # affiche la range de la tour dans le mode améliorer
    # + le rectange qui montre qu'elle est séléctionner
    if mode_ameliorer:
        pygame.draw.rect(
            screen,
            "pink",
            tour_selec_ameliorer.rect
        )
        pygame.draw.circle(
            screen,
            "grey",
            tour_selec_ameliorer.rect.center,
            tour_selec_ameliorer.range,
            2
        )
        # car sinon le carré pink recouvre la tour
        tour_selec_ameliorer.afficher()

    if mode_placement:
        bouton_exit_placer.afficher()
        screen.blit(
            Tour_selec_placmt.image,
            (screen_longeur - 190, screen_hauteur - 190)
        )

        if map_rect.contains(mouse_tour_rect):
            if (
               not any(bout_de_chemin.colliderect(mouse_tour_rect)
                       for bout_de_chemin in hitbox_chemin)
               and not any(
                          math.sqrt(
                            (mouse_pos[0] - une_tour.rect.centerx)**2 +
                            (mouse_pos[1] - une_tour.rect.centery)**2)
                          <=
                          (une_tour.rayon + mouse_tour_rayon - 5)
                          for une_tour in groupe_tour)
               ):
                pygame.draw.rect(screen, "green", mouse_tour_rect)
                screen.blit(
                    liste_tour[Tour_selec_placmt.tour_index][0],
                    (mouse_pos[0] -
                     (Tour_selec_placmt.taille_reel // 2),
                     mouse_pos[1] -
                     (Tour_selec_placmt.taille_reel // 2))
                )
            else:
                pygame.draw.rect(screen, "black", (mouse_tour_rect))
                screen.blit(
                    liste_tour[Tour_selec_placmt.tour_index][0],
                    (mouse_pos[0] -
                     (Tour_selec_placmt.taille_reel//2),
                     mouse_pos[1] -
                     (Tour_selec_placmt.taille_reel//2))
                )

    if mode_placement:  # range de la tour
        bouton_exit_placer.afficher()
        pygame.draw.circle(
            screen,
            "grey",
            mouse_pos,
            stat_tour[Tour_selec_placmt.tour_index + 1][0][1], 2)
        screen.blit(
            Tour_selec_placmt.image,
            (screen_longeur - 190, screen_hauteur - 190)
        )

        if map_rect.contains(mouse_tour_rect):
            if (
               not any(
                      bout_de_chemin.colliderect(mouse_tour_rect)
                      for bout_de_chemin in hitbox_chemin)
               and not any(
                        math.sqrt(
                            (mouse_pos[0] - une_tour.rect.centerx)**2 +
                            (mouse_pos[1] - une_tour.rect.centery)**2)
                        <=
                        (une_tour.rayon + mouse_tour_rayon - 5)
                        for une_tour in groupe_tour)
               ):
                pygame.draw.rect(screen, "green", mouse_tour_rect)
                screen.blit(
                    liste_tour[Tour_selec_placmt.tour_index][0],
                    (mouse_pos[0] -
                     (Tour_selec_placmt.taille_reel // 2),
                     mouse_pos[1] -
                     (Tour_selec_placmt.taille_reel // 2)))
            else:
                pygame.draw.rect(screen, "black", (mouse_tour_rect))
                screen.blit(
                    liste_tour[Tour_selec_placmt.tour_index][0],
                    (mouse_pos[0] -
                     (Tour_selec_placmt.taille_reel//2),
                     mouse_pos[1] -
                     (Tour_selec_placmt.taille_reel//2))
                )


def affichage_ath():
    """
    affiche tout ce qui est sur les boods de l'écran
    (vie, argent, vague, ect)
    cette fonction ne change aucune variable
    elle s'occupe uniquement d'afficher sur l'écran
    """
    Systeme_Vague.afficher()  # Affiche le text de la vague
    # Affiche le bouton pour passer a la vague d'après
    if not Systeme_Vague.running:
        bouton_play.afficher()

    # la description de la tour s'affiche
    # que si le joueur ne selectionne pas de tour
    if not (mode_ameliorer or mode_placement):
        for tour_hud in hud:
            if tour_hud.rect.collidepoint(mouse_pos):
                screen.blit(tour_hud.description, (1200, 600))
                # la souris ne peut pas être sur deux tour a la fois
                # donc si on trouve la tour sur laquelle le joueur est
                # ca ne sert a rien de continuer
                break

    if not mode_placement:
        # bouton setting
        bouton_setting.afficher()

    if mode_ameliorer:
        if tour_selec_ameliorer.niveau < 3:
            screen.blit(text_amiloorer_tour, text_lv_up_tour_rect)
            screen.blit(text_cost_lv_up, text_cost_lv_up_rect)
            bouton_ameliorer_valider.afficher()
            bouton_ameliorer_annuler.afficher()
        else:
            screen.blit(text_amiliorer_nv_max, text_amiliorer_nv_max_rect)
        bouton_vendre_la_tour.afficher()

    for élément in hud:
        élément.afficher()

    Vie_joueur.afficher()
    argent_joueur.afficher()  # permet d'afficher l'argnet du joueur
    bouton_accelere.afficher()


def set_volume(valeur):
    """
    valeur est la variable a laquelle tout les son sont régler
    """
    global text_son, text_son_rect

    for s in liste_son_gen:
        s.set_volume(valeur)
    if music:
        pygame.mixer.music.set_volume(valeur)
    text_son = font.render(f"{int(valeur * 10)}", True, (105, 78, 165))
    text_son_rect = text_son.get_rect(center=(550, 320))


# Boucle principale
while running:
    mouse_pos = pygame.mouse.get_pos()
    if pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # evente qui permet de quiter le jeu
                running = False

            # event pour détecter les touches du clavier appuyer
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    pause = False

            # event pour détecter les clique de la souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not setting_rect.collidepoint(mouse_pos):
                        pause = False
                    elif bouton_son.collidepoint(mouse_pos):
                        if son:
                            son = False
                            pygame.mixer.music.pause()
                            son_image = bouton_son_off_image
                        else:
                            son = True
                            pygame.mixer.music.unpause()
                            son_image = bouton_son_on_image

                    elif bouton_moins.is_overmouse(mouse_pos):
                        if volume >= 0.2:
                            volume -= 0.1
                        else:
                            volume = 0
                        set_volume(volume)

                    elif bouton_plus.is_overmouse(mouse_pos):
                        if volume <= 0.8:
                            volume += 0.1
                        else:
                            volume = 1
                        set_volume(volume)

                    elif bouton_music.collidepoint(mouse_pos):
                        if music:
                            music = False
                            pygame.mixer.music.set_volume(0)
                            music_image = bouton_music_off_image
                        else:
                            music = True
                            pygame.mixer.music.set_volume(volume)
                            music_image = bouton_music_on_image

                    elif bouton_reset.is_overmouse(mouse_pos):
                        reset()

        affichage_gen()  # affichage habituelle:
        # perrmet d'avoir un fond noircis
        # pour que le joueur comprenne qu'il est dans une autres fenêtre
        screen.blit(ecran_noir_opaque, (0, 0))
        # fond qui sert de menu pause
        pygame.draw.rect(screen, "black", (300, 200, 600, 400))
        pygame.draw.rect(screen, (255, 240, 188), (310, 210, 580, 380))
        screen.blit(son_image, bouton_son)
        screen.blit(music_image, bouton_music)
        screen.blit(text_son, text_son_rect)
        bouton_plus.afficher()
        bouton_moins.afficher()
        bouton_reset.afficher()

    else:  # boucle normal, dans le cas ou le jeu n'est pas en pause
        mouse_pos = pygame.mouse.get_pos()
        mouse_tour_rect.center = mouse_pos

        # Gestion des événements
        for event in pygame.event.get():
            # evente qui permet de quiter le jeu
            if event.type == pygame.QUIT:
                running = False

            # event pour détecter les touches du clavier appuyer
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not (mode_placement or mode_ameliorer):
                        pause = True
                    else:
                        mode_placement = False
                        mode_ameliorer = False

                if event.key == pygame.K_1:  # Créer un nouvel ennemi #escargot
                    groupe_enemie.add(Enemi(0, ennemi_escargot_image))

                elif event.key == pygame.K_2:  # poulet
                    groupe_enemie.add(Enemi(1, ennemi_poulet_image))

                elif event.key == pygame.K_3:  # bee
                    groupe_enemie.add(Enemi(2, ennemi_bee_image))

                elif event.key == pygame.K_4:  # bear
                    groupe_enemie.add(Enemi(3, ennemi_ours_image))

                elif event.key == pygame.K_5:  # rhino
                    groupe_enemie.add(Enemi(4, ennemi_rhino_image))

                elif event.key == pygame.K_6:  # oiseau
                    groupe_enemie.add(Enemi(5, ennemie_oiseau_image))

                elif event.key == pygame.K_SPACE:
                    argent_joueur.ajouter(1000)

                # pour que le joueur puisse selectioner une tour
                # avec son clavier
                elif event.key == pygame.K_a:
                    mode_ameliorer = False
                    if argent_joueur.argent >= liste_tour_prix[0]:
                        entrer_mode_placement(hud.sprites()[0])
                    else:
                        if son:
                            son_refus.play()
                        argent_joueur.clignotement()

                elif event.key == pygame.K_z:
                    mode_ameliorer = False
                    if argent_joueur.argent >= liste_tour_prix[1]:
                        entrer_mode_placement(hud.sprites()[1])
                    else:
                        if son:
                            son_refus.play()
                        argent_joueur.clignotement()

                elif event.key == pygame.K_e:
                    mode_ameliorer = False
                    if argent_joueur.argent >= liste_tour_prix[2]:
                        entrer_mode_placement(hud.sprites()[2])
                    else:
                        if son:
                            son_refus.play()
                        argent_joueur.clignotement()

            # parti qui controle se qui se passe une fois
            # que le joueur a cliquer qqpart

            # event pour détecter les clique de la souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # si le joueur fait un clique gauche
                    # print(mouse_pos) fonction pour debuger
                    if (bouton_setting.is_overmouse(mouse_pos) and
                       not mode_placement):
                        pause = True

                    # event pour detécter si la souris est sur le bouton
                    elif bouton_play.is_overmouse(mouse_pos):
                        if not Systeme_Vague.running:
                            Systeme_Vague.prochaine_vague()

                    elif bouton_exit_placer.is_overmouse(mouse_pos):
                        mode_placement = False

                    elif bouton_accelere.is_overmouse(mouse_pos):
                        if frame_rate >= 240:
                            frame_rate = 60
                        else:
                            frame_rate *= 2

                # gestion des tours
                # cette parti gère le joueur
                # si il veux rentrer dans le mode placement
                    for icone_tour in hud:
                        if icone_tour.rect.collidepoint(mouse_pos):
                            if mode_ameliorer:
                                mode_ameliorer = False
                            if (argent_joueur.argent >=
                               liste_tour_prix[icone_tour.tour_index]):
                                entrer_mode_placement(icone_tour)
                            else:
                                if son:
                                    son_refus.play()
                                argent_joueur.clignotement()

                    # est activé si le joueur
                    # est dans le mode placement de tour
                    if mode_placement is True:
                        # verifier si les coordoner sont dans l'écran
                        if map_rect.contains(mouse_tour_rect):
                            # est ce que le curseur est sur le chemin ?
                            if not any(
                                       bout_de_chemin.colliderect(
                                        mouse_tour_rect)
                                       for bout_de_chemin in hitbox_chemin):
                                if not any(
                                    math.sqrt(
                                        (mouse_pos[0] -
                                         une_tour.rect.centerx)**2 +
                                        (mouse_pos[1] -
                                         une_tour.rect.centery)**2)
                                        <=
                                        une_tour.rayon + mouse_tour_rayon - 5
                                        for une_tour in groupe_tour):
                                    # le -5 est pour une marge
                                    # et que le jeu ne soit pas trop frustrant
                                    # pour le joueur)
                                    mode_placement = False
                                    if son:
                                        son_tour_placer.play()
                                    Tour_selec_placmt.ajouter_tour(
                                        mouse_pos)
                                    argent_joueur.retirer(
                                        liste_tour_prix[
                                            Tour_selec_placmt.tour_index]
                                    )
                    else:
                        # si mode placment == False
                        # mais le joueur est dans le mode améliorer
                        if mode_ameliorer:
                            if bouton_ameliorer_valider.is_overmouse(
                               mouse_pos):
                                if tour_selec_ameliorer.niveau < 3:
                                    if (
                                       argent_joueur.argent >=
                                       tour_selec_ameliorer.cost_upgrade
                                       ):
                                        tour_selec_ameliorer.upgrade()
                                    else:
                                        if son:
                                            son_refus.play()
                                        argent_joueur.clignotement()

                            elif bouton_vendre_la_tour.is_overmouse(mouse_pos):
                                tour_selec_ameliorer.kill()
                                rendre = liste_tour_prix[
                                    tour_selec_ameliorer.index_tour]
                                # a lv 1 ont n'a pas upgrade la tour
                                for i in range(
                                   tour_selec_ameliorer.niveau - 1):
                                    rendre += stat_tour[
                                        tour_selec_ameliorer.index_tour][
                                            i][6]
                                argent_joueur.ajouter(rendre // 2)
                                if son:
                                    son_vente_tour.play()
                            mode_ameliorer = False

                        # mode placement == False ->
                        # fonction qui clique sur une tour et qui regarde +
                        # le joueur n'est pas dans le mode amiliorer
                        for une_tour in groupe_tour:
                            if math.sqrt(
                                (mouse_pos[0] -
                                 une_tour.rect.centerx)**2 +
                                (mouse_pos[1] -
                                 une_tour.rect.centery)**2) <= une_tour.rayon:
                                tour_selec_ameliorer = une_tour
                                mode_ameliorer = True
                                if tour_selec_ameliorer.niveau < 3:
                                    text_cost_lv_up = (
                                        font_amiliorer.render(
                                            f"""coût amélioration :
                                            {tour_selec_ameliorer.cost_upgrade
                                             }$""", True, "cyan", "black"))
                                    text_cost_lv_up_rect = (
                                        text_cost_lv_up.get_rect(
                                            midtop=(
                                                text_lv_up_tour_rect.midbottom)
                                                                )
                                                            )
                                # sert d'optimisation +
                                # le joueur ne séléctionne pas 2 tour en
                                # mm temps
                                break

            elif event.type == SPAWN_ENEMY and Systeme_Vague.running:
                # Créer un nouvel ennemi
                Systeme_Vague.update_vague()
                if (Systeme_Vague.compteur_vague_tick >
                   3 * Systeme_Vague.numero_vague and len(groupe_enemie) == 0):
                    Systeme_Vague.running = False
                    Systeme_Vague.stop_vague()

        # Mise à jour
        groupe_enemie.update()
        groupe_balle.update()
        groupe_tour.update()
        argent_joueur.update()
        Vie_joueur.update()

        affichage_gen()

    pygame.display.update()
    clock.tick(frame_rate)  # Limite à 60 FPS

"""
a faire
    faire une fonction qui tire avec la classe Tour
        les balles despagnes si elles ne  sont pas contenue dans l'écran,
          vérifier si une grande balle despawn quand une petite partie de sa
          hitbox sort de l'écran ou quand l'entéirter de sa hitbox sort
        régler le pb qu'on ne voit pas les balles des fois
          (faire en sorte qu'elle despawn
          un peu après leur touche de l'ennemie)
        régler le pb que si les balles vont trop vite,
          elle ne passent jamais au dessus d'un ennemie
            peut être avec une line de pygame qui ferais la taille de la
            distance parcourus par la balle puis on vérifie si elle overlap ??

    changer le texte du mode améliorer par ce que la c'est vrm moche
    mettre tour les bouton dans la classe bouton et l'adapter pour changer
      le paramètre vague en cours en un booléen afficher (oui / non)
    faire plus de ficher comme le spec tour pour plus tard pouvoir utiliser
      sql a la place
    mettre les lien des tours dans le ficher spec tour et toutes les infos
      relative aux tours
    faire un meilleur message pour que le joueur sache quand il n'a plus
      d'argent
    idée :
        enlever le limite à 60 fps et calculer tout les déplacement avec un
          fonction qui regarde cb de temps depuis la dernière fram et qui
          avance les ennemies en conséquence
        pb : assez dur a coder, il faut faire gaffe
          a ce que tout marche comme avant.
        """
