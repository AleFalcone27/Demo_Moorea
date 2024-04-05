from pymongo.mongo_client import MongoClient
from .user import User
from .task import Task
from bson import ObjectId

uri = "mongodb+srv://AleFalcone:Overyou200127@cluster0.guiv1nd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class Database:
    def __init__(self, db_uri, db_name, db_collection):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[db_collection]
    
    def login(self,email:str ,password:str):
        """ 
        Sumary:
            Verificar las credenciales para el inicio de sesion, confrontado los datos ingrsados con los registros de la base de datos
        
        Args:
            email (str): Email del usuario
            password (str): pasword del usuario
        
        Returns:
            El usuario si la condición se cumple, caso contrario Falso
        """
        
        user = self.collection.find_one({"email": email, "password":password})
        
        if user:
            return user
        else: 
            return False
        
        
    
    def register(self, user: User ) -> bool:
        """
        Sumary:
            Inserta un nuevo User en la base de datos
        
        Args:
            User (User): Instancia de User

        Returns:
            bool: True se insertaron correctamente los datos en la Bd, caso contrario False  
        """
        try:
            self.collection.insert_one({
                                "username": user.name,
                                "email": user.email,
                                "password": user.password,
                                "is_admin": user.is_admin
                            })
            return True
            
        except Exception as e:
            
            print("Error:", e)
            return ["Error: " + str(e)]
        
        
        
        
    def get_usernames(self):
        """
        Summary:
            Devuelve todos los nombres de la base de datos

        Returns:
            list: Lista de nombres de usuario
        """
        try:

            users = self.collection.find({"username": {"$exists": True}})
            usernames = []
            
            for user in users:
                usernames.append(user["username"])
            
            return usernames
        
        except Exception as e:
            
            print("Error:", e)
            return ["Error: " + str(e)]

        
    def insert_task(self, task: Task ) -> bool:
        """
        Sumary:
            Inserta una nueva Task en la base de datos
        
        Args:
            task (Task): Instancia de Task

        Returns:
            bool: True se insertaron correctamente los datos en la Bd, caso contrario False  
        """
        try:
            self.collection.insert_one({
                                "title": task.tite,
                                "due_date": task.due_date,
                                "current_date": task.current_date,
                                "description": task.description,
                                "assignee": task.assignee,
                                "assignor": task.assignor,
                                "status": "pending"
                            })
            return True
        except Exception as e:
            
            print("Error:", e)       
            return False
        
        
    
    def get_tasks(self, session_user_name:str) :
        """
        Sumary:
            Levanta de la bd todas las tareas asociadas al nombre de la session actual
        
        Args:
            session_user_name (str): Nombre del usuario de la session actual

        Returns:
            bool: True se insertaron correctamente los datos en la Bd, caso contrario False  
        """
        try:
            resultados = self.collection.find({"assignee": session_user_name})
            
            return resultados
        except Exception as e:
            print("Error:", e)       
            return {"message": "error"}



    def update_status_task(self, req):
        """
        Sumary:
            Modifica el estado de una tarea
        
        Args:
            req (json): Contiene el _id de la tarea a modificar y el estado al cual se va a cambiar

        Returns:
            bool: True si la modificación se hizo corectamente
        """
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(req["_id"])},
                {'$set': {'status': req["status"]}}
            )

            return True
        except Exception as e:
            
            print("Error:", e)
            return False
                                 


    def update_privileges_user(self, user_name:str, bool:bool):
        """
        Sumary:
            Modifica los permisos del usuario
        
        Args:
            user_name (str): Nombre del usuario al que se le an a modificar los permisos
            bool (bool): Indica si se van a dar perimsos o a revocar

        Returns:
            bool: True si la modificación se hizo corecta
        """
        try:
            
            result = self.collection.update_one(
                {'username': user_name},
                {'$set': {'is_admin': bool}}
             )

            return True
        except Exception as e:
            
            print("Error:", e)
            return False   

        