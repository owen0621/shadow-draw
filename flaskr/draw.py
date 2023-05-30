from flask import Blueprint, render_template, request, abort, redirect, url_for
from sqlalchemy.orm import sessionmaker

from database import Session, User, Ensurance, Rent_history

draw_blueprint = Blueprint("draw", __name__, template_folder="templates")


# homepage for user
@draw_blueprint.route("/")
def user_root():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")
    # access the copy of db via orm
    session = Session()
    user = session.get(User, int(card_id))
    session.close()
    if user is None:
        abort(404, "User not found")

    return render_template("user_root.html", user=user)


# user profile page
@draw_blueprint.route("/profile")
def user_profile():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")
    # access the copy of db via orm
    session = Session()
    user = session.get(User, int(card_id))  # get user by pk
    ensures = (
        session.query(Ensurance).filter_by(CardID=int(card_id)).all()
    )  # get ensurances by attibute cardId
    session.close()
    if user is None:
        abort(404, "User not found")

    return render_template("user_profile.html", user=user, ensures=ensures)


# user history page
@draw_blueprint.route("/history")
def user_history():
    # get cardId from request arguments
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(400, "Parameter not found")
    # access the copy of db via orm
    session = Session()
    user = session.get(User, int(card_id))  # get user by pk
    histories = (
        session.query(Rent_history).filter_by(User_cardID=int(card_id)).all()
    )  # get histories by attibute cardId
    session.close()
    if user is None:
        abort(404, "User not found")

    return render_template("user_history.html", user=user, histories=histories)


# get and post the renting info
@draw_blueprint.route("/rent", methods=["POST", "GET"])
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
        # access the copy of db via orm
        session = Session()
        user = session.get(User, int(card_id))
        session.close()
        if user is None:
            abort(404, "User not found")
        return render_template("user_rent.html", user=user)
