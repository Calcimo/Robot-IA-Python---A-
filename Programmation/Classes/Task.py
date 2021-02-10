class Task:
    
    def __init__(self,x,y,pointValue,typeT="base"):
        """
        Constructeur de la classe Task
        ***Param***
        int x - Position x de la case (N,S,E,O) \n
        int y - Position y  de la case (N,S,E,O) \n
        pointValue - Valeur de points de la tâche \n
        typeT - Type de la tâche
        """
        self.x = x
        self.y = y
        self.pointValue = pointValue
        self.typeT = typeT 
        self.belongsTo = "noOne"

    def addTask(self, city):
        """
        Ajoute une tâche à la liste City.tasks
        ***Param***
        task (Task::class) - tâche à ajoutée à la liste
        """
        if city.getCel(self.x,self.y).status == "route":
            city.tasks.append(self)
            city.getCel(self.x,self.y).status = "task"