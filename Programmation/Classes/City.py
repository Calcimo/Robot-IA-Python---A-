from .Case import Case
from .Building import Building
from tkinter import *
from .Task import Task
from .Robot import Robot
from .Team import Team
import random
import logging


class City:

    def __init__(self,sizeX,sizeY, canvas, fenetre, nbrobot = 2):
        """
        Constructeur de la classe city.
        ***Param***
        sizex - la taille horizontale de la ville.\n
        sizey - la taille verticale de la ville.\n
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        fenetre (Window::class) - Fenetre dans laquelle la ville où se trouve les robots est affichée
        """
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = []
        for i in range(sizeX):
            matrixLine = []
            for j in range(sizeY):
                matrixLine += [Case(i,j)]
            self.matrix += [matrixLine]
        self.photo = [PhotoImage(file = "Design/recharge1_1.png"),#0
                    PhotoImage(file = "Design/recharge1_2.png"),#1
                    PhotoImage(file = "Design/recharge1_3.png"),#2
                    PhotoImage(file = "Design/recharge2_1.png"),#3
                    PhotoImage(file = "Design/recharge2_2.png"),#4
                    PhotoImage(file = "Design/recharge2_3.png"),#5
                    PhotoImage(file = "Design/recharge3_1.png"),#6
                    PhotoImage(file = "Design/recharge3_2.png"),#7
                    PhotoImage(file = "Design/recharge3_3.png"),#8
                    PhotoImage(file = "Design/route.png"),#9
                    PhotoImage(file = "Design/toit1_1.png"),#10
                    PhotoImage(file = "Design/toit1_1_bis.png"),#11
                    PhotoImage(file = "Design/toit1_2.png"),#12
                    PhotoImage(file = "Design/toit1_3.png"),#13
                    PhotoImage(file = "Design/toit2_1.png"),#14
                    PhotoImage(file = "Design/toit2_2.png"),#15
                    PhotoImage(file = "Design/toit2_3.png"),#16
                    PhotoImage(file = "Design/toit3_1.png"),#17
                    PhotoImage(file = "Design/toit3_2.png"),#18
                    PhotoImage(file = "Design/toit3_3.png"),#19
                    PhotoImage(file = "Design/toit3_3_bis.png"),#20
                    PhotoImage(file = "Design/toit2_2_bis.png"),#21
                    PhotoImage(file = "Design/toit2_3_bis.png"),#22
                    PhotoImage(file = "Design/toit3_2_bis.png"),#23
                    PhotoImage(file = "Design/toit3_3_v3.png"),#24
                    PhotoImage(file = "Design/simple_tache.png"),#25
                    PhotoImage(file = "Design/enchere.png")#26
                    ]
        self.photoZoom = [PhotoImage(file = "Design/recharge1_1.png"),#0
                    PhotoImage(file = "Design/recharge1_2.png"),#1
                    PhotoImage(file = "Design/recharge1_3.png"),#2
                    PhotoImage(file = "Design/recharge2_1.png"),#3
                    PhotoImage(file = "Design/recharge2_2.png"),#4
                    PhotoImage(file = "Design/recharge2_3.png"),#5
                    PhotoImage(file = "Design/recharge3_1.png"),#6
                    PhotoImage(file = "Design/recharge3_2.png"),#7
                    PhotoImage(file = "Design/recharge3_3.png"),#8
                    PhotoImage(file = "Design/route.png"),#9
                    PhotoImage(file = "Design/toit1_1.png"),#10
                    PhotoImage(file = "Design/toit1_1_bis.png"),#11
                    PhotoImage(file = "Design/toit1_2.png"),#12
                    PhotoImage(file = "Design/toit1_3.png"),#13
                    PhotoImage(file = "Design/toit2_1.png"),#14
                    PhotoImage(file = "Design/toit2_2.png"),#15
                    PhotoImage(file = "Design/toit2_3.png"),#16
                    PhotoImage(file = "Design/toit3_1.png"),#17
                    PhotoImage(file = "Design/toit3_2.png"),#18
                    PhotoImage(file = "Design/toit3_3.png"),#19
                    PhotoImage(file = "Design/toit3_3_bis.png"),#20
                    PhotoImage(file = "Design/toit2_2_bis.png"),#21
                    PhotoImage(file = "Design/toit2_3_bis.png"),#22
                    PhotoImage(file = "Design/toit3_2_bis.png"),#23
                    PhotoImage(file = "Design/toit3_3_v3.png"),#24
                    PhotoImage(file = "Design/simple_tache.png"),#25
                    PhotoImage(file = "Design/enchere.png")#26
                    ]
        self.idPhoto = []
        self.buildings = []
        self.tasks = []
        self.imgRobots = []
        self.ourTasks = {}
        self.randomGenerate(canvas)
        self.addRandomTask(canvas)
        self.teams = []
        self.nbrobot = nbrobot
        self.labelench = []
        self.labelteam = []
        self.labelpoint = []
        self.labelrobot = []
        self.generateTeams(canvas,fenetre)
        self.mult = 1
        self.reload = 0
        self.enmouv = False
        


    def getCel(self,x,y):
        """
        Retourne la cellule dont les coordonnées sont passées en paramètre
        ***Param***
        x - poition x de la cellule \n
        y - postion y de la cellule
        ***Return***
        (Case::class) La cellule souhaitée.
        """
        #print(x,y)
        return self.matrix[x][y]

    def detectSpace(self,bat)->bool:
        """
        Permet de savoir si un bâtiment à l'espace nécessaire pour être ajouter à l'emplacement voulu
        ***Param***
        bat (Building::class) - bâtiment à ajouter à la ville
        ***Return***
        booléen indiquant si le bâtiment possède l'espace nécessaire ou non.
        """
        #print("nouveau batiement")
        retour = True
        for i in range(bat.x - 1,bat.x+bat.sizeX + 2):
            for j in range(bat.y - 1,bat.y+bat.sizeY + 2):
                if i < 0 or i > self.sizeX -1 or j < 0 or j > self.sizeY - 1:
                    retour = False
                if i >= 0 and i < self.sizeX and j >=0 and j < self.sizeY :
                    #print("On teste la case",i,j)
                    if self.getCel(i,j).status != "route" :
                        retour = False
                        #print("boum")
            """
        if retour :
            #print("batiment accepté")
        else :
            #print("batiment refusé")
            """
        return retour

    def randomGenerate(self, canvas):
        """
        Méthode permettant de remplir la ville de bâtiments de façon aléatoire.
        ***Param***
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        """
        #Génération des grands batiments avec X et Y pouvant avoir comme valeur 2 ou 3
        for i in range(self.sizeX-2):
            for j in range(self.sizeY-2):
                randSizeX = random.randint(2,3)
                randSizeY = random.randint(2,3)
                bat = Building(i,j,randSizeX,randSizeY,"decor")
                if self.detectSpace(bat) :
                    bat.createBuilding(self)

        #Génération des moyens batiments avec X et Y pouvant avoir comme valeur 1 ou 2
        for i in range(self.sizeX-2):
            for j in range(self.sizeY-2):
                randSizeX = random.randint(1,2)
                randSizeY = random.randint(1,2)
                bat = Building(i,j,randSizeX,randSizeY,"decor")
                if self.detectSpace(bat) :
                    bat.createBuilding(self)

        #Génération des petits batiments avec X et Y pouvant avoir comme valeur 1
        for i in range(self.sizeX-2):
            for j in range(self.sizeY-2):
                bat = Building(i,j,1,1,"decor")
                if self.detectSpace(bat) :
                    bat.createBuilding(self)
        
        #Conversion de n batiment en station de recharge
        stock = []
        for i in range(self.sizeX*self.sizeY//100):
            alea = random.randint(0, len(self.buildings)-1)
            while (alea in stock) and (len(stock) < len(self.buildings)):
                alea = random.randint(0, len(self.buildings)-1)
            stock += [alea]
            self.buildings[alea].bType = "station"

        #Génération graphique des routes
        #for i in range(20, 600, 20):
        #    for j in range(20, 600, 20):
        #        city = canvas.create_image(i, j, anchor = NW, image = self.photo[9])
        city = canvas.create_rectangle(20, 20, self.sizeX*20, self.sizeY*20, fill='grey')

        #Génération graphique des bâtiments + case de charge
        for i in range(len(self.buildings)):
            #batiment decor
            if self.buildings[i].bType == "decor":
                #batiment 1 1
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 1:
                    nob = random.random()
                    if nob < 0.5:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[10])
                        self.idPhoto.append(0)
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[11])
                        self.idPhoto.append(1)
                #batiment 1 2
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[12])
                    self.idPhoto.append(0)
                #batiment 1 3
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[13])
                    self.idPhoto.append(0)
                #batiment 2 1
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[14])
                    self.idPhoto.append(0)
                #batiment 2 2
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 2:
                    nob = random.random()
                    if nob < 0.5:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[15])
                        self.idPhoto.append(0)
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[21])
                        self.idPhoto.append(1)
                #batiment 2 3
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 3:
                    nob = random.random()
                    if nob < 0.5:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[16])
                        self.idPhoto.append(0)
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[22])
                        self.idPhoto.append(1)
                #batiment 3 1
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[17])
                    self.idPhoto.append(0)
                #batiment 3 2
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 2:
                    nob = random.random()
                    if nob < 0.5:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[18])
                        self.idPhoto.append(0)
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[23])
                        self.idPhoto.append(1)
                #batiment 3 3
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 3:
                    nob = random.random()
                    if nob < 0.33334:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[19])
                        self.idPhoto.append(0)
                    elif nob < 0.666667:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[20])
                        self.idPhoto.append(1)
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                    self.buildings[i].y*20+20,
                                                    anchor = NW,
                                                    image = self.photo[24])
                        self.idPhoto.append(2)

            #batiment station
            elif self.buildings[i].bType == "station":
                
                #batiment 1 1
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[0])
                    self.idPhoto.append(0)
                #batiment 1 2
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[1])
                    self.idPhoto.append(0)
                #batiment 1 3
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[2])
                    self.idPhoto.append(0)
                #batiment 2 1
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[3])
                    self.idPhoto.append(0)
                #batiment 2 2
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[4])
                    self.idPhoto.append(0)
                #batiment 2 3
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[5])
                    self.idPhoto.append(0)
                #batiment 3 1
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[6])
                    self.idPhoto.append(0)
                #batiment 3 2
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[7])
                    self.idPhoto.append(0)
                #batiment 3 3
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20+20,
                                                self.buildings[i].y*20+20,
                                                anchor = NW,
                                                image = self.photo[8])
                    self.idPhoto.append(0)

                #generation case de charge
                for j in range(self.buildings[i].sizeY):
                    self.getCel(self.buildings[i].x-1, self.buildings[i].y+j).charge = True
                    self.getCel(self.buildings[i].x+self.buildings[i].sizeX, self.buildings[i].y+j).charge = True
                for j in range(self.buildings[i].sizeX):
                    self.getCel(self.buildings[i].x+j, self.buildings[i].y-1).charge = True
                    self.getCel(self.buildings[i].x+j, self.buildings[i].y+self.buildings[i].sizeY).charge = True

    def refreshGenerate(self, canvas):
        """
        Méthode permettant de rafraichir la generation (routes, batiments) dans le cadre du zoom.
        ***Param***
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        """
        self.mult = int(self.mult)
        canvas.delete('all')
        for i in range(len(self.photo)):
            self.photoZoom[i] = self.photo[i].zoom(self.mult)

        #Génération graphique des routes
        #for i in range(20*self.mult, 600*self.mult, 20*self.mult):
        #    for j in range(20*self.mult, 600*self.mult, 20*self.mult):
        #        city = canvas.create_image(i, j, anchor = NW, image = self.photoZoom[9])
        city = canvas.create_rectangle(20*self.mult, 20*self.mult, self.sizeX*20*self.mult, self.sizeY*20*self.mult, fill='grey')
        
        #Génération graphique des bâtiments + case de charge
        for i in range(len(self.buildings)):
            #batiment decor
            if self.buildings[i].bType == "decor":
                #batiment 1 1
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 1:
                    if self.idPhoto[i] == 0:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[10])
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[11])
                #batiment 1 2
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[12])
                #batiment 1 3
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[13])
                #batiment 2 1
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[14])
                #batiment 2 2
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 2:
                    if self.idPhoto[i] == 0:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[15])
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[21])
                #batiment 2 3
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 3:
                    if self.idPhoto[i] == 0:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[16])
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[22])
                #batiment 3 1
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[17])
                #batiment 3 2
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 2:
                    if self.idPhoto[i] == 0:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[18])
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[23])
                #batiment 3 3
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 3:
                    if self.idPhoto[i] == 0:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[19])
                    elif self.idPhoto[i] == 1:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[20])
                    else:
                        buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                    self.buildings[i].y*20*self.mult+20*self.mult,
                                                    anchor = NW,
                                                    image = self.photoZoom[24])

            #batiment station
            elif self.buildings[i].bType == "station":
                
                #batiment 1 1
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[0])
                #batiment 1 2
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[1])
                #batiment 1 3
                if self.buildings[i].sizeX == 1 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[2])
                #batiment 2 1
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[3])
                #batiment 2 2
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[4])
                #batiment 2 3
                if self.buildings[i].sizeX == 2 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[5])
                #batiment 3 1
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 1:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[6])
                #batiment 3 2
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 2:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[7])
                #batiment 3 3
                if self.buildings[i].sizeX == 3 and self.buildings[i].sizeY == 3:
                    buildings = canvas.create_image(self.buildings[i].x*20*self.mult+20*self.mult,
                                                self.buildings[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[8])

        #generation task
        for i in range(len(self.tasks)):
            if self.tasks[i].typeT == "base":
                self.ourTasks[(self.tasks[i].x,self.tasks[i].y)] = canvas.create_image(self.tasks[i].x*20*self.mult+20*self.mult,
                                                self.tasks[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[25])
            else :
                self.ourTasks[(self.tasks[i].x,self.tasks[i].y)] = canvas.create_image(self.tasks[i].x*20*self.mult+20*self.mult,
                                                self.tasks[i].y*20*self.mult+20*self.mult,
                                                anchor = NW,
                                                image = self.photoZoom[26])

        #generation robot
        for i in range(len(self.teams)):
            for j in range(len(self.teams[i].robots)):
                for k in range(len(self.teams[i].robots[j].photo)):
                    self.teams[i].robots[j].photoZoom[k] = self.teams[i].robots[j].photo[k].zoom(self.mult)
                if self.teams[i].robots[j].team == "blue" :
                    self.teams[i].robots[j].img = canvas.create_image(self.teams[i].robots[j].x*20*self.mult+20*self.mult,
                                                                        self.teams[i].robots[j].y*20*self.mult+20*self.mult,
                                                                        anchor = NW,
                                                                        image = self.teams[i].robots[j].photoZoom[self.teams[i].robots[j].numRobot])
                elif self.teams[i].robots[j].team == "red" :
                    self.teams[i].robots[j].img = canvas.create_image(self.teams[i].robots[j].x*20*self.mult+20*self.mult,
                                                                        self.teams[i].robots[j].y*20*self.mult+20*self.mult,
                                                                        anchor = NW,
                                                                        image = self.teams[i].robots[j].photoZoom[4+self.teams[i].robots[j].numRobot])

    def generateTeams(self, canvas, fenetre, nbTeams = 2):
        """
        Méthode permettant de générer les Teams dans la ville
        ***Param***
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        fenetre (Window::class) - Fenetre dans laquelle la ville où se trouve les robots est affichée\n
        int nbTeams - Nombre de Teams dans la ville\n
        int nbRobots - Nombre de Robots dans la ville
        """
        nbRobots = self.nbrobot
        color = ["blue","red"]
        k=0
        l=0
        for i in range(nbTeams):
            self.teams += [Team(color[i])]
            self.labelteam.append(Label(fenetre, text=f"{self.teams[i].color} team",font='Helvetica 14 bold', bg='#CCC2C2', width=23, height=4+self.nbrobot, anchor="n", borderwidth=2, relief='solid'))
            self.labelteam[i].pack()
            self.labelteam[i].place(x=10,y=60+30*k)
            if self.teams[i].color == "blue":
                self.labelteam[i].config(fg="#0091ff")
                c=0
            else:
                self.labelteam[i].config(fg="red")
                c=4
            for j in range(nbRobots):
                if color[i] == "blue" :
                    battery = random.randint(60,100)
                    self.teams[i].addRobot(Robot(0,0,"a*","blue",canvas,self, j, battery,battery,fenetre))
                    #self.imgRobots += [canvas.create_oval(25,25,35,35,fill="blue")]
                elif color[i] == "red" :
                    battery = random.randint(60,100)
                    self.teams[i].addRobot(Robot(self.sizeX-2,self.sizeY-2,"a*","red",canvas,self, j, battery,battery,fenetre))
                    #self.imgRobots += [canvas.create_oval((self.sizeX-1)*20+5,(self.sizeY-1)*20+5,(self.sizeX-1)*20+15,(self.sizeY-1)*20+15,fill="red")]
                self.labelrobot.append(Label(fenetre, text=f"Robot {j+1}",font='Helvetica 14 bold', bg='#CCC2C2'))
                self.labelrobot[j+l].bind("<Button-1>", lambda event, id=j+l, team=i, robot=j, c=c : self.mouseClick(id, fenetre, team, robot, c))
                self.labelrobot[j+l].pack()
                self.labelrobot[j+l].place(x=20,y=120+30*k)
                k+=1
            l += len(self.teams[i].robots)
            k+=3

    def addRandomTask(self, canvas):
        """
        Rempli la ville de tâches de façon aléatoire.
        ***Param***
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        """
        k = 0
        for i in range(self.sizeX-2):
            for j in range(self.sizeY-2):
                if k > 65:
                #if k < 3 :
                    k=0
                    points = 50
                    if random.random() > 0.9:
                        task = Task(i,j,150,"auction")
                    else :
                        task = Task(i,j,points,"base")
                    task.addTask(self)
                k += random.randint(1, 6)
                #k +=1
        for i in range(len(self.tasks)):
            if self.tasks[i].typeT == "base":
                self.ourTasks[(self.tasks[i].x,self.tasks[i].y)] = canvas.create_oval(self.tasks[i].x*20+20+20/4,
                                                                        self.tasks[i].y*20+20+20/4,
                                                                        self.tasks[i].x*20+20+20/4+20/2,
                                                                        self.tasks[i].y*20+20+20/4+20/2,
                                                                        fill='red')
            else :
                self.ourTasks[(self.tasks[i].x,self.tasks[i].y)] = canvas.create_oval(self.tasks[i].x*20+20+20/4,
                                                                        self.tasks[i].y*20+20+20/4,
                                                                        self.tasks[i].x*20+20+20/4+20/2,
                                                                        self.tasks[i].y*20+20+20/4+20/2,
                                                                        fill='purple')

    def getTask(self,x,y):
        """
        Renvoie la tâche dont les coordonnées sont placées en paramètre.
        ***Param***
        x - position x de la tâche \n
        y - postion y de la tâche
        ***Return***
        (task::class) - La classe souhaitée.  \n
        Renvoie la chaîne de caractère "ERROR" si aucune tâche ne correspond aux coordonnées.
        """
        retour = "ERROR"
        for i in range(len(self.tasks)):
            if self.tasks[i].x == x and self.tasks[i].y == y :
                retour = i
        return retour
    
    def removeTask(self,pos):
        """
        Supprime la tâche dont les coordonnées sont passées en paramètre.
        ***Param***
        pos tuple - coordonnées x et y de la tâche à supprimer.
        """
        self.tasks.pop(self.getTask(pos[0],pos[1]))
        self.getCel(pos[0],pos[1]).status = "route"

    def deplacement(self, canvas, fenetre):
        """
        Méthode permettant de simuler les tours de chaque robot
        ***Param***
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        fenetre (Window::class) - Fenetre dans laquelle la ville où se trouve les robots est affichée
        """
        if self.reload == 1:
            while self.labelpoint != []:
                self.labelpoint[0].destroy()
                self.labelpoint.pop(0)
            while self.labelteam != []:
                self.labelteam[0].destroy()
                self.labelteam.pop(0)
            while self.labelrobot != []:
                self.labelrobot[0].destroy()
                self.labelrobot.pop(0)
            while self.labelench != []:
                self.labelench[0].destroy()
                self.labelench.pop(0)
            return 1
        for i in range(len(self.teams)):
            for j in range(len(self.teams[i].robots)):
                """
                GARDER LE DEPLACEMENT ALEATOIRE ?
                if self.teams[i].robots.moveType == "alea":
                    depl = self.teams[i].robots.randomMove(self)
                """
                #Si le robot n'est pas entrain de se charger
                if self.teams[i].robots[j].isLoading == False :     
                    #Si le robot se déplace suivant l'algorithme a*                         
                    if self.teams[i].robots[j].moveType == "a*":
                        #Gestion du cas où le robot a déjà une tâche de type enchère en tâche marquée
                        if self.teams[i].robots[j].markedTask == None or self.teams[i].robots[j].markedTask != "auction":
                            currentAuction = self.isAuctionMarked()
                            #print("numéro du robot : ",j)
                            #print("on vérifie les enchères chez les ",self.teams[i].color)
                            #print(currentAuction)
                        else :
                            currentAuction = [False,False,False,-1,-1, -1, -1]
                        #Si le robot a besoin de se recharger
                        if self.teams[i].robots[j].needLoading() == True:
                            target = self.teams[i].robots[j].findLoadingFromRobotPos(self)
                            self.teams[i].robots[j].markedTask = None
                        #Si une enchère est en prise par un autre robot
                        else :
                            #Si cette enchère est prise par un robot de l'équipe opposé
                            if currentAuction[0] == True and ((currentAuction[1] == False and self.teams[i].robots[j].team == "blue") or (currentAuction[2] == False and self.teams[i].robots[j].team == "red")):
                                #print(currentAuction[3], currentAuction[4])
                                #print(type(self.getTask(currentAuction[3], currentAuction[4])))
                                if isinstance(self.getTask(currentAuction[3], currentAuction[4]), int) and not(self.teams[i].determineAuctionDealer(self.tasks[self.getTask(currentAuction[3], currentAuction[4])])):
                                    for p in range(len(self.teams)):
                                        for o in range(len(self.teams[p].robots)):
                                            self.teams[p].robots[o].markedTask = None
                                    self.removeTask([currentAuction[3], currentAuction[4]])
                                    canvas.delete(self.ourTasks[currentAuction[3], currentAuction[4]])
                                    currentAuction = [False,False,False,-1,-1, -1, -1]
                                    #("on détruit !")
                                elif self.getTask(currentAuction[3], currentAuction[4]) != "ERROR" : 
                                    self.teams[i].robots[j].markedTask = self.tasks[self.getTask(currentAuction[3], currentAuction[4])]
                            #Si le robot ne possède pas de tâche marquée
                            if self.teams[i].robots[j].markedTask == None :
                                target = self.teams[i].robots[j].findTaskFromRobotPos(self,currentAuction[0])
                            #Si le robot possède déjà une tâche marquée et qu'il ne l'a pas encore atteinte
                            else :
                                target = [self.teams[i].robots[j].markedTask.x, self.teams[i].robots[j].markedTask.y]
                        #création de la liste de coordonnées successives que le robot empruntera
                        chemin = self.teams[i].robots[j].aEtoileMove(self,target)
                        #affichage des encheres prise sur la window
                        if currentAuction[0] == True:
                            if self.labelench == []:
                                self.labelench.append(Label(fenetre, text=f"Robot {currentAuction[6]+1} / {self.teams[currentAuction[5]].color} team\n is participating\n in an auction",font='Arial 15 bold', fg="white", bg='#CCC2C2', borderwidth=2, relief="solid", width=20, height=10))
                                #print(f"Robot {j+1} de Team {i+1} a pris une enchere")
                                self.labelench[0].pack()
                                self.labelench[0].place(x=920,y=150)
                                if self.teams[i].color == "blue":
                                    c = 0
                                else:
                                    c = 4
                                self.labelench.append(Label(fenetre, image=self.teams[currentAuction[5]].robots[currentAuction[6]].photo[self.teams[currentAuction[5]].robots[currentAuction[6]].numRobot+c], bg='#CCC2C2'))
                                self.labelench[1].pack()
                                self.labelench[1].place(x=1030,y=185)
                        else:
                            while self.labelench != []:
                                self.labelench[0].destroy()
                                self.labelench.pop(0)

                        #Si le robot n'a pas trouvé de tâche
                        if chemin == None :
                            chemin = [[0,0,-1,-1]]
                        depl = self.teams[i].robots[j].moveItSelfFromCoord([chemin[0][0],chemin[0][1]]) + [chemin[0][2],chemin[0][3]]
                    dx = depl[0]*self.mult
                    dy = depl[1]*self.mult
                    #gestion du cas où le robot s'est fait "volé sa tâche" par un autre robot
                    if dx == 0 and dy == 0 and self.teams[i].robots[j].markedTask != None and self.teams[i].robots[j].markedTask.typeT == "base":
                        self.teams[i].robots[j].markedTask = None
                    #pour l'instant tjs le problème de robots qui ne bougent pas
                    #--------------------ICI-----------------------------------
                    #Si le robot est sur une case de tâche
                    if depl[2] != -1:
                        #Si le robot est apte à traiter la tâche et qu'il se trouve sur une tâche
                        if self.teams[i].robots[j].needLoading() == False and self.getCel(depl[2],depl[3]).status == "task":
                            #Si la tâche est simple (pas d'enchère) ou que la tâche appartient à l'équipe du robot
                            if (self.tasks[self.getTask(depl[2],depl[3])].typeT == "base" or self.teams[i].robots[j].team == self.tasks[self.getTask(depl[2],depl[3])].belongsTo):
                                canvas.delete(self.ourTasks[depl[2],depl[3]])
                                self.teams[i].robots[j].markedTask = None
                                self.teams[i].addPoint(self.tasks[self.getTask(depl[2],depl[3])].pointValue)
                                #print("Score de l'équipe :",self.teams[i].color, "est de :",self.teams[i].point)
                                self.removeTask([depl[2],depl[3]])
                            else:
                            #elif self.getCel(self.teams[i].robots[j].x,self.teams[i].robots[j].y) :
                                #print("le robot attend un challenger") #a completer
                                myRobot = self.teams[i].robots[j]
                                for k in range(len(self.teams)):
                                    for p in range(len(self.teams[k].robots)):
                                        ennemyRobot = self.teams[k].robots[p]
                                        if myRobot != ennemyRobot and myRobot.x == ennemyRobot.x and myRobot.y == ennemyRobot.y and ennemyRobot.markedTask == myRobot.markedTask :
                                            #print("----------------on fait la résolution de la tâche---------------")
                                            self.teams[i].auctionAgainstOtherTeam(myRobot.markedTask,self.teams[k])
                                            myRobot.markedTask = None
                                            ennemyRobot.markedTask = None
                                            self.removeTask([depl[2],depl[3]])
                                            canvas.delete(self.ourTasks[depl[2],depl[3]])
                        else : 
                            self.teams[i].robots[j].isLoading = True
                    canvas.move(self.teams[i].robots[j].img,dx,dy)
                if self.teams[i].robots[j].isLoading :
                    if self.teams[i].robots[j].batteryLevel + 5 <= self.teams[i].robots[j].maxBattery :
                        self.teams[i].robots[j].batteryLevel += 5
                        self.teams[i].point -= 1
                    else :
                        self.teams[i].robots[j].batteryLevel = self.teams[i].robots[j].maxBattery
                        self.teams[i].robots[j].isLoading = False
        #print("on fini un tour pour un robot")
        canvas.pack()
        k = 0
        while self.labelpoint != []:
            self.labelpoint[0].destroy()
            self.labelpoint.pop(0)
        for i in range(len(self.teams)):
            self.labelpoint.append(Label(fenetre, text=f"score : {int(self.teams[i].point)}",font='Helvetica 14 bold', bg='#CCC2C2'))
            self.labelpoint[i].pack()
            self.labelpoint[i].place(x=125,y=90+30*k)
            k+=3+len(self.teams[i].robots)

        k=0
        for i in range(len(self.teams)):
            for j in range(len(self.teams[i].robots)):
                self.teams[i].robots[j].meter.pack()
                self.teams[i].robots[j].meter.place(x=100,y=120+30*k)
                self.teams[i].robots[j].showbattery(self.teams[i].robots[j].meter)
                k+=1
            k+=3
        fenetre.after(50*len(self.teams)*len(self.teams[i].robots)-20*len(self.teams[i].robots), self.deplacement, canvas, fenetre)

    def mouseClick(self, id, fenetre, team, robot, c):    
        top=Toplevel(fenetre)
        top.config(bg='#636A73')
        l=Label(top,image = self.teams[team].robots[robot].photo[self.teams[team].robots[robot].numRobot+c], bg='#636A73')
        l.pack()

    def lemouv(self, canvas, fenetre):
        if self.enmouv == False:
            self.deplacement(canvas, fenetre)
            self.enmouv = True

    def isAuctionMarked(self):
        """
        Permet de savoir si une tâche d'enchère est marquée et par quelle équipe
        ***Return***
        array - contenant [bool indiquant si une enchère est marquée ou non,
                            bool indiquant si équipe bleu marqué,
                            bool indiquant si équipe rouge marqué,
                            coordonnées x de la tâche, 
                            coordonnées y de la tâche,
                            int num team prise;
                            int num robot pris]
        """
        toReturn = [False,False,False,-1,-1, -1, -1]
        for i in range(len(self.teams)):
            for j in range(len(self.teams[i].robots)):
                myTask = self.teams[i].robots[j].markedTask
                #print(myTask)
                if myTask != None and myTask.typeT == "auction" :
                    toReturn[0] = True
                    toReturn[3] = myTask.x
                    toReturn[4] = myTask.y
                    if self.teams[i].color == "blue":
                        toReturn[1] = True
                    else :
                        toReturn[2] = True
                    toReturn[5] = i
                    toReturn[6] = j
        #print(toReturn)
        return toReturn
