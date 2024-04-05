from datetime import datetime

class Task:
    def __init__ (self, title:str ,due_date:datetime, description:str, assignee:str, assignor:str):
        self.tite = title
        self.due_date = datetime.strptime(due_date, "%d/%m/%Y")
        
        current_date_string = datetime.now().strftime("%d/%m/%Y")
        self.current_date = datetime.strptime(current_date_string, "%d/%m/%Y")
        
        self.description = description
        self.assignee = assignee
        self.assignor = assignor
        self.status = "pending"
        
    