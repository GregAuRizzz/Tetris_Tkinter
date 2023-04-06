import random

class ModeleTetris:
    def __init__(self, nb_lignes=20, nb_colonnes=14, base=4,score=0):
        """
        Constructeur de la classe ModeleTetris
        """
        self.__haut = nb_lignes + base
        self.__larg = nb_colonnes
        self.__base = base
        self.__score = score
        self.__terrain = []
        for i in range(self.__base):
            self.__terrain.append([-2 for _ in range(self.__larg)])
        for x in range(self.__haut-self.__base):
            self.__terrain.append([-1 for _ in range(self.__larg)])
        self.__forme = Forme(self)
        self.__suivante = Forme(self)

    def get_largeur(self):
        """
        Renvoie la largeur du plateau
        return -> int
        """
        return self.__larg

    def get_hauteur(self):
        """
        Renvoie la hauteur du plateau
        return -> int
        """
        return self.__haut

    def get_valeur(self, h, l):
        """
        h -> int
        l -> int
        Renvoie la valeur du terrain
        return -> int
        """
        if h >= len(self.__terrain) or l >= len(self.__terrain[0]):
            return 3
        return self.__terrain[h][l]

    def est_occupe(self, h, l):
        """
        l -> int
        c -> int
        Renvoie True si la case est occupé
        return -> Bool
        """
        if self.get_valeur(h, l) == -2 or self.get_valeur(h, l) == -1:
            return False
        else:
            return True

    def fini(self):
        """
        Indique si la partie est fini
        return -> Bool
        """
        for i in range(self.__larg):
            if self.est_occupe(self.__base, i):
                return True
        return False
    def get_couleur_forme(self):
        """
        Renvoie la couleur de self.__forme
        return -> Str
        """
        return self.__forme.get_couleur()

    def get_coords_forme(self):
        """
        Renvoie les coordonnées absolues de self_forme
        return -> (int,int)
        """
        return self.__forme.get__coords()

    def ajoute_forme(self):
        """
        Pose self.__forme sur le terrain 
        """
        for y, x in self.__forme.get__coords():
            self.__terrain[x][y] = self.__forme.get_couleur()
            
    #Modifié à l'étape 3:
    def forme_tombe(self):
        """
        Fait tomber self.__forme si elle n'est pas tombé
        return -> bool
        """
        if self.__forme.tombe():
            self.ajoute_forme()
            self.__forme = self.__suivante
            self.__suivante = Forme(self)
            self.supprime_ligne_complete()
            return True
        else:
            return False
    
    def forme_a_gauche(self):
        """
        Modifie la forme de une case vers la gauche
        """
        self.__forme.a_gauche()
    
    def forme_a_droite(self):
        """
        Modifie la forme de une case vers la droite
        """
        self.__forme.a_droite()
        
    def forme_tourne(self):
        """
        Fait tourner la forme
        """
        self.__forme.tourne()
        
    def est_ligne_complete(self,lig):
        """
        Verifie si une ligne est complété par des couleurs
        return -> bool
        """
        for i in range(0,lig):
            if not self.est_occupe(lig,i):
                return False
        return True
    
    def supprime_ligne(self,lig):
        """
        Supprime une ligne si elle est complète
        """
        if self.est_ligne_complete(lig):
            self.__terrain.pop(lig)
            nouvelle_ligne = []
            for i in range(0,self.get_largeur()):
                nouvelle_ligne.append(-1)
            self.__terrain.insert(4,nouvelle_ligne)
        
    def supprime_ligne_complete(self):
        """
        Verifie si il y a des lignes (sans la base)
        """
        for i in range(self.__base,self.get_hauteur()):
            if self.est_ligne_complete(i):
                self.__score += 1
                self.supprime_ligne(i)      

    def get_score(self):
        """
        Retourne le score actuel
        return -> int
        """
        return self.__score
    
    def get_couleur_suivante(self):
        """
        Renvoie la couleur de self.__forme
        return -> Str
        """
        return self.__suivante.get_couleur()
    def get_coords_suivante(self):
        """
        Renvoie la couleur de self.__forme
        return -> Str
        """
        return self.__suivante.get_coords_relatives()
    
# Liste des formes à générer et afficher
LES_FORMES = [[(0,1),(0,0),(0,-1),(0,2)],
              [(0,0),(0,1),(1,1),(1,0)],
              [(0,0),(-1,-1),(0,-1),(1,0)],
              [(0,0),(0,-1),(-1,0),(1,-1)],
              [(0,0),(-1,0),(1,0),(-1,1)],
              [(0,0),(-1,0),(1,0),(1,1)], 
              [(0,0),(-1,0),(1,0),(0,1)],
              [(0,0),(-1,0),(0,-1),(0,1),(1,0)],
              [(0,0),(0,1),(0,-1),(-1,1),(-1,-1)]]
                
class Forme:
    def __init__(self,modele,couleur = 0):
        """
        Constructeur de la class Forme
        """
        self.__modele = modele 
        self.__couleur = random.randint(0,len(LES_FORMES)-1)
        self.__forme = LES_FORMES[self.__couleur]
        self.__y0 = random.randint(2,self.__modele.get_largeur() -2)
        self.__x0 = 1
        
    def tourne(self):
        """
        Renvoie une nouvelle forme qui tourne si c'est possible
        """
        forme_prec,self.__forme = self.__forme,[]
        for i,j in forme_prec:
            self.__forme.append((-j,i))
        if self.position_valide():
            return self.__forme
        else:
            self.__forme = forme_prec

    def get_couleur(self):
        """
        Renvoie la couleur de la forme
        return -> int
        """
        return self.__couleur

    def get__coords(self):
        """
        Renvoie une liste de couple (int,int) qui sont les coordonées absolue de la forme sur le terrain du modèle
        return -> List
        """
        return [(self.__y0 + y,self.__x0 + x) for y,x in self.__forme]

    def collision(self):
        """
        Renvoie True si la forme doit se poser, faux sinon
        return -> bool
        """
        for x, y in self.get__coords():
            if self.__modele.est_occupe(y,x):
                return True
        return False

    def tombe(self):
        """
        Renvoie True si la forme est tombée, faux sinon
        :return:
        """
        self.__x0 += 1
        if self.collision():
            self.__x0 -= 1
            return True
        else:
            return False
        
    def position_valide(self):
        """
        teste si la position de la forme est valide
        :return:
        """
        for x, y in self.get__coords():
            if x < 0 or x >= self.__modele.get_largeur() or y < 0 or y >= self.__modele.get_hauteur() or self.__modele.est_occupe(y,x):
                return False
        return True
    def a_gauche(self):
        """
        dépalce la forme d'une colonne vers la gauche si possible et teste si la npuvelle position est valide
        :return:
        """
        self.__y0 -= 1
        if self.position_valide():
            return True
        else:
            self.__y0 += 1
            return False
    def a_droite(self):
        """
        déplace la forme d'une colonne vers la droite si possible et teste si la nouvelle position est valide
        :return:
        """
        self.__y0 += 1
        if self.position_valide():
            return True
        else:
            self.__y0 -= 1
            return False
    def get_coords_relatives(self):
        """
        Retourne les coordonnés relatives
        """
        return self.__forme
