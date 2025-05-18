import pygame
import math
from spec import stat_tour, stat_balle, stat_ennemie, vague_predefinie

# Initialisation
pygame.init()
pygame.display.set_caption("V1 Tower Defense")
clock = pygame.time.Clock()
pause = False
son = True

#screen
screen_longeur = 1600
screen_hauteur = 900
screen = pygame.display.set_mode((screen_longeur, screen_hauteur))  # Résolution officielle

#map
map_image = pygame.image.load("map/map.png").convert()
map_rect = map_image.get_rect(topleft = (0, 0))
background_planks = pygame.image.load("assets/background/planks_background.jpg").convert()

#image ennemie
ennemi_escargot_image = (pygame.image.load("assets/enemi/escargot.png").convert_alpha(), pygame.image.load("assets/enemi/escargot_toucher.png").convert_alpha())
ennemi_poulet_image = (pygame.image.load("assets/enemi/poulet.png").convert_alpha(), pygame.image.load("assets/enemi/poulet_toucher.png").convert_alpha())
ennemi_bee_image = (pygame.image.load("assets/enemi/bee.png").convert_alpha(), pygame.image.load("assets/enemi/bee_toucher.png").convert_alpha())
ennemi_ours_image = (pygame.image.load("assets/enemi/ours.png").convert_alpha(), pygame.image.load("assets/enemi/ours_toucher.png").convert_alpha())
ennemi_rhino_image = (pygame.image.load("assets/enemi/rhino.png").convert_alpha(), pygame.image.load("assets/enemi/rinho_toucher.png").convert_alpha())
ennemie_oiseau_image = ((pygame.image.load("assets/enemi/oiseau_1.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_2.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_3.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_4.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_5.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_6.png").convert_alpha()),
                        (pygame.image.load("assets/enemi/oiseau_toucher_1.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_toucher_2.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_toucher_3.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_toucher_4.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_toucher_5.png").convert_alpha(),
                        pygame.image.load("assets/enemi/oiseau_toucher_6.png").convert_alpha()))
#background image
background_v1 = pygame.image.load("assets/tour/background_v1.png").convert()


#son
son_vente_tour = pygame.mixer.Sound("assets/sound/son_vente_tour.mp3")
son_refus = pygame.mixer.Sound("assets/sound/erreur.mp3")
son_tour_placer = pygame.mixer.Sound("assets/sound/placement_tour.mp3")
son_tire = pygame.mixer.Sound("assets/sound/tour_tire.mp3")
son_cannon = pygame.mixer.Sound("assets/sound/cannon_tire.mp3")
son_liste = (son_tire, son_cannon)
#icone
vie_image = pygame.image.load("assets/button/coeur.png").convert_alpha()

#boutton
boutton_vendre_tour_image = pygame.image.load("assets/button/vendre_la_tour.png").convert_alpha() 
boutton_setting_image = pygame.image.load("assets/button/setting.png").convert_alpha()
boutton_play_image = pygame.image.load("assets/button/boutton_jouer.png").convert_alpha()
bouton_valider_image = pygame.image.load("assets/button/valider.png").convert_alpha()
boutton_son_on_image = pygame.image.load("assets/button/son.png").convert_alpha()
boutton_son_off_image = pygame.image.load("assets/button/muet.png").convert_alpha()
son_image = boutton_son_on_image if son else boutton_son_off_image

ecran_noir_opaque = pygame.Surface((1600, 900)).convert()
ecran_noir_opaque.fill((0, 0, 0))
ecran_noir_opaque.set_alpha(128)

ecran_rouge_opaque = pygame.Surface((1600, 900)).convert()
ecran_rouge_opaque.fill((255, 0, 0))
ecran_rouge_opaque.set_alpha(60)

bouton_exit_placer = pygame.image.load("assets/button/croix_fermer.png").convert_alpha()
bouton_exit_placer_rect = bouton_exit_placer.get_rect(bottomleft = (map_rect.right, screen_hauteur))

#chemin
chemin_vecteur_general = [("x", 197), ("y", -237), ("x", 244), ("y", 311), ("x", 316), ("y", -151), ("x", 442)]

#event
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1000)

#font
font = pygame.font.Font(None, 130)
font_prix = pygame.font.Font(None, 75)
font_amiliorer = pygame.font.Font(None, 39)

#Tour :
    #image améliorer tout
text_amiloorer_tour = font_amiliorer.render("voulez vous améliorer la tour ?", True, "cyan", "black")
text_amiloorer_tour_rect = text_amiloorer_tour.get_rect(midtop = (1400, 605))
text_amiliorer_nv_max = font_amiliorer.render("Tour niveau max", True, "cyan", "black")
text_amiliorer_nv_max_rect = text_amiliorer_nv_max.get_rect(midtop = (1400, 605))

    #image Tour
