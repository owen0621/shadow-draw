from flask import Blueprint, render_template, jsonify, request, abort, url_for, redirect
from database import db


user_blueprint = Blueprint('user', __name__, template_folder='templates')

# homepage for user
@user_blueprint.route("/")
def user_root():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")
        
    # query data from db
    cursor = db.connection.cursor()
    cursor.execute(f'''
        SELECT * FROM User
        WHERE CardID = {card_id};
    ''')
    user = cursor.fetchone()
    if user is None:
        abort(404, "User not found")
    cursor.close()

    return render_template("user_root.html", user=user)


# user profile page
@user_blueprint.route("/profile")
def user_profile():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")

    # query data from db
    cursor = db.connection.cursor()

    # query user data
    cursor.execute(f'''
        SELECT * FROM User
        WHERE CardID = {card_id};
    ''')
    user = cursor.fetchone()
    if user is None:
        abort(404, "User not found")

    # query user's ensurance data
    cursor.execute(f'''
        SELECT * FROM Ensurance
        WHERE CardID = {card_id};
    ''')
    ensures = cursor.fetchall()

    return render_template("user_profile.html", user=user, ensures=ensures)


# user history page
@user_blueprint.route("/history")
def user_history():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")

    # query data from db
    cursor = db.connection.cursor()

    # query user data
    cursor.execute(f'''
        SELECT * FROM User
        WHERE CardID = {card_id};
    ''')
    user = cursor.fetchone()
    if user is None:
        abort(404, "User not found")

    # query user's rent_history data
    cursor.execute(f'''
        SELECT * FROM Rent_history
        WHERE User_cardID = {card_id};
    ''')
    histories = cursor.fetchall()
    cursor.close()

    return render_template("user_history.html", user=user, histories=histories)


# get and post the renting info
@user_blueprint.route("/rent", methods=["POST", "GET"])
def user_rent():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")

    # post: redirect to renting api
    if request.method == "POST":
        bike_serial = request.form["bsf"]
        return redirect(
            url_for("api.user_rent_api", bike_serial=bike_serial, card_id=card_id)
        )
    # get: generate the form to gather the renting info
    else:
        # query data from db
        cursor = db.connection.cursor()
        cursor.execute(f'''
            SELECT * FROM User
            WHERE CardID = {card_id};
        ''')
        user = cursor.fetchone()
        if user is None:
            abort(404, "User not found")
        cursor.close()

        return render_template("user_rent.html", user=user)

# FROM HERE
# get and post the returning info
@user_blueprint.route("/return", methods=["POST", "GET"])
def user_return():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")

    # post: redirect to renting api
    if request.method == "POST":
        is_broken = request.form["ibf"]
        park_loc = request.form["plf"]
        return redirect(
            url_for(
                "api.user_return_api",
                card_id=card_id,
                is_broken=is_broken,
                park_loc=park_loc,
            )
        )
    # get: generate the form to gather the renting info
    else:
        # query data from db
        cursor = db.connection.cursor()
        cursor.execute(f'''
            SELECT * FROM User
            WHERE CardID = {card_id};
        ''')
        user = cursor.fetchone()
        if user is None:
            abort(404, "User not found")
        
        cursor.execute(f'''
            SELECT Name FROM Location;
        ''')
        stops = cursor.fetchall()
        cursor.close()

        return render_template("user_return.html", user=user, stops=stops)

# renting api
@user_blueprint.route("/list", methods=["POST", "GET"])
def user_list():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")

    # post: redirect to renting api
    if request.method == "POST":
        input_loc = request.form["lf"]
        return redirect(url_for("api.user_list_api", card_id=card_id, input_loc=input_loc))
    # get: generate the form to gather the renting info
    else:
        # query data from db
        cursor = db.connection.cursor()
        cursor.execute(f'''
            SELECT * FROM User
            WHERE CardID = {card_id};
        ''')
        user = cursor.fetchone()
        if user is None:
            abort(404, "User not found")
        
        cursor.execute(f'''
            SELECT Name FROM Location;
        ''')
        stops = cursor.fetchall()
        cursor.close()

        return render_template("user_list_form.html", user=user, stops=stops)
