import pygame
from sys import exit
from random import randint
pygame.init()

pygame.display.set_caption("jeu tower defance v1")
clock = pygame.time.Clock()

#font (a changer plus tard)
font = pygame.font.Font(None, 50)

#background fill, a enlever quand le scripte sera fini, cette zone n'est jamais sensé être vue
screen = pygame.display.set_mode((1440,880))
screen.fill("red")

#map
map = pygame.image.load(".venv/img/map_1.png").convert()
map = pygame.transform.smoothscale(map, (1200, 800))
map_rect = map.get_rect(topleft = (0, 0))

#icones
coeur = pygame.image.load(".venv/img/icones/coeur.png").convert_alpha()
coeur =  pygame.transform.smoothscale(coeur, (40, 40))
coeur_rect = coeur.get_rect(midright = (1035, 840)) #décaler de 15px du txt_vie

son_mute = pygame.image.load(".venv/img/icones/son_mute.png").convert_alpha()
son_mute = pygame.transform.smoothscale(son_mute, (42, 42))
son_mute_rect = son_mute.get_rect(center = (450, 838))

son_on = pygame.image.load(".venv/img/icones/son_on.png").convert_alpha()
son_on = pygame.transform.smoothscale(son_on, (42, 42))
son_on_rect = son_on.get_rect(center = (450, 838))



#son
hit = pygame.mixer.Sound('.venv/sound/hit.mp3')

class Statistiques():
    """
    statistique basique du joueur (argent, vie, ennemie tué, score, ...)
    """
    def __init__(self):
        self.argent = 1000
        self.ennemie_tue = 0
        #vie
        self.vie = 10 #si cette valeur est modifier, il faut modifier la valeur dans l'argument de la ligne d'en dessous
        self.text_vie = font.render("Vie : 10", False, "Red")
        self.text_vie_rect = self.text_vie.get_rect(midleft = (1050,840))
        #score
        self.score = 0
        self.txt_score = font.render("score : 0", False, "Blue")
        self.txt_score_rect = self.txt_score.get_rect(midleft = (40,840))

    def update_score(self, nouveau_score, ajouter = False):
        """
        si ajouter est False (ou non préciser), la fonction sert a définir le score a une valeur précises,
        si Ajouter est défini et égale à True, la fonction prend le score acctuelle et ajoute le parmaètre pris en entrer (nouveau_score)
        """
        self.score = self.score + nouveau_score if ajouter else nouveau_score
        self.txt_score = font.render(f"score: {self.score}", False, "Blue")
    
    def update_vie(self, vie, retirer = True):
        """
        si retirer n'est pas définie ou qu'il est égale a True, update la vie en retirant vie a self.vie
        si retirer est préciser et égale a false, la vie est défini a une valeur précise
        """
        if retirer:
            if self.vie - vie <= 0:
                print("game over") #ici, il faut faire en sotre que le jeu s'arrêt
                self.vie = 0
            else:
                self.vie -= vie
            if son == True:
                hit.play()
        else: #si retirer == False, alors on defini self.vie a la valeur de vie
            slef.vie = vie

        self.text_vie = font.render(f"Vie : {self.vie}", False, "Red")
        pygame.mixer.Sound('.venv/sound/hit.mp3')

    
    def update(self):        
        screen.blit(self.txt_score, self.txt_score_rect) #score
        screen.blit(coeur, coeur_rect) #vie coeur
        screen.blit(self.text_vie, self.text_vie_rect) #vie txt
        
stat = Statistiques()
son = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 
        if event.type == pygame.MOUSEMOTION: #print la position de la souris quand elle bouge, utilse pour debuger ou trouver des pixel précis
            pass
            #print(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                #clique gauche détecter
                
                if son:
                    if son_on_rect.collidepoint(pygame.mouse.get_pos()):
                        son = False
                        print(son)
                else:
                    if son_mute_rect.collidepoint(pygame.mouse.get_pos()):
                        son = True
                        print(son)
                
    #ligne pour tester les scripte
    #stat.update_score(1, True) #test que le score marche bien
    if randint(0,50) == 0: #ligne pour tester si la vie marche
        stat.update_vie(1) #ligne pour tester si la vie marche
    
    #update :
    #map
    screen.fill("Yellow")
    screen.blit(map,map_rect) #map(a faire absolument en premier)
    
    stat.update() #affichage des states

    if son == True:
        screen.blit(son_on,son_on_rect)        
    else:
        screen.blit(son_mute,son_mute_rect)

    #derière ligne du scripte
    pygame.display.update()
    clock.tick(60)