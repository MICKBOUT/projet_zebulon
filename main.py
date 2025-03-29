import pygame
import math
from spec_tour import stat_tour

# Initialisation
pygame.init()
pygame.display.set_caption("V1 Tower Defense")
clock = pygame.time.Clock()

#screen
screen_longeur = 1600
screen_hauteur = 900
screen = pygame.display.set_mode((screen_longeur, screen_hauteur))  # Résolution officielle

#map
map_image = pygame.image.load("map/map.png").convert()
map_rect = map_image.get_rect(topleft = (0, 0))

#image ennemie
enemi_rouge_image = pygame.image.load("enemi/enemi_rouge.png").convert_alpha()
enemi_vert_image = pygame.image.load("enemi/enemi_vert.png").convert_alpha()
enemi_bleu_image = pygame.image.load("enemi/enemi_bleu.png").convert_alpha()

#background image
background_v1 = pygame.image.load("assets/tour/background_v1.png")

#icone
bouton_play_image = pygame.image.load("assets/button/bouton-jouer.png").convert_alpha()
vie_image = pygame.image.load("assets/button/coeur.png").convert_alpha()

bouton_exit_placer = pygame.image.load("assets/button/quitter_le_mode_tour_placer.png").convert_alpha()
bouton_exit_placer_rect = bouton_exit_placer.get_rect(bottomleft = (map_rect.right, screen_hauteur))

#chemin
chemin_vecteur_general = [("x", 197), ("y", -237), ("x", 244), ("y", 311), ("x", 316), ("y", -151), ("x", 442)]

#event
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1000)

#font
font = pygame.font.Font(None, 130)
font_prix = pygame.font.Font(None, 75)

load_tour = [ 
    pygame.image.load("assets/tour/tour_test_v1.png").convert_alpha(),
    pygame.image.load("assets/tour/tour_2_rouge.png").convert_alpha()]
liste_tour = [(tour, tour.get_rect(topleft = (0, 0))) for tour in load_tour]

liste_tour_prix = [300, 500]
if len(liste_tour_prix) <= len(liste_tour): liste_tour_prix += ([-1] * (len(liste_tour) - len(liste_tour_prix))) #si j'ai oublier de mettre un prix pour une tour, ajoute des -1 a la liste pour que il n'y ai pas d'erreure dans le scripte

liste_image_balle = [pygame.image.load("assets/tour/balle_1.png"),
                     pygame.image.load("assets/tour/balle_2.png")]

border = pygame.image.load("assets/tour/border.png").convert_alpha()
border_rect = border.get_rect(topright = (screen_longeur, 0))

#hitbox chemin
liste_point_chemin = ((0, 410, 230, 465), (170, 170, 230, 465), (170, 170, 455, 230), (410, 170, 470, 550), (410, 480, 790, 550), (730, 330, 790, 550), (730, 330, 1200, 390))
hitbox_chemin = [pygame.Rect(x1, y1, x2 - x1, y2 - y1) for x1, y1, x2, y2 in liste_point_chemin]


class Enemi(pygame.sprite.Sprite):
    def __init__(self, pos, speed, vie, damage, image):
        super().__init__()
        self.chemin_vecteur = []
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.vie = vie
        self.indice_chemin = 0
        self.compteur = 0
        self.speed = speed
        self.damage = damage
        for vecteur in chemin_vecteur_general:
            self.chemin_vecteur += [(vecteur[0], vecteur[1]-vecteur[1]%self.speed)]

    def update(self):
        if self.compteur == self.chemin_vecteur[self.indice_chemin][1]:
                if self.indice_chemin != len(self.chemin_vecteur)-1:
                    self.compteur = 0
                    self.indice_chemin += 1
                else:
                    self.kill()
                    Vie1.enleve_vie(self.damage)
        else:
            if self.chemin_vecteur[self.indice_chemin][0] == "x":
                if self.chemin_vecteur[self.indice_chemin][1] > 0:
                    self.compteur += self.speed
                    self.rect.x += self.speed
                else:
                    self.compteur -= self.speed
                    self.rect.x -= self.speed
            else:
                if self.chemin_vecteur[self.indice_chemin][1] > 0:
                    self.compteur += self.speed
                    self.rect.y += self.speed
                else:
                    self.compteur -= self.speed
                    self.rect.y -= self.speed
    
    def enlever_vie(self, vie):
        self.vie -= vie
        if self.vie <= 0:
            self.kill()
            argent_joueur.ajouter(80)

