from flask import render_template, redirect, url_for, request, session, flash, Blueprint, jsonify
from models.dbConecction import Task 
from models.dbConecction import Database, uri
from blueprints.app_blueprint import session
import json

db = Database(uri, "Cluster0", "database_products.test")

user_routes = Blueprint("user_routes", __name__,
                       template_folder="templates",
                       static_folder="static")

# Admin
@user_routes.route("/user/admin", methods=["POST","GET"])
def user_admin():
    
    if request.method == "GET":
        users = db.get_usernames()
        return render_template("admin.html", users=users, session=session)

    elif request.method == "POST":
        
        task_title = request.form["task_title"]
        task_due_date = request.form["task_due_date"]
        task_description = request.form["task_description"]
        task_assignee = request.form["task_assignee"]
        
        if any([task_title == "", task_due_date == "", task_description == "", task_assignee == ""]): # verificamos que todos los datos esten completos antes de instanciar un Task
            flash("Error al crear la Task")
            return redirect(url_for("user_routes.user_admin"))
        else:
            new_task = Task(task_title,task_due_date,task_description,task_assignee,session["user_name"])
            
            if db.insert_task(new_task):
                flash("Task creada correctamente !!")
                return redirect(url_for("user_routes.user_admin"))
            else: 
                flash("Error al crear la task")
                return render_template("admin.html")
 
    
# Admin privileges
@user_routes.route("/user/admin/privileges", methods=["POST"]) # Le pegamos a otro endpoint para que el codigo sea mas legible 
def user_admin_privileges():
     
    if request.method == "POST": # Esto debería ser un PUT, pero la etiqueta form de html por defecto no permite enviar PUT reqs 
    
        target_user = request.form["user_target"]
        pressed_button = request.form["button"] # obtenemos el boton que se presionó
        
        if pressed_button == "Revoke privileges":
            db.update_privileges_user(target_user,False)
            flash("Privileges revoked")
        else:
            db.update_privileges_user(target_user,True)
            flash("Privileges granted")
        return redirect(url_for("user_routes.user_admin"))
       
# Inbox
@user_routes.route("/user/inbox",methods=["POST","GET"])
def user_inbox():
    if request.method == "GET":
        return render_template("inbox.html", tasks = db.get_tasks(session["user_name"]))

    elif request.method == "POST": # Esto tambíen debería ser un PUT, pero la etiqueta form de html por defecto no permite enviar PUT reqs
        value = request.form["args"]
        json_req = json.loads(value)
        print(db.update_status_task(json_req))
        return render_template("inbox.html", tasks = db.get_tasks(session["user_name"]))
    
    
# Done tasks   
@user_routes.route("/user/done/", methods=["PUT","GET"])
def user_done():
    if request.method == "GET":   
        return render_template("done.html", tasks = db.get_tasks(session["user_name"]))
    
    