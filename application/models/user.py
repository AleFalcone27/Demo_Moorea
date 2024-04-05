class User:
    def __init__(self,name:str, email:str, password:str) -> None:
        
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = False

