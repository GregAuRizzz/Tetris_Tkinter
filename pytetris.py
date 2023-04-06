import modele as md
import vue

class Controleur:
    def __init__(self, tetris):
        """
        Constructeur de la case Controleur
        """
        self.__tetris = tetris
        self.__vue = vue.VueTetris(tetris)
        self.__fen = self.__vue.fenetre()
        self.__delai = 320
        self.joue()
        self.__fen.mainloop()
    
    def debind(self):
        """
        Unbind les 4 touches (enlever les fonctions aux touches)
        """
        self.__fen.unbind("<Key-Left>")
        self.__fen.unbind("<Key-Right>")
        self.__fen.unbind("<Key-Down>")
        self.__fen.unbind("<Key-Up>")

    def rebind(self):
        """
        Rebind les 4 touches (réassignation des fonctions aux touches)
        """
        self.__fen.bind("<Key-Left>",self.forme_a_gauche)
        self.__fen.bind("<Key-Right>",self.forme_a_droite)
        self.__fen.bind("<Key-Down>",self.forme_tombe)
        self.__fen.bind("<Key-Up>",self.forme_tourne)

    def joue(self):
        """
        Boucle principale du jeu. Fait tomber une forme d'une ligne, vérifie si la partie continue.
        """
        if self.__tetris.fini():
            self.__vue.change_btn()
        if not self.__tetris.fini() or self.__vue.get_start() == True:
            self.affichage()
            if self.__vue.get_start() == True:
                self.__tetris.forme_tombe()
            self.__fen.after(self.__delai, self.joue)
            
    def affichage(self):
        """
        Affiche le terrain et la forme en cours
        """
        if not self.__vue.get_start() :
            self.debind()
        if self.__vue.get_start():
            self.rebind()
        if not self.__tetris.fini():
            self.__vue.met_a_jour_score(self.__tetris.get_score())
            self.__vue.dessine_terrain()
            self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
            self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivante(),self.__tetris.get_couleur_suivante())
        
    def forme_a_gauche(self,event):
        """
        Décale la forme à gauche
        """
        self.__tetris.forme_a_gauche()
        
        
    def forme_a_droite(self,event):
        """
        Décale la forme à droite
        """
        self.__tetris.forme_a_droite()
        
    def forme_tombe(self,event):
        """
        Demande au modèle de faire tomber la forme plus vite
        """
        self.__delai = 190
        self.__tetris.forme_tombe()
        self.affichage()
        self.__delai = 330
        
    def forme_tourne(self,event):
        """
        Fait tourner la forme
        """
        self.__tetris.forme_tourne()

    
if __name__ == "__main__" :
    tetris = md.ModeleTetris()
    ctrl = Controleur(tetris)