load_tour = [pygame.image.load("assets/tour/tour_1_lv1.png").convert_alpha(),
            pygame.image.load("assets/tour/tour_2_rouge.png").convert_alpha(),
            pygame.image.load("assets/tour/tour_3_lv1.png").convert_alpha(),
            pygame.image.load("assets/tour/tour_1_lv1.png").convert_alpha(),
            pygame.image.load("assets/tour/tour_1_lv1.png").convert_alpha(),
            pygame.image.load("assets/tour/tour_1_lv1.png").convert_alpha()]
liste_tour = [(tour, tour.get_rect(topleft = (0, 0))) for tour in load_tour]

liste_upgrade = (
    (pygame.image.load("assets/tour/tour_1_lv2.png").convert_alpha(), pygame.image.load("assets/tour/tour_1_lv3.png").convert_alpha()),
    (pygame.image.load("assets/tour/tour_2_rouge_lv2.png").convert_alpha(), pygame.image.load("assets/tour/tour_2_rouge_lv3.png").convert_alpha()),
    (pygame.image.load("assets/tour/tour_3_lv2.png").convert_alpha(), pygame.image.load("assets/tour/tour_3_lv3.png").convert_alpha()),
    (pygame.image.load("assets/tour/tour_1_lv2.png").convert_alpha(), pygame.image.load("assets/tour/tour_1_lv3.png").convert_alpha()),
    (pygame.image.load("assets/tour/tour_1_lv2.png").convert_alpha(), pygame.image.load("assets/tour/tour_1_lv3.png").convert_alpha()),
    (pygame.image.load("assets/tour/tour_1_lv2.png").convert_alpha(), pygame.image.load("assets/tour/tour_1_lv3.png").convert_alpha()))

border = pygame.image.load("assets/tour/border.png").convert_alpha()
border_rect = border.get_rect(topright = (screen_longeur, 0))

description = (pygame.image.load("assets/description_tour/description_tour_1.png").convert(),
               pygame.image.load("assets/description_tour/description_tour_2.png").convert(),
               pygame.image.load("assets/description_tour/description_tour_3.png").convert(),
               pygame.image.load("assets/description_tour/description_tour_4.png").convert(),
               pygame.image.load("assets/description_tour/description_tour_5.png").convert(),
               pygame.image.load("assets/description_tour/description_tour_6.png").convert(),
               )


liste_tour_prix = [300, 500, 500] #300, 300, 300 #reste des prix pour les tours non défini 
if len(liste_tour_prix) <= len(liste_tour): liste_tour_prix += ([-1] * (len(liste_tour) - len(liste_tour_prix))) #si j'ai oublier de mettre un prix pour une tour, ajoute des -1 a la liste pour que il n'y ai pas d'erreure dans le scripte

#balles
vitesse_balle = (20, 20, 8, 20, 20, 20)
liste_image_balle = (pygame.image.load("assets/balle/balle_1.png").convert_alpha(),
                     pygame.image.load("assets/balle/balle_2.png").convert_alpha(),
                     pygame.image.load("assets/balle/balle_3.png").convert_alpha())

explosion = (pygame.image.load("assets/balle/explosion_1.png").convert_alpha(),
             pygame.image.load("assets/balle/explosion_2.png").convert_alpha(),
             pygame.image.load("assets/balle/explosion_3.png").convert_alpha(),
             pygame.image.load("assets/balle/explosion_4.png").convert_alpha(),
             pygame.image.load("assets/balle/explosion_5.png").convert_alpha(),
             pygame.image.load("assets/balle/explosion_6.png").convert_alpha(),
             pygame.image.load("assets/balle/explosion_7.png").convert_alpha())


#divers
mouse_tour_rect = pygame.Rect(0, 0, 75, 75) #cette variable sert a ce qu'il n'y ai pas d'erreur a cause d'une variable par défini, une fois dans la boucle, elle est update en temps réel. 
setting_rect = pygame.Rect((300, 200, 600, 400))

#hitbox chemin + point pour ennemie
liste_point_chemin = ((0, 410, 230, 465), (170, 170, 230, 465), (170, 170, 455, 230), (410, 170, 470, 550), (410, 480, 790, 550), (730, 330, 790, 550), (730, 330, 1200, 390))
hitbox_chemin = [pygame.Rect(x1, y1, x2 - x1, y2 - y1) for x1, y1, x2, y2 in liste_point_chemin]
point_ennemie = ((200, 440), (200, 200), (440, 200), (440, 515), (760, 515), (760, 360), (1200, 360))

