from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from models.dbConecction import User 
from models.dbConecction import Database,uri

db = Database(uri, "Cluster0", "database_products.test")

app_routes = Blueprint("app_routes", __name__,
                       template_folder="templates",
                       static_folder="static")

# Root
@app_routes.route("/")
def index():
    return redirect(url_for("app_routes.login"))

# Login
@app_routes.route("/login", methods=["GET","POST"])
def login():
    
    if request.method == "POST":
        user_email = request.form["email"]
        user_pass = request.form["pass"]
        user = db.login(user_email,user_pass) 

        if user: 
            session.permanent = True
            session["user_name"] = user["username"]
            session["user_isadmin"] = user["is_admin"]
            return redirect(url_for("app_routes.user"))
    
        else: 
            flash("Credenciales erroneas",'error')
            return render_template("login.html")
    else:
        return render_template("login.html")
        
# Register
@app_routes.route("/register",methods=["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        user_name = request.form["name"]
        user_email = request.form["email"]
        user_pass = request.form["pass"]
        
        if any([user_name == "", user_email == "", user_pass == ""]): # verificamos que todos los campos esten completos antes de instanciar un User
            flash("Error al crear el usuario")
            return redirect(url_for("app_routes.register"))

        else:
            new_user = User(user_name,user_email,user_pass)
            
            if db.register(new_user):
                flash("Usuario registrado correctamente !!")
                return redirect(url_for("app_routes.login"))
            else: 
                flash("Error al crear el usuario")
                return render_template("register.html")

# LogOut
@app_routes.route("/logout", methods=["GET"])
def logout():
    if "user_name" in session:
        session.clear() # Limpiamos los datos de session
        flash("Cesión finalizada con éxito")
    else:
        flash("Debes iniciar cesión primero")
    return redirect(url_for("app_routes.login"))


# User profile
@app_routes.route("/user")
def user():
    
    if "user_name" in session:
        return render_template("user.html", user=session)
    
    else: 
        flash("Ingresa tus credenciales para iniciar cesion primero")
        return redirect(url_for("app_routes.login"))