class Button():
    def __init__(self, pos, image):
        """
        classe pour les boutons, pos est un tuple de (x, y) evidemment
        """
        self.pos = pos
        self.manche_en_cours = False
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
            
    def ajoute_vie(self, n):
        self.vie += n

    def enleve_vie(self, n):
        self.vie -= n

    def reinitialiser_vie(self):
        self.vie = self.vie_initiale
        
    def update(self):
        text = font.render(str(self.vie), True, (150, 0, 0))
        text_rect = text.get_rect(topleft = (140, 800))
        screen.blit(self.image, self.pos)
        screen.blit(text, text_rect)

class Argent():
    def __init__(self, argent):
            self.rendu = False
            self.pos = (850, 810)
            self.argent = argent
            self.text = font.render(f"{self.argent}$", True, "black")

    def ajouter(self, n):
        self.argent += n
        self.rendu = True
    def retirer(self, n):
        self.argent -= n
        self.rendu = True
    def definir(self, n):
        self.argent = n
        self.rendu = True
    
    def update(self):
        if self.rendu == True:
            self.text = font.render(f"{self.argent}$", True, "black")
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
        
        self.text_vague = font.render(f"Vague {self.numero_vague}", True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(center= (600, 850))
    
    def update_vague(self):
        self.compteur_vague_tick += 1
        if self.compteur_vague_tick < self.numero_vague:
            Enemi_bleu = Enemi(pos=(0, 434), speed=3, vie= 100, damage=3, image=enemi_bleu_image)
            groupe_enemie.add(Enemi_bleu)
        if self.compteur_vague_tick < self.numero_vague*2:
            Enemi_vert = Enemi(pos=(0, 434), speed=2, vie= 100, damage=2, image=enemi_vert_image)
            groupe_enemie.add(Enemi_vert)
        if self.compteur_vague_tick < self.numero_vague*3:
            Enemi_rouge = Enemi(pos=(0, 434), speed=1, vie= 100, damage=1, image=enemi_rouge_image)
            groupe_enemie.add(Enemi_rouge)
        #print(self.compteur_vague_tick)
        
    def stop_vague(self):
        self.compteur_vague_tick = 0      

class Tour(pygame.sprite.Sprite):
    """
    cette class contien tout les tour avec leur emplacement sur le terrain, elle notament a fair apparaitre les tours sur le terrain et gerer leur fonctionnement (tire, ect)
    """
    def __init__(self, position, nb_tour = 0):
        super().__init__()
        self.ennemie = None #sert a savoir si un enemie est viser ou non
        self.angle = 0
        self.tick_depuis_dernier_tire = 0
        self.cooldown, self.range, self.traverse, self.effect, self.zone, self.degat, self.index_balle = stat_tour[nb_tour]
        self.image_load = liste_tour[nb_tour][0] #image associer a la tour
        self.image = self.image_load
        self.rect = self.image_load.get_rect(center = (position)) #rect qui sert de hitbow a la tour
        self.rect_image_affichage = self.rect
        self.position = position
        self.rayon = self.rect.w//2 #avec 4, on peut créer un cercle avec ce rayon et avoir la même taille.

    def viser(self):
        if not self.ennemie in groupe_enemie:#version pas opti mais qui marche
            self.ennemie = None

        if self.ennemie == None: #si aucun énemie n'est viser
            distance_ennemie_proche = None
            for ennemie in groupe_enemie:
                distance = math.sqrt(((self.rect.centerx - ennemie.rect.centerx)**2) + ((self.rect.centery - ennemie.rect.centery)**2))
                if distance_ennemie_proche == None or distance < distance_ennemie_proche :
                    distance_ennemie_proche = distance
                    tampon_ennemie = ennemie #cette variable sert a stocker le ennemie dans la boucle le temps qu'elle se termie pour ensuite l'assigner a self.ennemie

            if distance_ennemie_proche != None and distance_ennemie_proche < self.range:
                self.ennemie = tampon_ennemie

        elif math.sqrt(((self.rect.centerx - self.ennemie.rect.centerx)**2) + ((self.rect.centery - self.ennemie.rect.centery)**2)) > self.range:
            #dans le cas ou l'ennemie est plus loin que la range, on remet la valeur self. ennemie a None pour arreter de la viser
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
                self.tick_depuis_dernier_tire = 0
        else:
            self.tick_depuis_dernier_tire += 1

    def update(self):
        self.viser()
        self.tirer()

    def affichage(self):
        #pygame.draw.rect(screen, 'red', self.rect_image_affichage)
        #pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(self.image, self.rect_image_affichage)

class Balle_tour(pygame.sprite.Sprite):
    def __init__(self, index_balle : int, position : tuple, angle : float):
        super().__init__()
        self.image = pygame.transform.rotate(liste_image_balle[index_balle], -math.degrees(angle)) 
        self.direction_x, self.direction_y = math.cos(angle), math.sin(angle)  #direction vers la quelle la balle ce dirige a chaque
        self.pos = list(position)
        self.rect = self.image.get_rect(center = position)
        
    def mouvement(self):
        self.pos[0] += self.direction_x * 20
        self.pos[1] += self.direction_y * 20
        self.rect.center = self.pos
        if not map_rect.colliderect(self.rect):
            self.kill()
    
    def collision_ennemie(self):
        for ennemie in groupe_enemie:
            if self.rect.colliderect(ennemie.rect):
                ennemie.enlever_vie(25) #plus tard, changer le 1 avec les dégat de la tour qui a enlever la vie
                self.kill()

    def update(self):
        self.mouvement()    
        self.collision_ennemie()

    def afficher(self):
        screen.blit(self.image, self.rect)   

class Hud_tour(pygame.sprite.Sprite):
    def __init__(self, tour_index):
        super().__init__()
        self.tour_index = tour_index
        self.taille_reel = liste_tour[tour_index][1].w
        self.image = pygame.transform.scale_by(liste_tour[tour_index][0], 180/self.taille_reel)
        self.prix = liste_tour_prix[tour_index]
        self.rect = self.image.get_rect(topleft = (map_rect.right + 200 * ((tour_index)%2), (200 * (tour_index // 2))))
        self.rayon = self.taille_reel//2 #avec 4, on peut créer un cercle avec ce rayon et avoir la même taille.
        self.prix = font_prix.render(f"{liste_tour_prix[tour_index]}$", True, (0, 255, 255))

    def ajouter_tour(self, position):
        # en vrai ça serait bien de mettre une vérif qui dit que je peux pas placer une tour si il y en a deja une
        # mais ca sert a rien par ce que dans le scripte on vérifie déja ca donc ca serait redondant 
        groupe_tour.add(Tour(position, self.tour_index))
    
    def afficher(self):
        "permet d'avoir un meilleur controle sur l'affichage des tours, avec le background et le reste"
        pygame.draw.rect(screen, 'black', self.rect)
        screen.blit(background_v1, self.rect)
        screen.blit(self.image, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(self.prix, (self.rect.left + 10, self.rect.bottom - 30))


#ennemie temporaire, ces valeurs ne serrons plus présente dans le scrpte finale
Enemi_rouge = Enemi(pos=(0, 434), speed=1, vie= 100, damage=1, image=enemi_rouge_image) # Créer un nouvel ennemi
Enemi_vert = Enemi(pos=(0, 434), speed=2, vie= 100, damage=2, image=enemi_vert_image)  
Enemi_bleu = Enemi(pos=(0, 434), speed=3, vie= 100, damage=1, image=enemi_bleu_image)

bouton_play = Button((50, 800), bouton_play_image) #bouton pour lancer une vague
Vie1 = Vie(100, vie_image) #classe pour gérer la vie
argent_joueur = Argent(500)
Systeme_Vague = Vagues() #classe pour gérer le système de vague
groupe_enemie = pygame.sprite.Group() # Groupe d'ennemis
groupe_tour = pygame.sprite.Group() #groupe avec les tour
groupe_balle = pygame.sprite.Group() #groupe avec les balles
hud = pygame.sprite.Group() #group pour gérer le hud de tour

for i in range(len(liste_tour)):
    hud.add(Hud_tour(i))

def gestion_affichage_mode_placement():
    """cette fonction gérer le dessous du curseur dans le joeur est de le mode placement de tour""" 
    if mode_placement:
        screen.blit(bouton_exit_placer, (bouton_exit_placer_rect))
        screen.blit(Tour_selectioner_placement.image, (screen_longeur-200, screen_hauteur-200, 200, 200))
        
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
    
    
mouse_tour_rect = pygame.Rect(0, 0, 75, 75) #cette variable sert a ce qu'il n'y ai pas d'erreur a cause d'une variable par défini, une fois dans la boucle, elle est update en temps réel. 

# Boucle principale
running = True
mode_placement = False
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_tour_rect.center = mouse_pos
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #evente qui permet de quiter le jeu
            running = False

        if event.type == pygame.KEYDOWN: #event pour détecter les touches du clavier appuyer
            if event.key == pygame.K_1: #Créer un nouvel ennemi
                groupe_enemie.add(Enemi_rouge)
            if event.key == pygame.K_2:
                groupe_enemie.add(Enemi_vert)
            if event.key == pygame.K_3:
                groupe_enemie.add(Enemi_bleu)
            if event.key == pygame.K_a:
                entrer_mode_placement(hud.sprites()[0])
            if event.key == pygame.K_z:
                entrer_mode_placement(hud.sprites()[1])
                         
            if mode_placement:
                if event.key == pygame.K_ESCAPE:
                    mode_placement = False

        if event.type == pygame.MOUSEBUTTONDOWN: #event pour détecter les clique de la souris
            if event.button == 1:
                #print(mouse_pos)
                pass

            if bouton_play.is_overmouse(mouse_pos): #event pour detécter si la souris est sur le bouton
                if not Systeme_Vague.running:
                    Systeme_Vague.prochaine_vague()

            #gestion des tours
            if event.button == 1: #cette parti gère le joueur si il veux rentrer dans le mode placement
                for icone_tour in hud:
                    if icone_tour.rect.collidepoint(mouse_pos):
                       entrer_mode_placement(icone_tour)

                if mode_placement != False: #ce else est activé si le joueur est dans le mode placement de tour
                    if map_rect.contains(mouse_tour_rect): #verifier si les coordoner sont dans l'écran
                        if liste_tour_prix[Tour_selectioner_placement.tour_index] <= argent_joueur.argent:
                            if not any(bout_de_chemin.colliderect(mouse_tour_rect) for bout_de_chemin in hitbox_chemin):#est ce que le curseur est sur le chemin ?
                                if not any(math.sqrt((mouse_pos[0] - une_tour.rect.centerx)**2 + (mouse_pos[1] - une_tour.rect.centery)**2) <= (une_tour.rayon + mouse_tour_rayon - 5) for une_tour in groupe_tour):
                                    #le -5 est pour une marge et que le jeu ne soit pas trop frustrant pour le joueur)                               
                                    Tour_selectioner_placement.ajouter_tour(mouse_pos)
                                    mode_placement = False
                                    argent_joueur.retirer(liste_tour_prix[Tour_selectioner_placement.tour_index])

                        else: #dans ce cas, le joueur n'as pas assez d'argent
                            print("vous n'avez pas assez d'argent et tout et tout")
                    
                if event.button == 1:#pour sortir du mode placement de tour
                    if bouton_exit_placer_rect.collidepoint(mouse_pos):
                        mode_placement = False

        if event.type == SPAWN_ENEMY and Systeme_Vague.running:
            # Créer un nouvel ennemi
            Systeme_Vague.update_vague()
            if Systeme_Vague.compteur_vague_tick > 3*Systeme_Vague.numero_vague and len(groupe_enemie) == 0:
                Systeme_Vague.running = False
                Systeme_Vague.stop_vague()
        
        if bouton_play.is_overmouse(mouse_pos):
                pass

    # Mise à jour
    groupe_enemie.update()
    groupe_tour.update()
    groupe_balle.update()
    
    #Affichage
    screen.fill("yellow") #fond jaune
    screen.blit(map_image, (0, 0)) #map

    if not Systeme_Vague.running:
        screen.blit(bouton_play_image, bouton_play.pos)

    screen.blit(Systeme_Vague.text_vague, Systeme_Vague.rect_text_vague)  # Affiche tous les ennemis
    gestion_affichage_mode_placement() #gestion du curseur Noir / Vert, le l'icone fermer + de la preview de la tour
    argent_joueur.update()
    
    #affichage : faire d'abord la map et ses élément puis le hud par ce que c'est sinon les projectif peuvent overlap bref voila
    
    groupe_enemie.draw(screen)

    for tour in groupe_tour: #affichage des tour
        tour.affichage()

    for balle in groupe_balle:
        balle.afficher()
    
    for élément in hud:
        élément.afficher()
    
    Vie1.update()#draw la vie, + update avec les calcules
    argent_joueur.afficher()

    #for i in hitbox_chemin:# pour afficher la hitbox du chemin et debuger le code
    #    pygame.draw.rect(screen, "red", i)
    pygame.display.update()
    clock.tick(400)  #Limite à 60 FPS

"""
a faire
    chemin min()
    vie1 draw et update != 
    revoire la classe vie par ce que l'affichage est un peu bizzare est pas propre (priorité faible)

    faire une fonction qui tire avec la classe Tour
        les balles despagnes si elles ne  sont pas contenue dans l'écran, vérifier si une grande balle despawn quand une petite partie de sa hitbox sort de l'écran ou quand l'entéirter de sa hitbox sort
        
        régler le pb que si les balles vont trop vite, elle ne passent jamais au dessus d'un ennemie
            peut être avec une line de pygame qui ferais la taille de la distance parcourus par la balle puis on vérifie si elle overlap ??
    faire un meilleur message pour que le joueur sache quand il n'a plus d'argent
    restucturer le code pour que le mode_placement ne soit plus dans la fonction mouse bouton down mais a part pour une meilleur lisibilité
    class argent
    revoire le systéme de spawn, les ennemies spawn par vague a l'intérieure des vagues, il faudrais qu'ils arrivent tous en mm temps ou presque
    idée :
        enlever le limite à 60 fps et calculer tout les déplacement avec un fonction qui regarde cb de temps depuis la dernière fram et qui avance les ennemies en conséquence
        pb : assez dur a coder, il faut faire gaffe a ce que tout marche comme avant.
        """