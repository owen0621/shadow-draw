from flask import Flask, render_template

# from flask_sqlalchemy import SQLAlchemy


import logging

from database import app
from draw import draw_blueprint
from api import api_blueprint


# app = Flask(
#     __name__,  # the name of the current file
#     static_url_path="/python",  # access static file via /python/filename
#     static_folder="static",  # the folder where static files at
#     template_folder="templates",  # the folder where templates files at
# )
# # db config
# app.app_context().push()
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "mysql://root:password@localhost/Youbike"  # mod by your self
# db = SQLAlchemy(app)
# Session = sessionmaker(bind=db.engine)
# add console log
app.logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)


# root
@app.route("/")
def index():
    return "Draw"


# register blueprint
app.register_blueprint(draw_blueprint, url_prefix="/draw")
app.register_blueprint(api_blueprint, url_prefix="/api")


# error handler 404
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(str(error))
    return render_template("404.html"), 404


# error handler 400
@app.errorhandler(400)
def parameter_not_found_error(error):
    app.logger.error(str(error))
    return render_template("400.html"), 400


# error handler 500
@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(str(error))
    return render_template("500.html"), 500


# default error handler
@app.errorhandler(Exception)
def default_error_handler(error):
    app.logger.error(str(error))
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run()
