from tkinter import *
from pytetris import *

DIM = 30

#Couleurs utiles aux Tetris
COULEURS = ["red", "blue", "green","coral1","yellow", "orange", "purple", "pink","CadetBlue4",
            "dark grey", "black"]


class VueTetris:
    def __init__(self, modele):
        """
        Constructeur de la classe VueTetris
        """
        #Construction du terrain :
        self.__modele = modele
        self.__fenetre = Tk()
        self.__fenetre.title("Tetris")
        self.__can_terrain = Canvas(self.__fenetre, width=DIM * self.__modele.get_largeur() +300, height=DIM * self.__modele.get_hauteur())
        self.__can_terrain['bg']='aquamarine'
        
        #Construction du bouton quitter :
        self.__bouton_quitter = Button(self.__fenetre,text = "Au Revoir",command = self.__fenetre.destroy)        
        self.__can_terrain.pack()
        self.__bouton_quitter.pack()
        self.__bouton_quitter['bg']='brown2'
        self.__bouton_quitter.place(x=23*self.__modele.get_hauteur(),y=20*self.__modele.get_hauteur())
        
        #Construction de la Forme Suivante et du petit carré 6x6 :
        self.__SUIVANT = 6
        self.forme_suivante = Label(self.__fenetre,text="Forme Suivante")
        self.forme_suivante.place(x=22*self.__modele.get_hauteur()+5,y=10*self.__modele.get_hauteur())
        self.forme_suivante['bg']='aquamarine'
        self.__can_fsuivante = Canvas(self.__fenetre, width=self.__SUIVANT*30, height=self.__SUIVANT*30)
        self.__can_fsuivante['bg']='aquamarine'
        
        # Score :
        self._lbl_score = Label(self.__fenetre,text="Score : 0")
        self._lbl_score.place(x=23*self.__modele.get_hauteur()+5,y=19*self.__modele.get_hauteur())
        self._lbl_score['bg']='aquamarine'
        
        #Forme suivante :
        self.__les_suivants = []
        for i in range(0,self.__SUIVANT):
            ligne = []
            for j in range(0,self.__SUIVANT):
                case = self.__can_fsuivante.create_rectangle(i*DIM,j*DIM, DIM + i*DIM, DIM + j*DIM, outline="white", fill="black")
                ligne.append(case)
            self.__les_suivants.append(ligne)
        self.__can_fsuivante.place(x=20*self.__modele.get_hauteur()+5,y=11*self.__modele.get_hauteur())
        
        # Bouton commencer/pause/recommencer :
        self.__bouton_start = Button(self.__fenetre,text = "Commencer",command = self.change_btn) 
        self.__bouton_start.pack()
        self.__bouton_start.place(x=23*self.__modele.get_hauteur(),y=5*self.__modele.get_hauteur())
        self.__bouton_start['bg']='chocolate1'
        self.__start = False
        
        # Boucle création de cases :
        self.__les_cases = []
        for i in range(self.__modele.get_hauteur()):
            ligne = []
            for j in range(self.__modele.get_largeur()):
                case = self.__can_terrain.create_rectangle(j*DIM,i*DIM, DIM + j*DIM, DIM + i*DIM, outline="white", fill=COULEURS[self.__modele.get_valeur(j, i)])
                ligne.append(case)
            self.__les_cases.append(ligne)
 
    def change_btn(self):
        """
        Change le texte du bouton en fonction de la partie 
        """
        if self.__modele.fini():
            Button.destroy(self.__bouton_start)
            self.__bouton_start = Button(self.__fenetre,text = "Recommencer",command = self.recommencer)
            self.__bouton_start['bg']='white'
            self.__bouton_start.pack()
            self.__bouton_start.place(x=23*self.__modele.get_hauteur(),y=5*self.__modele.get_hauteur())
        if self.__bouton_start['text'] == 'Commencer':
            self.__bouton_start['bg']='chocolate'
            self.start()
            self.__bouton_start['text'] = 'Pause'
        elif self.__bouton_start['text'] == 'Pause':
            self.__bouton_start['bg']='chocolate1'
            self.pause()
            self.__bouton_start['text'] = 'Reprendre'
        elif self.__bouton_start['text'] == 'Reprendre':
            self.__bouton_start['bg']='chocolate'
            self.reprendre()
            self.__bouton_start['text'] = 'Pause'
            
    def recommencer(self):
        """
        Recrée une instance de ModeleTetris pour rejouer
        """
        self.__fenetre.destroy()
        tetris = md.ModeleTetris()
        ctrl = Controleur(tetris)

    def start(self):
        if self.__start == False:
            self.__start = True

    def pause(self):
        """
        Met en pause le jeu
        """
        self.__start = False

    def reprendre(self):
        """
        Reprend le jeu
        """
        self.__start = True

    def recommencer_partie(self):
        """
        Recree une nouvelle partie une fois que la precedente est finie
        """
        if self.__modele.fini():
            self.__modele.recommencer()
                    
    def get_start(self):
        """
        Retourne l'état du bouton start (True = Partie lancée et False = arrêt)
        """
        return self.__start
        
    def met_a_jour_score(self,val):
        """
        Mets à jours le bouton score
        """
        self._lbl_score.config(text=f"Score : {self.__modele.get_score()}")

    def dessine_case_suivante(self, h, l, color):
        """
        dessine la case suivante en ligne i et en colonne j de la couleur a l'indice coul
        """
        self.__can_fsuivante.itemconfig(self.__les_suivants[h][l], fill=COULEURS[color])

    def nettoie_forme_suivante(self):    
        for i in range(len(self.__les_suivants)):
            for j in range(len(self.__les_suivants)):
                self.dessine_case_suivante(i,j,-1)

    def dessine_forme_suivante(self,coords,coul):
        """
        dessine la prochaine forme en fonction de ses coordonnées et de sa couleur
        """
        self.nettoie_forme_suivante()
        for i in range(len(coords)):
            self.dessine_case_suivante(coords[i][1]+2, coords[i][0]+2, coul)

    def fenetre(self):
        """
        Renvoie la fenetre
        """
        return self.__fenetre

    def dessine_case(self, h, l, color):
        """
        Dessine la case en ligne i et en colonne j de la couleur a l'indice coul
        """
        self.__can_terrain.itemconfig(self.__les_cases[h][l], fill=COULEURS[color])

    def dessine_terrain(self):
        """
        Dessine le terrain
        """
        for h in range(self.__modele.get_hauteur()):
            for l in range(self.__modele.get_largeur()):
                self.dessine_case(h, l, self.__modele.get_valeur(h, l))

    def dessine_forme(self, coords, coul):
        """
        Dessine la forme en fonction de ses coordonnées et de sa couleur
        """
        for i in range(len(coords)):
            self.dessine_case(coords[i][1], coords[i][0], coul)