class Enemi(pygame.sprite.Sprite):
    def __init__(self, index_ennemie, image):
        super().__init__()
        self.speed, self.vie, self.damage, self.animation = stat_ennemie[index_ennemie]
        self.image = image  #self.image prend la liste de toutes les iamges et après dans la fonction afficher(), la bonne est afficher
        if self.animation : self.rect = self.image[0][0].get_rect(center = (0, 440)) #dans le cas ou l'image a des animation, la premire image est dans la deuxième liste
        else: self.rect = self.image[0].get_rect(center = (0, 440))
        self.index_point = 0 #le point vers lequelle l'ennemie se dirige
        self.distance = 0 #est ce que l'ennemie est loin ou pas sur la map ( pour viser avec les tours)
        self.toucher = 0 #permet de compter le nb de frame pour que l'ennelie soit toucher 
        self.compteur = 0 #un compteur qui permet de savoir sur quelle image est le joueur

    def update(self):
        x, y = self.rect.center
        if abs(x - point_ennemie[self.index_point][0]) < self.speed: #si la valeur abs est plus petit que la vitesse alors on met la pos a la destination cas a la prochaine frame l'ennemie sera au pts
            x = point_ennemie[self.index_point][0] # associer la valeur de x au pt pour plus tard la mettre sur la variable slef.pos
        else: #l'ennemie est encore loin du point
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
            Vie1.enleve_vie(self.damage)
    
    def enlever_vie(self, vie):
        self.vie -= vie
        self.toucher = 7
        if self.vie <= 0:
            self.kill()
            argent_joueur.ajouter(80)
    
    def frame(self):
        self.compteur += 1
        if self.compteur // 10 >= len(self.image[0]):
                self.compteur = 0

    def afficher(self):
        if self.toucher > 0:
            self.toucher -= 1
            screen.blit(self.image[1][self.compteur // 10], self.rect) if self.animation else screen.blit(self.image[1], self.rect)
        else:
            screen.blit(self.image[0][self.compteur // 10], self.rect) if self.animation else  screen.blit(self.image[0], self.rect)
        
        if self.animation: self.frame() #sert a changer la fram pour que l'ennemie bouge

class Button():
    def __init__(self, pos, image):
        """
        classe pour les boutons, pos est un tuple de (x, y) evidemment
        """
        self.pos = pos
        self.afficher = False
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
    
    def is_overmouse(self, pos):
        return self.rect.collidepoint(pos)
    
class Vie():
    def __init__(self, vie, image):
            self.vie_initiale = vie
            self.vie = vie
            self.pos = (320, 800)
            self.image = image
            self.rect = self.image.get_rect(center=self.pos)
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
        screen.blit(self.text, (140, 800))

class Argent():
    def __init__(self, argent):
            self.rendu = False
            self.pos = (850, 810)
            self.argent = argent
            self.text = font.render(f"{self.argent}$", True, "black")
            self.tick_clignotment = 0
            self.couleur = "black"

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
            if int(self.tick_clignotment // 10)%2 == 0:
                self.couleur = "black"
                self.rendu = True
            else:
                self.rendu = True
                self.couleur = "red"
            self.tick_clignotment -= 1

        if self.rendu == True:
            self.text = font.render(f"{self.argent}$", True, self.couleur)
            self.rendu = False

    def afficher(self):
        screen.blit(self.text, self.pos)
    

class Vagues():
    def __init__(self):
        self.numero_vague = 0
        self.running = False
        self.compteur_vague_tick = 0
        self.text_vague = font.render("Vague 0", True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(center = (600, 850))

    def prochaine_vague(self):
        self.numero_vague += 1
        self.running = True
        if self.numero_vague <= 30:
            self.ennemis_a_spawn = vague_predefinie[self.numero_vague-1]
        
        self.text_vague = font.render(f"Vague {self.numero_vague}", True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(center= (600, 850))
        self.numero_chaine, self.ennemis_spawn_de_la_chaine = 0, 0
    
    def update_vague(self):
        self.compteur_vague_tick += 1 #vrais ticks (de vague), initialisé à 0
        pygame.time.set_timer(SPAWN_ENEMY, self.ennemis_a_spawn[self.numero_chaine][2])
        if self.ennemis_spawn_de_la_chaine < self.ennemis_a_spawn[self.numero_chaine][1]: #si le nombre d'ennemis deja spawn de la chaine est inférieur à celui prévu:
            if self.ennemis_a_spawn[self.numero_chaine][0] == "escargot":
                groupe_enemie.add(Enemi(0, image = ennemi_escargot_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "poulet":
                groupe_enemie.add(Enemi(1, image = ennemi_poulet_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "bee":
                groupe_enemie.add(Enemi(2, image = ennemi_bee_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "bear":
                groupe_enemie.add(Enemi(3, image = ennemi_ours_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "rhino":
                groupe_enemie.add(Enemi(4, image = enemi_rhino_image))
            elif self.ennemis_a_spawn[self.numero_chaine][0] == "oiseau":
                groupe_enemie.add(Enemi(5, image = ennemie_oiseau_image))
            self.ennemis_spawn_de_la_chaine += 1
        elif len(self.ennemis_a_spawn)-1 > self.numero_chaine:
            self.numero_chaine += 1
            self.ennemis_spawn_de_la_chaine = 0
        
    def stop_vague(self):
        self.compteur_vague_tick = 0      

class Tour(pygame.sprite.Sprite):
    """
    cette class contien tout les tour avec leur emplacement sur le terrain, elle notament a fair apparaitre les tours sur le terrain et gerer leur fonctionnement (tire, ect)
    """
    def __init__(self, position, nb_tour = 0):
        super().__init__()
        self.cooldown, self.range, self.traverse, self.effect, self.degat, self.index_balle, self.cost_upgrade, self.son = stat_tour[nb_tour][0]
        
        self.index_tour = nb_tour
        self.ennemie = None #sert a savoir si un enemie est viser ou non
        self.angle = 0
        self.tick_depuis_dernier_tire = 0
        self.niveau = 1
        self.image_upgrade = liste_upgrade[nb_tour]
        self.image_load = liste_tour[nb_tour][0] #image associer a la tour
        self.image = self.image_load
        self.rect = self.image_load.get_rect(center = (position)) #rect qui sert de hitbow a la tour
        self.rect_image_affichage = self.rect
        self.position = position
        self.rayon = self.rect.w//2 #avec 4, on peut créer un cercle avec ce rayon et avoir la même taille.

    def upgrade(self):
        self.niveau += 1
        argent_joueur.retirer(self.cost_upgrade)
        self.image = self.image_upgrade[self.niveau - 2]
        self.image_load = self.image
        self.rect_image_affichage = self.image.get_rect(center = (self.position))
        self.cooldown, self.range, self.traverse, self.effect, self.degat, self.index_balle, self.cost_upgrade, self.son = stat_tour[self.index_tour][self.niveau - 1]

    def viser(self):
        if not self.ennemie in groupe_enemie: #version pas opti mais qui marche
            self.ennemie = None
        tampon_ennemie = None
        for ennemie in groupe_enemie:
            distance = math.sqrt(((self.rect.centerx - ennemie.rect.centerx)**2) + ((self.rect.centery - ennemie.rect.centery)**2))
            if distance <= self.range:
                if tampon_ennemie == None or ennemie.distance > tampon_ennemie.distance:
                    tampon_ennemie = ennemie       

        if tampon_ennemie != None:
            self.ennemie = tampon_ennemie
        else:
            self.ennemie = None
        if self.ennemie != None: #ne pas mettre de else a la place du if car si le self.enemie est définie dans la boucle du dessus, il faut qu'on puisse rentrer dans cette boucle
            self.angle = math.atan2(self.ennemie.rect.centery - self.rect.centery, self.ennemie.rect.centerx - self.rect.centerx) #formule qui calcule l'angle (counterclaockwize)
            deg = -math.degrees(self.angle)
            self.image = pygame.transform.rotate(self.image_load, deg)
            self.rect_image_affichage = self.image.get_rect(center = (self.position))

    def tirer(self):
        if self.tick_depuis_dernier_tire >= self.cooldown:
            if self.ennemie != None:
                groupe_balle.add(Balle_tour(self.index_balle, self.rect.center, self.angle))
                if son: son_liste[self.son].play()
                self.tick_depuis_dernier_tire = 0
        else:
            self.tick_depuis_dernier_tire += 1

    def update(self):
        self.viser()
        self.tirer()

    def afficher(self):
        #pygame.draw.rect(screen, 'red', self.rect_image_affichage)
        #pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(self.image, self.rect_image_affichage)

class Balle_tour(pygame.sprite.Sprite):
    def __init__(self, index_balle, position, angle : float):
        super().__init__()
        #self.zone = False si la tour ne fait pas de dégats de zone ou la range des dégat dans le cas contraire
        self.degat_balle, self.speed, self.zone, self.image = stat_balle[index_balle] #self.image = index de l'image dans la liste, c'est le cas uniquement dans la fonction init
        self.image = pygame.transform.rotate(liste_image_balle[self.image], -math.degrees(angle)) 
        self.direction_x, self.direction_y = math.cos(angle), math.sin(angle)  #direction vers la quelle la balle ce dirige a chaque
        self.pos = list(position)
        self.rect = self.image.get_rect(center = position)
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
                        if math.sqrt((self.pos[0] - ennemie_zone.rect.centerx)**2 + (self.pos[1] - ennemie_zone.rect.centery)**2) <= self.zone:
                            ennemie_zone.enlever_vie(self.degat_balle)
                    self.en_vie = False
                    self.animation = 0
                    self.image = explosion[0]
                    self.rect = self.image.get_rect(center = self.pos)
                
                else:
                    ennemie.enlever_vie(self.degat_balle) #plus tard, changer le 1 avec les dégat de la tour qui a enlever la vie
                    self.kill()
                break #fait en sorte que la balle touche un seul ennemie
    
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
        self.image = pygame.transform.scale_by(liste_tour[tour_index][0], 180/self.taille_reel)
        self.prix = liste_tour_prix[tour_index]
        self.rect = pygame.Rect(map_rect.right + 200 * ((tour_index)%2), (200 * (tour_index // 2)), 200, 200)
        self.rayon = self.taille_reel//2 #avec 4, on peut créer un cercle avec ce rayon et avoir la même taille.
        self.prix = font_prix.render(f"{liste_tour_prix[tour_index]}$", True, (0, 255, 255))
        self.description = description[tour_index]

    def ajouter_tour(self, position):
        # en vrai ça serait bien de mettre une vérif qui dit que je peux pas placer une tour si il y en a deja une
        # mais ca sert a rien par ce que dans le scripte on vérifie déja ca donc ca serait redondant 
        groupe_tour.add(Tour(position, self.tour_index))
    
    def afficher(self):
        "permet d'avoir un meilleur controle sur l'affichage des tours, avec le background et le reste"
        pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(background_v1, self.rect)
        screen.blit(self.image, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(self.prix, (self.rect.left + 10, self.rect.bottom - 50))

boutton_play = Button((10, 800), boutton_play_image) #bouton pour lancer une vague
boutton_setting = Button((1125, 10), boutton_setting_image) #bouton pour aller dans les paramètres
boutton_ameliorer_valider = Button((1250, 675), bouton_valider_image)
boutton_ameliorer_annuler = Button((1400, 675), bouton_exit_placer)
boutton_son = boutton_son_on_image.get_rect(topleft = (350, 250))
boutton_vendre_la_tour = Button((1200, 800), boutton_vendre_tour_image) 

Vie1 = Vie(100, vie_image) #classe pour gérer la vie
argent_joueur = Argent(5000)# classe qui défini l'argent du joueur
Systeme_Vague = Vagues() #classe pour gérer le système de vague
hud = pygame.sprite.Group() #group pour gérer le hud de tour
groupe_enemie = pygame.sprite.Group() # Groupe d'ennemis
groupe_tour = pygame.sprite.Group() #groupe avec les tour
groupe_balle = pygame.sprite.Group() #groupe avec les balles
for i in range(len(liste_tour)): hud.add(Hud_tour(i))

def gestion_affichage_mode_placement():
    """cette fonction gérer le dessous du curseur dans le joeur est de le mode placement de tour""" 
    if mode_placement:
        screen.blit(bouton_exit_placer, (bouton_exit_placer_rect))
        screen.blit(Tour_selectioner_placement.image, (screen_longeur-190, screen_hauteur-190))
        
        if map_rect.contains(mouse_tour_rect):
            if not any(bout_de_chemin.colliderect(mouse_tour_rect) for bout_de_chemin in hitbox_chemin) and not any(math.sqrt((mouse_pos[0] - une_tour.rect.centerx)**2 + (mouse_pos[1] - une_tour.rect.centery)**2) <= (une_tour.rayon + mouse_tour_rayon -5) for une_tour in groupe_tour):
                    pygame.draw.rect(screen, "green", mouse_tour_rect)
                    screen.blit(liste_tour[Tour_selectioner_placement.tour_index][0], (mouse_pos[0] - (Tour_selectioner_placement.taille_reel//2), mouse_pos[1] - (Tour_selectioner_placement.taille_reel//2)))
            else:
                pygame.draw.rect(screen, "black", (mouse_tour_rect))
                screen.blit(liste_tour[Tour_selectioner_placement.tour_index][0], (mouse_pos[0] - (Tour_selectioner_placement.taille_reel//2), mouse_pos[1] - (Tour_selectioner_placement.taille_reel//2)))

def entrer_mode_placement(tour_input):
    """
    ce scripte sert a ce que cette partie du code ne soit pas copier coller plusieur fois mais plutôt regrouper dans un seul scripte
    Input : Element de la classe Hud_tour dans le groupe pygame.srrite.Groupe hud.
    Output : None
    fait rentrer le jeu dans le mode placement avec la tour selectionner en input
    """
    global mode_placement, Tour_selectioner_placement, mouse_tour_rect, mouse_tour_rayon
    mode_placement = True
    Tour_selectioner_placement = tour_input
    #le - tour_input.rayon sert a ce que le sprite ne soit pas placer a la mauvaise frame sans avoir a utiliser un .center car la calsse n'est pas encore défini, il faudrais peut être regarder si une solution plus opti est possible dans le future
    mouse_tour_rect = pygame.Rect((mouse_pos[0] - tour_input.rayon, mouse_pos[1] - tour_input.rayon), liste_tour[Tour_selectioner_placement.tour_index][1].size)
    mouse_tour_rayon = Tour_selectioner_placement.rayon
    
# Boucle principale
running = True
mode_placement = False
mode_ameliorer = False
while running:
    mouse_pos = pygame.mouse.get_pos()
    if pause:
        surface_sans_srcalpha = pygame.Surface((200, 200))
        surface_sans_srcalpha.fill((0, 0, 255))  # Bleu opaque

        # Appliquer une transparence globale (0 = invisible, 255 = opaque)
        surface_sans_srcalpha.set_alpha(128)  # Semi-transparent

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #evente qui permet de quiter le jeu
                running = False
            
            elif event.type == pygame.KEYDOWN: #event pour détecter les touches du clavier appuyer
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    pause = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN: #event pour détecter les clique de la souris
                if event.button == 1:
                    if not setting_rect.collidepoint(mouse_pos):
                        pause = False
                    elif boutton_son.collidepoint(mouse_pos):
                        if son == True:
                            son = False
                            son_image = boutton_son_off_image
                        else:
                            son = True
                            son_image = boutton_son_on_image
        #affichage habituelle:
        screen.fill("yellow") #fond jaune
        screen.blit(map_image, (0, 0)) #map
        if not Systeme_Vague.running: screen.blit(boutton_play.image, boutton_play.pos)
        screen.blit(Systeme_Vague.text_vague, Systeme_Vague.rect_text_vague) 
        Vie1.afficher()
        argent_joueur.afficher()
        screen.blit(boutton_setting.image, boutton_setting.pos)
        for ennemie in groupe_enemie: ennemie.afficher()
        for tour in groupe_tour: tour.afficher()
        for balle in groupe_balle: balle.afficher()
        for élément in hud: élément.afficher()
        screen.blit(ecran_noir_opaque, (0, 0)) #perrmet d'avoir un fond noircis pour que le joueur comprenne qu'il est dans une autres fenêtre
        pygame.draw.rect(screen, "white", (300, 200, 600, 400)) #fond qui sert de menu pause
        pygame.draw.rect(screen, "black",(310, 210, 580, 380))
        screen.blit(son_image, boutton_son)
        #pygame.draw.rect(screen, 'red', setting_rect)

    else: #boucle normal, dans le cas ou le jeu n'est pas en pause
        mouse_pos = pygame.mouse.get_pos()
        mouse_tour_rect.center = mouse_pos
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #evente qui permet de quiter le jeu
                running = False

            elif event.type == pygame.KEYDOWN: #event pour détecter les touches du clavier appuyer
                if event.key == pygame.K_ESCAPE:
                    if not (mode_placement or mode_ameliorer):
                        pause = True
                    else:
                        mode_placement = False
                        mode_ameliorer = False
                if event.key == pygame.K_1: #Créer un nouvel ennemi #escargot
                    groupe_enemie.add(Enemi(0, image = ennemi_escargot_image))
                elif event.key == pygame.K_2:#poulet
                    groupe_enemie.add(Enemi(1, image = ennemi_poulet_image))
                elif event.key == pygame.K_3:#bee
                    groupe_enemie.add(Enemi(2, image = ennemi_bee_image))
                elif event.key == pygame.K_4:#bear
                    groupe_enemie.add(Enemi(3, image = ennemi_ours_image))
                elif event.key == pygame.K_5:#rhino
                    groupe_enemie.add(Enemi(4, image = ennemi_rhino_image))
                elif event.key == pygame.K_6: #oiseau
                    groupe_enemie.add(Enemi(5, image = ennemie_oiseau_image))
                #pour que le joueur puisse selectioner une tour avec son clavier
                elif event.key == pygame.K_a:
                    mode_ameliorer = False
                    if argent_joueur.argent >= liste_tour_prix[0]:
                        entrer_mode_placement(hud.sprites()[0])
                    else:
                        if son: son_refus.play()
                        argent_joueur.clignotement()
                
                elif event.key == pygame.K_z:
                    mode_ameliorer = False
                    if argent_joueur.argent >= liste_tour_prix[1]:
                        entrer_mode_placement(hud.sprites()[1])
                    else:
                        if son: son_refus.play()
                        argent_joueur.clignotement()
            
                elif event.key == pygame.K_e:
                    mode_ameliorer = False
                    if argent_joueur.argent >= liste_tour_prix[2]:
                        entrer_mode_placement(hud.sprites()[2])
                    else:
                        if son: son_refus.play()
                        argent_joueur.clignotement()

            elif event.type == pygame.MOUSEBUTTONDOWN: #event pour détecter les clique de la souris
                if event.button == 1: #si le joueur fait un clique gauche
                    #print(mouse_pos)
                    if boutton_setting.is_overmouse(mouse_pos) and not mode_placement:
                        pause = True

                    elif boutton_play.is_overmouse(mouse_pos): #event pour detécter si la souris est sur le bouton
                        if not Systeme_Vague.running:
                            Systeme_Vague.prochaine_vague()
                
                    elif bouton_exit_placer_rect.collidepoint(mouse_pos):
                        mode_placement = False
                #gestion des tours
                #cette parti gère le joueur si il veux rentrer dans le mode placement
                    for icone_tour in hud:
                        if icone_tour.rect.collidepoint(mouse_pos):
                            if mode_ameliorer: mode_ameliorer = False
                            if argent_joueur.argent >= liste_tour_prix[icone_tour.tour_index]:
                                entrer_mode_placement(icone_tour)
                            else:
                                if son: son_refus.play()
                                argent_joueur.clignotement()

                    if mode_placement == True: #est activé si le joueur est dans le mode placement de tour
                        if map_rect.contains(mouse_tour_rect): #verifier si les coordoner sont dans l'écran
                            if not any(bout_de_chemin.colliderect(mouse_tour_rect) for bout_de_chemin in hitbox_chemin):#est ce que le curseur est sur le chemin ?
                                if not any(math.sqrt((mouse_pos[0] - une_tour.rect.centerx)**2 + (mouse_pos[1] - une_tour.rect.centery)**2) <= (une_tour.rayon + mouse_tour_rayon - 5) for une_tour in groupe_tour):
                                    #le -5 est pour une marge et que le jeu ne soit pas trop frustrant pour le joueur)                               
                                    mode_placement = False
                                    if son: son_tour_placer.play()
                                    Tour_selectioner_placement.ajouter_tour(mouse_pos)
                                    argent_joueur.retirer(liste_tour_prix[Tour_selectioner_placement.tour_index])
                    else:
                        if mode_ameliorer: #si mode placment == False mais le joueur est dans le mode améliorer
                            if boutton_ameliorer_valider.is_overmouse(mouse_pos):
                                if tour_selectioner_ameliorer.niveau < 3:
                                    if argent_joueur.argent >= tour_selectioner_ameliorer.cost_upgrade:
                                        tour_selectioner_ameliorer.upgrade()
                                    else:
                                        if son: son_refus.play()
                                        argent_joueur.clignotement()
                                        
                            elif boutton_vendre_la_tour.is_overmouse(mouse_pos):
                                tour_selectioner_ameliorer.kill()                        
                                rendre = liste_tour_prix[tour_selectioner_ameliorer.index_tour]
                                for i in range(tour_selectioner_ameliorer.niveau - 1): # a lv 1 ont n'a pas upgrade la tour
                                    rendre += stat_tour[tour_selectioner_ameliorer.index_tour][i][6]
                                argent_joueur.ajouter(rendre // 2 )
                                if son: son_vente_tour.play()
                            mode_ameliorer = False
                            
                        #mode placement == False -> fonction qui clique sur une tour et qui regarde + le joueur n'est pas dans le mode amiliorer
                        for une_tour in groupe_tour:
                            if math.sqrt((mouse_pos[0] - une_tour.rect.centerx)**2 + (mouse_pos[1] - une_tour.rect.centery)**2 )<= une_tour.rayon:
                                tour_selectioner_ameliorer = une_tour
                                mode_ameliorer = True
                                if tour_selectioner_ameliorer.niveau < 3:
                                    text_cout_amelioration = font_amiliorer.render(f"coût amélioration : {tour_selectioner_ameliorer.cost_upgrade} $", True, "cyan", "black")
                                    text_cout_amelioration_rect =  text_cout_amelioration.get_rect(midtop = (text_amiloorer_tour_rect.midbottom))
                                break #sert d'optimisation + le joueur ne séléctionne pas 2 tour en m^ temps

            elif event.type == SPAWN_ENEMY and Systeme_Vague.running:
                # Créer un nouvel ennemi
                Systeme_Vague.update_vague()
                if Systeme_Vague.compteur_vague_tick > 3*Systeme_Vague.numero_vague and len(groupe_enemie) == 0:
                    Systeme_Vague.running = False
                    Systeme_Vague.stop_vague()

        # Mise à jour
        groupe_enemie.update()
        groupe_balle.update()
        groupe_tour.update()
        argent_joueur.update()
        Vie1.update()

        #Affichage
        screen.fill("yellow") #fond jaune
        screen.blit(map_image, (0, 0)) #map
        if not mode_ameliorer and not mode_placement:    
            for tour_hud in hud:
                if tour_hud.rect.collidepoint(mouse_pos):
                    screen.blit(tour_hud.description, (1200, 600))
                    break #la souris ne peut pas être sur deux tour a la fois donc si on trouve la tour sur laquelle le joueur est ca ne sert a rien de continuer

        if not Systeme_Vague.running:
            screen.blit(boutton_play.image, boutton_play.pos)
        
        screen.blit(Systeme_Vague.text_vague, Systeme_Vague.rect_text_vague)  # Affiche le text de la vague
        gestion_affichage_mode_placement() #gestion du curseur Noir / Vert, le l'icone fermer + de la preview de la tour
        
        #affichage : faire d'abord la map et ses élément puis le hud par ce que c'est sinon les projectil peuvent overlap bref voila
        #groupe_enemie.draw(screen)
        for ennemie in groupe_enemie:
            ennemie.afficher()

        for tour in groupe_tour: #affichage des tour
            tour.afficher()

        for balle in groupe_balle:
            balle.afficher()
        
        if mode_placement:
            pygame.draw.circle(screen, "grey", mouse_pos, stat_tour[Tour_selectioner_placement.tour_index][0][1], 2)
        else: #si le joueur est dans le mode placement, alors ont affiche pas l'icone des settings pour laisser ua joueur la possiblilité de mettre un tour a cette endroit
            screen.blit(boutton_setting.image, boutton_setting.pos)#bouton setting
        
        if mode_ameliorer:
            if tour_selectioner_ameliorer.niveau < 3:
                screen.blit(text_amiloorer_tour, text_amiloorer_tour_rect)
                screen.blit(text_cout_amelioration, text_cout_amelioration_rect)
                screen.blit(boutton_ameliorer_valider.image, boutton_ameliorer_valider.pos)
                screen.blit(boutton_ameliorer_annuler.image, boutton_ameliorer_annuler)
            else:
                screen.blit(text_amiliorer_nv_max, text_amiliorer_nv_max_rect)
            screen.blit(boutton_vendre_la_tour.image, boutton_vendre_la_tour.rect)
            pygame.draw.rect(screen, "pink", tour_selectioner_ameliorer.rect)
            pygame.draw.circle(screen, "grey", tour_selectioner_ameliorer.rect.center, tour_selectioner_ameliorer.range, 2)
            tour_selectioner_ameliorer.afficher() #car sinon le carré pink recouvre la tour
        
        for élément in hud:
            élément.afficher()
        
        Vie1.afficher()
        argent_joueur.afficher()#permet d'afficher l'argnet du joueur
    
        # for i in hitbox_chemin:# pour afficher la hitbox du chemin et debuger le code
        #    pygame.draw.rect(screen, "red", i)
        
    pygame.display.update()
    clock.tick(60)  #Limite à 60 FPS

"""
a faire
    faire une fonction qui tire avec la classe Tour
        les balles despagnes si elles ne  sont pas contenue dans l'écran, vérifier si une grande balle despawn quand une petite partie de sa hitbox sort de l'écran ou quand l'entéirter de sa hitbox sort
        régler le pb qu'on ne voit pas les balles des fois (faire en sorte qu'elle despawn un peu après leur touche de l'ennemie)
        régler le pb que si les balles vont trop vite, elle ne passent jamais au dessus d'un ennemie
            peut être avec une line de pygame qui ferais la taille de la distance parcourus par la balle puis on vérifie si elle overlap ??
    
    changer le texte du mode améliorer par ce que la c'est vrm moche
    mettre tour les bouton dans la classe bouton et l'adapter pour changer le paramètre vague en cours en un booléen afficher (oui / non)
    faire plus de ficher comme le spec tour pour plus tard pouvoir utiliser sql a la place
    mettre les lien des tours dans le ficher spec tour et toutes les infos relative aux tours
    faire un meilleur message pour que le joueur sache quand il n'a plus d'argent
    idée :
        enlever le limite à 60 fps et calculer tout les déplacement avec un fonction qui regarde cb de temps depuis la dernière fram et qui avance les ennemies en conséquence
        pb : assez dur a coder, il faut faire gaffe a ce que tout marche comme avant.
        """