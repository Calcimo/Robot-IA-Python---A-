import random
import itertools
from tkinter import *
from tkinter import tix

class Robot:
    
    def __init__(self,x,y,moveType,team,canvas,city, numRobot = 0, batteryLevel=100,maxBattery=100,fenetre=""):
        """
        Constructeur de la classe Robot
        ***Param***
        int x - position x d'apparition du robot \n
        int y - position y d'apparition du robot \n
        str moveType - type de déplacement du robot (Aléatoire ou A*) \n
        str team - équipe du robot \n
        canvas (Canvas::class) - Canvas dans lequel le robot est dessiner\n
        city (City::class) - Ville dans laquelle se déplace le robot\n
        int numRobot - Numéro du robot\n
        int batteryLevel - niveau de charge du robot \n
        int maxBattery - niveau de charge maximal du robot \n
        bool isLoading - indique si le robot est en processus de rechargement\n
        fenetre (Window::class) - Fenetre dans laquelle la ville où se trouve les robots est affichée
        """
        self.x = x
        self.y = y
        self.moveType = moveType
        self.batteryLevel = batteryLevel
        self.maxBattery = maxBattery
        self.team = team
        self.isLoading = False
        self.numRobot = numRobot
        self.photo = [PhotoImage(file = "Design/robot_blue_1.png"),#0
                    PhotoImage(file = "Design/robot_blue_2.png"),#1
                    PhotoImage(file = "Design/robot_blue_3.png"),#2
                    PhotoImage(file = "Design/robot_blue_4.png"),#3
                    PhotoImage(file = "Design/robot_red_1.png"),#4
                    PhotoImage(file = "Design/robot_red_2.png"),#5
                    PhotoImage(file = "Design/robot_red_3.png"),#6
                    PhotoImage(file = "Design/robot_red_4.png")#7
                    ]
        self.photoZoom = [PhotoImage(file = "Design/robot_blue_1.png"),#0
                    PhotoImage(file = "Design/robot_blue_2.png"),#1
                    PhotoImage(file = "Design/robot_blue_3.png"),#2
                    PhotoImage(file = "Design/robot_blue_4.png"),#3
                    PhotoImage(file = "Design/robot_red_1.png"),#4
                    PhotoImage(file = "Design/robot_red_2.png"),#5
                    PhotoImage(file = "Design/robot_red_3.png"),#6
                    PhotoImage(file = "Design/robot_red_4.png")#7
                    ]
        if self.team == "blue" :
            self.img = canvas.create_image(20,
                                            20,
                                            anchor = NW,
                                            image = self.photo[self.numRobot])
        elif self.team == "red" :
            self.img = canvas.create_image((city.sizeX-1)*20,
                                            (city.sizeY-1)*20,
                                            anchor = NW,
                                            image = self.photo[4+self.numRobot])
        self.markedTask = None
        self.meter = tix.Meter(fenetre,fill="green")

    def moveItSelf(self,direction):
        """
        Déplace le robot dans la direction souhaitée
        ***Param***
        str direction - Direction dans laquelle va se déplacer le robot (N,S,E,O)
        ***Return***
        liste comportant les modifications (en pixel) de position du robot dans la ville
        """
        dx = 0
        dy = 0
        if self.batteryLevel > 0 :
            if direction == "N":
                self.y -= 1
                dy = -20
            elif direction == "S":
                self.y += 1
                dy = 20
            elif direction == "W":
                self.x -= 1
                dx = -20
            elif direction == "E":
                self.x += 1
                dx = 20
            self.batteryLevel -= 1
            return [dx,dy]
        return [0,0]

    def moveItSelfFromCoord(self,coord):
        """
        Déplace le robot vers les coordonneés souhaitée (à 1 de distance de l'emplacement du robot) \n
        Ce déplacement est impossible si le robot n'a plus de charge
        ***Param***
        tuple coord - Coordonnées de la case ciblée
        ***Return***
        liste comportant les modifications (en pixel) de position du robot dans la ville
        """
        dx = 0
        dy = 0
        if self.batteryLevel > 0 :
            if coord[0]-self.x == 1:
                self.x += 1
                dx = 20
            elif coord[0]-self.x == -1:
                self.x -= 1
                dx = -20
            elif coord[1]-self.y == 1:
                self.y += 1
                dy = 20
            elif coord[1]-self.y == -1:
                self.y -= 1
                dy = -20
            if [dx,dy] != [0,0] :
                self.batteryLevel -= 1
            return [dx,dy]
        return [0,0]

    def randomMove(self, city)->list:
        """
        Méthode permettant de déplacer un robot de façon aléatoire et de connaître l'emplacement de l'hypothétique tâche \n
        sur laquelle le robot se situerait.
        ***Param***
        city (City::class) - Ville dans laquelle le robot se déplace
        ***Return***
        liste comportant les éléments suivants : \n
                                                [Nombre de pixels de déplacement horizontal du robot, \n
                                                 Nombre de pixels de déplacement vertical du robot, \n
                                                 position x de la tâche (-1 si aucune tâche), \n
                                                 position y de la tâche (-1 si aucune tâche)]
        """
        retour = [0,0,-1,-1]
        alea = random.randint(0,3)
        #0 : Nord, 1: Est, 2: Sud, 3: Ouest
        if alea == 0 and self.y > 0:
            if city.getCel(self.x,self.y-1).status == "route" or city.getCel(self.x,self.y-1).status == "task":
                retour = self.moveItSelf("N")
                retour += self.detectTask(city)
        elif alea == 1 and self.x < city.sizeX-2:
            if city.getCel(self.x+1,self.y).status == "route" or city.getCel(self.x+1,self.y).status == "task":
                retour = self.moveItSelf("E")
                retour += self.detectTask(city)
        elif alea == 2 and self.y<city.sizeY-2:
            if city.getCel(self.x,self.y+1).status == "route" or city.getCel(self.x,self.y+1).status == "task":
                retour = self.moveItSelf("S")
                retour += self.detectTask(city)
        elif alea == 3 and self.x>0 :
            if city.getCel(self.x-1,self.y).status == "route" or city.getCel(self.x-1,self.y).status == "task":
                retour = self.moveItSelf("W")
                retour += self.detectTask(city)
        return retour

    def detectTask(self, city)->list:
        """
        Permet de savoir si un robot est présent sur une case de tâche.
        ***Param***
        city (City::class) - ville dans laquelle la tâche est détectée.
        ***Return***
        liste contenant les coordonnées de la tâche si le robot est dessus.  \n
        [-1,-1] si le robot n'est sur aucune tâche.
        """
        if city.getCel(self.x,self.y).status == "task":
            return [self.x,self.y]
        return [-1,-1]

    def aEtoileMove(self, city, posTask)->list: #ajout d'une tâche dans la param pour ne pas avoir le find dans la fonction et ne renvoyer que le dernier déplacement ou ne récupérer que le dernier
        """
        Algorithme de déplacement A*.
        Permet au robot de rejoindre un tâche en suivant l'agorithme A*.
        ***Param***
        city (City::class) - ville dans laquelle le robot évolue \n
        posTask tuple - comporte les coordonnées de la tâche à atteindre
        ***Return***
        liste de listes des différentes cases par lesquelles il faut passer pour rejoindre la tâche. \n
        Liste sous le format suivant : [[case1],[case2],...,[caseTâche]] \n
        [caseI] = [Position x de la prochaine cellule, \n
                   Position y de la prochaine cellule, \n
                   Position x de la tâche sur laquelle le robot se situe (-1 si aucune case), \n
                   Position y de la tâche sur laquelle le robot se situe (-1 si aucune case)]
        """
        open_nodes = []
        closed_nodes = []
        open_nodes += [self.determineNodesInfos([self.x,self.y],[self.x,self.y],posTask)+[[-1,-1]]]
        compt = 0
        #PARCOURS DE LA GRILE AVEC L'ALGO
        while compt < 100:     
            compt+=1
            miniF = open_nodes[0][3]
            miniH = open_nodes[0][2]
            current = open_nodes[0]
            index = 0
            for i in range(len(open_nodes)):
                if open_nodes[i][3] < miniF: 
                    miniF = open_nodes[i][3]
                    miniH = open_nodes[i][2]
                    current = open_nodes[i]
                    index = i
                elif open_nodes[i][3] == miniF and open_nodes[i][2] < miniH:
                    miniF = open_nodes[i][3]
                    miniH = open_nodes[i][2]
                    current = open_nodes[i]
                    index = i
            open_nodes.pop(index)
            closed_nodes += [current]

            #CREATION DE LA LISTE RETOUR
            if current[0] == posTask:
                verif = False
                robot_move_node = current
                retour = [] 
                while verif == False :
                    if robot_move_node[4] == [-1,-1]:
                        verif = True
                    for i in range(len(closed_nodes)):
                        if closed_nodes[i][0] == robot_move_node[4]:
                            robot_move_node = closed_nodes[i]
                    if robot_move_node[0][0] != self.x or robot_move_node[0][1] != self.y : 
                        if self.needLoading() :
                            retour = [robot_move_node[0]+self.detectLoading(city)] + retour
                        else :
                            retour = [robot_move_node[0]+self.detectTask(city)] + retour
                retour += [[posTask[0],posTask[1],posTask[0],posTask[1]]]
                return retour

            #AJOUT DES VOISINS DANS L'OPEN_NODES
            for i in self.getNeighbours((current[0][0],current[0][1]),(self.x,self.y),posTask,city):
                if city.getCel(i[0][0],i[0][1]).status != "building" and self.isNodeInTheList(i,closed_nodes) == False and self.isNodeInTheList(i,open_nodes) == False :
                        open_nodes+=[i+[[current[0][0],current[0][1]]]]
    
    def determineNodesInfos(self,pos,start,goal)->list:
        """
        Revoie les données relative à un noeud dans le cadre de l'algorithme A*
        ***Param***
        pos tuple - comportant les coordonneés du noeud. \n
        start tuple - comportant les coordonnées du noeud de départ. \n
        goal tuple - comportant les coordonnées du noeud d'arrivée (en général les coordonnées d'une tâche).
        ***Return***
        liste comportant les informations relatives au noeud sous le format suivant: \n
                                                [[position x du noeud, position y du noeud], \n
                                                 G cost (distance depuis le noeud de début), \n
                                                 H cost (distance depuis le noeud d'arrivée), \n
                                                 F cost = G + H, \n
                                                 [posistion x du noeud parent, position y du noeud parent] (non fourni par cette méthode)]
        """
        # [0] = position du noeud, [1] = G cost (distance depuis le début), [2] = H cost (distance depuis l'arrivée), [3] F cost = G + H, [4] = pos parent
        return [[pos[0],pos[1]], abs(pos[0]-start[0])+abs(pos[1]-start[1]), abs(pos[0]-goal[0])+abs(pos[1]-goal[1]), abs(pos[0]-start[0])+abs(pos[1]-start[1])+abs(pos[0]-goal[0])+abs(pos[1]-goal[1])]

    def getNeighbours(self,pos,start,goal,city) : #surement pb sortie de grille
        """
        Renvoie les noeuds voisins d'un noeud mis en paramètre
        ***Param***
        pos tuple - comportant les coordonneés du noeud. \n
        start tuple - comportant les coordonnées du noeud de départ. \n
        goal tuple - comportant les coordonnées du noeud d'arrivée (en général les coordonnées d'une tâche). \n
        city (city::Class) - Ville dans laquelle le noeud se trouve.
        ***Return***
        liste de listes d'information de noeuds.
        liste comportant les informations relatives au noeud sous le format suivant:
                                                [[position x du noeud, position y du noeud],
                                                 G cost (distance depuis le noeud de début),
                                                 H cost (distance depuis le noeud d'arrivée),
                                                 F cost = G + H,
                                                 [posistion x du noeud parent, position y du noeud parent] (non fourni par cette méthode)]
        """
        retour = []
        if pos[0] > 0:
            retour += [self.determineNodesInfos((pos[0]-1,pos[1]),start,goal)] 
        if pos[0] < city.sizeX-1:
            retour += [self.determineNodesInfos((pos[0]+1,pos[1]),start,goal)]
        if pos[1] > 0:
            retour += [self.determineNodesInfos((pos[0],pos[1]-1),start,goal)] 
        if pos[1] < city.sizeY-1:
            retour += [self.determineNodesInfos((pos[0],pos[1]+1),start,goal)] 
        return retour
    
    def isNodeInTheList(self,node,liste):
        """
        Permet de savoir si un noeud mis en paramètre est dans une liste passé en paramètre
        ***Param***
        node - liste comportant les informations relatives à un noeud \n
        liste - liste dans laquelle est effectuée la recherche, composée de plusieurs noeuds 
        ***Return***
        booléen indiquant si le noeud est présent dans la liste ou non.
        """
        for i in liste:
            if node[0] == i[0]:
                return True
        return False

    def findTaskFrom00(self,city)->list:
        """
        Trouve la tâche en balayant la ville du haut gauche vers bas droite de façon horizontale puis verticale.
        ***Return***
        liste comportant les coordonnées de la tâche.
        """
        for i in range(city.sizeX):
            for j in range(city.sizeY):
                if city.getCel(j,i).status == "task":
                    return [j,i]
        return [-1,-1]

    def findTaskFromRobotPos(self,city,currentAuction)->list:
        """
        Trouve la tâche en balayant la ville autour du robot.
        ***Param***
        city (City::class) - Ville dans laquelle le robot évolue
        currentAuction bool - Permet de savoir si une tâche d'enchère est en cours ou non
        ***Return***
        liste comportant les coordonnées de la tâche.
        """
        initialPos = (self.x,self.y)
        digit = [-1,0,1]
        currentDigit = 1
        markedTaskCounter = []
        while len(city.tasks) > 0 and len(markedTaskCounter) < len(city.tasks) and len(digit) <= city.sizeX*2+1 and len(digit) <= city.sizeY*2+1:
            permut = itertools.product(digit,repeat=2)
            for i in permut:
                if initialPos[0]+i[0]>=0 and initialPos[0]+i[0]<city.sizeX and initialPos[1]+i[1]>=0 and initialPos[1]+i[1]<city.sizeY and city.getTask(initialPos[0]+i[0],initialPos[1]+i[1]) !="ERROR" :
                    if (city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])].typeT == "auction" and currentAuction == False) or city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])].typeT == "base" :
                        if self.isTaskMarked(city,city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])]) == False :
                            #print("le robot : ",self.team," marque la case :", city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])].x, " / ", city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])].y)
                            self.markedTask = city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])]
                            return [initialPos[0]+i[0],initialPos[1]+i[1]]
                        elif city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])] not in markedTaskCounter :
                            markedTaskCounter += [city.tasks[city.getTask(initialPos[0]+i[0],initialPos[1]+i[1])]]
            currentDigit+=1
            digit = [-currentDigit] + digit
            digit += [currentDigit]
        return [-1,-1]

    def findLoadingFromRobotPos(self,city)->list:
        """
        Trouve la case de recharge en balayant la ville autour du robot.
        ***Param***
        city (City::class) - Ville dans laquelle le robot évolue
        ***Return***
        liste comportant les coordonnées de la tâche.
        """
        initialPos = (self.x,self.y)
        digit = [-1,0,1]
        currentDigit = 1
        while len(city.tasks) > 0:
            permut = itertools.product(digit,repeat=2)
            for i in permut:
                if initialPos[0]+i[0]>=0 and initialPos[0]+i[0]<city.sizeX and initialPos[1]+i[1]>=0 and initialPos[1]+i[1]<city.sizeY and city.getCel(initialPos[0]+i[0],initialPos[1]+i[1]).charge == True:
                    return [initialPos[0]+i[0],initialPos[1]+i[1]]
            currentDigit+=1
            digit = [-currentDigit] + digit
            digit += [currentDigit]
        return [-1,-1]
    
    def needLoading(self) -> bool :
        """
        Permet de savoir si un robot a besoin de passer à une station de rechargement ou non.
        ***Return***
        bool True si le robot a besoin de se recharger, False sinon.
        """
        if self.batteryLevel <= 20 :
            return True
        return False

    def detectLoading(self, city)->list:
        """
        Permet de savoir si un robot est présent sur une case de rechargement ou non.
        ***Param***
        city (City::class) - ville dans laquelle la tâche est détectée.
        ***Return***
        liste contenant les coordonnées de la case de recharge si le robot est dessus.  \n
        [-1,-1] si le robot n'est sur aucune case de rechargement.
        """
        if city.getCel(self.x,self.y).charge == True:
            return [self.x,self.y]
        return [-1,-1]
    
    def isTaskMarked(self, city, task):
        """
        Permet de savoir si la tâche passée en paramètre est marquée par un autre robot ou non
        ***Param***
        city (City::class) - ville dans laquelle la tâche et le robot se trouvent.
        task (Task::class) - tâche dont on vérifie la disponibilité.
        ***Return***
        bool valant vrai si la tâche est marquée par un robot, faux sinon.
        """
        retour = False
        for i in range(len(city.teams)):
            for j in range(len(city.teams[i].robots)):
                if city.teams[i].robots[j].markedTask == task :
                    retour = True
        return retour
        

    def showbattery(self, meter):
        """
        Affichage de la barre de chargement du robot en fonction de son niveau decharge actuel
        ***Param***
        meter - barre de chargement
        """
        battery = self.batteryLevel
        meter.config(value=battery/100)
        if battery > 80:
            meter.config(fill="green")
        if battery < 70:
            meter.config(fill="yellow")
        if  battery < 50:
            meter.config(fill="orange")
        if battery < 30:
            meter.config(fill="red")
        meter.update()        
