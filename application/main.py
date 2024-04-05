from flask import Flask, render_template
from datetime import timedelta
from models.dbConecction import Database,uri
from blueprints.app_blueprint import app_routes
from blueprints.user_blueprint import user_routes


def create_app():
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html")

    app.register_blueprint(app_routes)
    app.register_blueprint(user_routes)

    app.secret_key = 'Secret'

    app.permanent_session_lifetime = timedelta(minutes = 3)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app

create_app()