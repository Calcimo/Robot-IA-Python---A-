class Building:
    
    def __init__(self,x,y,sizeX,sizeY,bType):
        """
        Constructeur de la classe Building
        ***Param***
        int x - Position x de la case (N,S,E,O) \n
        int y - Position y  de la case (N,S,E,O) \n
        int sizeX - Taille X du bâtiment \n
        int sizeX - Taille Y du bâtiment \n
        str bType - Type du bâtiment (Bâtiment de décor, station de recharge)
        """
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.bType = bType

    def createBuilding(self, city):
        """
        Ajoute un bâtiment à la ville.
        ***Param***
        city (City::class) - bâtiment à ajouter à la ville
        """
        #gestion des status des cases
        for i in range(self.x,self.x+self.sizeX):
            for j in range(self.y,self.y+self.sizeY):
                city.getCel(i,j).status = "building"
        city.buildings += [self]