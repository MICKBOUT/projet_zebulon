import pygame
import time

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
    pygame.image.load("assets/tour/tour_2_rouge.png").convert_alpha(),]

liste_tour = [(tour, tour.get_rect(topleft = (0, 0))) for tour in load_tour]
liste_tour_prix = [300, 500]
if len(liste_tour_prix) <= len(liste_tour): liste_tour_prix += ([-1] * (len(liste_tour) - len(liste_tour_prix))) #si j'ai oublier de mettre un prix pour une tour, ajoute des -1 a la liste pour que il n'y ai pas d'erreure dans le scripte

border = pygame.image.load("assets/tour/border.png").convert_alpha()
border_rect = border.get_rect(topright = (screen_longeur, 0))

#hitbox chemin
liste_point_chemin = ((0, 400, 240, 470), (160, 160, 240, 470), (160, 160, 480, 240), (400, 160, 480, 555), (400, 480, 800, 555), (720, 320, 800, 555), (720, 320, 1200, 400))
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
            self.pos = (400, 800)
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
        text_rect = text.get_rect(topleft = (200, 800))
        screen.blit(self.image, self.pos)
        screen.blit(text, text_rect)

class Vagues():
    def __init__(self):
        self.numero_vague = 0
        self.running = False
        self.compteur_vague_tick = 0
        self.text_vague = font.render("Vague 0", True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(center = (800, 850))
        

    def prochaine_vague(self):
        self.numero_vague += 1
        self.running = True
        
        self.text_vague = font.render(f"Vague {self.numero_vague}", True, (105, 78, 165))
        self.rect_text_vague = self.text_vague.get_rect(center= (800, 850))
    
    def update_vague(self):
        self.compteur_vague_tick += 1
        if self.compteur_vague_tick < self.numero_vague:
            Enemi_bleu = Enemi(pos=(0, 434), speed=3, vie= 100, damage=3, image=enemi_bleu_image)
            enemies.add(Enemi_bleu)
            print(enemies)
        if self.compteur_vague_tick < self.numero_vague*2:
            Enemi_vert = Enemi(pos=(0, 434), speed=2, vie= 100, damage=2, image=enemi_vert_image)
            enemies.add(Enemi_vert)
        if self.compteur_vague_tick < self.numero_vague*3:
            Enemi_rouge = Enemi(pos=(0, 434), speed=1, vie= 100, damage=1, image=enemi_rouge_image)
            enemies.add(Enemi_rouge)
        print(self.compteur_vague_tick)
        
    def stop_vague(self):
        self.compteur_vague_tick = 0      

class Tour(pygame.sprite.Sprite):
    """
    cette class contien tout les tour avec leur emplacement sur le terrain, elle notament a fair apparaitre les tours sur le terrain et gerer leur fonctionnement (tire, ect)
    """
    def __init__(self, position, nb_tour = 0):
        super().__init__()
        self.image = liste_tour[nb_tour][0]
        self.rect = self.image.get_rect(center = (position))

class Hud_tour(pygame.sprite.Sprite):
    def __init__(self, tour_index):
        super().__init__()
        self.tour_index = tour_index
        self.image = liste_tour[tour_index][0]
        self.prix = liste_tour_prix[tour_index]
        self.image = pygame.transform.scale_by(liste_tour[tour_index][0], 180/liste_tour[tour_index][1].w)
        self.rect = self.image.get_rect(topleft = (map_rect.right + 200 * ((tour_index)%2), (200 * (tour_index // 2))))
        
        self.prix = font_prix.render(f"{liste_tour_prix[tour_index]}$", True, (0, 255, 255))
    
    def ajouter_tour(self, position):
        #en vrai ça serait bien de mettre une vérif qui dit que je peux pas placer une tour si il y en a deja une
        #mais ca sert a rien par ce que dans le scripte on vérifie déja ca donc ca serait redondant 
        tour.add(Tour(position, self.tour_index))
    
    def afficher(self):
        "permet d'avoir un meilleur controle sur l'affichage des tours, avec le background et le reste"
        screen.blit(background_v1, self.rect)
        screen.blit(self.image, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(self.prix, (self.rect.left + 10, self.rect.bottom - 30))

#ennemie temporaire, ces valeurs ne serrons plus présente dans le scrpte finale
Enemi_rouge = Enemi(pos=(0, 434), speed=1, vie= 100, damage=1, image=enemi_rouge_image) # Créer un nouvel ennemi
Enemi_vert = Enemi(pos=(0, 434), speed=2, vie= 100, damage=2, image=enemi_vert_image)  
Enemi_bleu = Enemi(pos=(0, 434), speed=3, vie= 100, damage=1, image=enemi_bleu_image)

bouton_play = Button((50, 800), bouton_play_image) #bouton pour lancer une vague
Vie1 = Vie(100, vie_image) #classe pour gérer la vie
Systeme_Vague = Vagues() #classe pour gérer le système de vague
enemies = pygame.sprite.Group() # Groupe d'ennemis
tour = pygame.sprite.Group() #groupe avec les tour
hud = pygame.sprite.Group() #group pour gérer le hud de tour

for i in range(len(liste_tour)):
    hud.add(Hud_tour(i))

def gestion_affichage_mode_placement():
    if mode_placement != False:
        screen.blit(bouton_exit_placer, (bouton_exit_placer_rect))
        screen.blit(mode_placement.image, (screen_longeur-200, screen_hauteur-200, 200, 200))
        
        if map_rect.contains(mouse_tour_rect):
            if not any(une_tour.rect.colliderect(mouse_tour_rect) for une_tour in tour) and not any(bout_de_chemin.colliderect(mouse_tour_rect) for bout_de_chemin in hitbox_chemin):
                pygame.draw.rect(screen, "blue", mouse_tour_rect)

            else:
                pygame.draw.rect(screen, "red", (mouse_tour_rect))

mouse_tour_rect = pygame.Rect(0, 0, 75, 75)

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
                enemies.add(Enemi_rouge)
            if event.key == pygame.K_2:
                enemies.add(Enemi_vert)
            if event.key == pygame.K_3:
                enemies.add(Enemi_bleu)
                         
            if mode_placement != False:
                if event.key == pygame.K_ESCAPE:
                    mode_placement = False

        if event.type == pygame.MOUSEBUTTONDOWN: #event pour détecter les clique de la souris
            #if event.button == 1:
            #    print(mouse_pos)

            if bouton_play.is_overmouse(mouse_pos): #event pour detécter si la souris est sur le bouton
                if not Systeme_Vague.running:
                    Systeme_Vague.prochaine_vague()

            #gestion des tours
            if mode_placement == False: #le mode placement correspond au mode ou l'on peut poser des tour sur la map
                if event.button == 1:
                    for icone_tour in hud:
                        if icone_tour.rect.collidepoint(mouse_pos):
                            mode_placement = icone_tour
                            mouse_tour_rect = pygame.Rect(mouse_pos, liste_tour[icone_tour.tour_index][1].size)


            else: #ce else est activé si le joueur est dans le mode placement de tour
                if event.button == 1:
                    if map_rect.contains(mouse_tour_rect): #verifier si les coordoner sont dans l'écran
                        if True: #plus tard, mettre ici la vérification de si on a assez d'argent ou pas
                            if not any(une_tour.rect.colliderect(mouse_tour_rect) for une_tour in tour): #verifier si une tour collide avec l'endroit ou le joueur veut en placer une
                                if not any(bout_de_chemin.colliderect(mouse_tour_rect) for bout_de_chemin in hitbox_chemin):#est ce que le curseur est sur le chemin ?
                                    mode_placement.ajouter_tour(mouse_pos)
                    
                        else:#dans ce cas, le joueur n'as pas assez d'argent
                            pass
                            #print() vous n'avez pas assez d'argent et tout et tout
                    else:
                        for icone_tour in hud: #sert a changer quelle tour le joueur peut placer même si il est déjà dans le mode placment
                            if icone_tour.rect.collidepoint(mouse_pos):
                                mode_placement = icone_tour
                                mouse_tour_rect = pygame.Rect(mouse_pos, liste_tour[icone_tour.tour_index][1].size)

                if event.button == 1:#pour sortir du mode placement de tour
                    if bouton_exit_placer_rect.collidepoint(mouse_pos):
                        mode_placement = False

        if event.type == SPAWN_ENEMY and Systeme_Vague.running:
            # Créer un nouvel ennemi
            Systeme_Vague.update_vague()
            if Systeme_Vague.compteur_vague_tick > 3*Systeme_Vague.numero_vague and len(enemies) == 0:
                Systeme_Vague.running = False
                Systeme_Vague.stop_vague()
        if bouton_play.is_overmouse(mouse_pos):
                pass

    # Mise à jour des ennemis
    enemies.update()

    #Affichage
    screen.fill("yellow") #fond jaune
    screen.blit(map_image, (0, 0)) #map

    if not Systeme_Vague.running:
        screen.blit(bouton_play_image, bouton_play.pos)

    screen.blit(Systeme_Vague.text_vague, Systeme_Vague.rect_text_vague)  # Affiche tous les ennemis
    gestion_affichage_mode_placement() #gestion du curseur rouge / bleu, le l'icone fermer + de la preview de la tour
    #hud.draw(screen) #draw les icones des tours

    for i in hud:
        i.afficher()

    Vie1.update()#draw la vie, + update avec les 
    
    #map
    tour.draw(screen)
    enemies.draw(screen)
    
    #for i in hitbox_chemin:# pour afficher la hitbox du chemin et debuger le code
    #    pygame.draw.rect(screen, "red", i)
    pygame.display.update()
    clock.tick(400)  #Limite à 60 FPS

"""
a faire
    chemin min()
    vie1 draw et update != 

    restucturer le code pour que le mode_placement ne soit plus dans la fonction mouse bouton down mais a part pour une meilleur lisibilité
    class argent
"""