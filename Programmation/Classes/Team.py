import random
from Classes.Task import Task

class Team :

    def __init__(self,color):
        """
        Constructeur de la classe Case
        ***Param***
        int x - Position x de la case (N,S,E,O) \n
        int y - Position y  de la case (N,S,E,O) \n
        str status - Indicateur du type de la case (route, building (bâtiment),task (tâche))\n
        bool charge - Indique si la case permet la recharge du robot
        """
        self.robots = []
        self.point = 100
        self.color = color

    
    def addRobot(self,robot):
        """
        Ajoute un robot à la Team
        ***Param***
        robot - Robot ajouté
        """
        self.robots += [robot]


    def addPoint(self,point):
        """
        Ajoute les points obtenus par une tâche au score de l'équipe
        ***Param***
        point - Valeur du point
        """
        self.point += point

    def auctionAgainstOtherTeam(self,task,team):
        """
        Détermine à quelle équipe est remise une tâche sur le principe des enchères
        ***Param***
        task (Task::class) - tâche à départager \n
        team (Team::class) - 2e équipe voulant la tâche
        """
        verif = False
        currentTeam = 0
        bidAgain = 0.1
        while verif == False:
            if random.random() > bidAgain :
                bidAgain += 0.1
                currentTeam += 1
            else :
                verif = True
                if currentTeam%2 == 0 :
                    self.point -= bidAgain*100
                    task.belongsTo = self.color
                else:
                    team.point -= bidAgain*100
                    task.belongsTo = team.color
    
    def determineAuctionDealer(self, task)->bool:
        """
        Choisi quel robot va contester l'enchère avec l'équipe ennemie
        ***Param***
        task (Task::class) - tâche à départager
        ***Return***
        bool - Vrai si un robot a été choisi et se trouve à moins de 50 unités \n
        de distance de la tâche / Faux sinon
        """
        shortestDistance = 30
        winner = None
        for i in self.robots :
            robotDistance = abs(i.x-task.x) + abs(i.y-task.y)
            if robotDistance < shortestDistance :
                winner = i
                shortestDistance = robotDistance
        if shortestDistance >= 30 :
            return False
        winner.markedTask = task
        return True
                    