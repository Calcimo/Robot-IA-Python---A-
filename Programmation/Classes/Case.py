class Case :
    
    def __init__(self,x,y,status="route", charge=False):
        """
        Constructeur de la classe Case
        ***Param***
        int x - Position x de la case (N,S,E,O) \n
        int y - Position y  de la case (N,S,E,O) \n
        str status - Indicateur du type de la case (route, building (bâtiment),task (tâche))\n
        bool charge - Indique si la case permet la recharge du robot
        """
        self.x = x
        self.y = y
        self.status = status
        self.charge = charge

    def __str__(self):
        """
        Méthode to_string permettant l'accès aux informations relatives à la case
        ***Return***
        str Comportant les coordonnées de la case ainsi que son type (status)
        """
        return "Case : " + str(self.x) + " horizontal, " + str(self.y) + " vertical et son status est "+ str(self.status) 