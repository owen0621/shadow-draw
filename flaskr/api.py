from flask import Blueprint, render_template, jsonify, request, abort, url_for, redirect
from database import db


api_blueprint = Blueprint('api', __name__, template_folder='templates')

# renting api
@api_blueprint.route("/user/rent")
def user_rent_api():
    # get cardId and bike serial from request arguments
    card_id = request.args.get("card_id")
    bike_serial = request.args.get("bike_serial")
    if card_id is None or bike_serial is None:
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

    if user is None:  # if user not exist
        print("User not found")
        abort(404, "User not found")
    elif user['Rent_bike_serial'] is not None:  # if user already rent a bike
        print("User can't rent")
        abort(404, "User can't rent")
    
    # query bike data
    cursor.execute(f'''
        SELECT * FROM Bike
        WHERE Serial_num = {bike_serial}
    ''')
    bike = cursor.fetchone()
    if bike is None:  # if bike not exist
        print("Bike not found")
        abort(404, "Bike not found")
    elif bike['Is_using'] is True or bike['Is_broken'] is True:  # if bike is not avalible
        print("Bike is not avalible")
        abort(404, "Bike is not avalible")

    # update db data
    cursor.execute(f'''
        UPDATE Bike
        SET Is_using = 1
        WHERE Serial_num = {bike_serial};
    ''')
    db.connection.commit()
    cursor.execute(f'''
        UPDATE User
        SET Rent_bike_serial = {bike_serial}
        WHERE CardID = {card_id};
    ''')
    db.connection.commit()

    # redirct to user homepage
    return redirect(url_for("user.user_root", card_id=card_id))

# returning api
@api_blueprint.route("/user/return")
def user_return_api():
    # get cardId and bike serial from request arguments
    card_id = request.args.get("card_id")
    is_broken = True if request.args.get("is_broken") == 'y' else False
    park_loc = request.args.get("park_loc")
    if card_id is None or is_broken is None or park_loc is None:
        abort(400, "Parameter not found")

    # query data from db
    cursor = db.connection.cursor()

    # query user data
    cursor.execute(f'''
        SELECT * FROM User
        WHERE CardID = {card_id};
    ''')
    user = cursor.fetchone()
    if user is None:  # if user not exist
        abort(404, "User not found")
    elif user['Rent_bike_serial'] is None:  # if user is not renting a bike
        abort(404, "User isn't renting")

    # query bike data
    # 這裡或許不用檢查
    cursor.execute(f'''
        SELECT * FROM Bike
        WHERE Serial_num = {user['Rent_bike_serial']}
    ''')
    bike = cursor.fetchone()
    if bike is None:  # if bike not exist
        abort(404, "Bike not found")
    elif bike['Is_using'] is False or bike['Is_broken'] is True:  # unexpected error
        abort(500, "Something went wrong in table Bike")

    # query location data
    cursor.execute(f'''
        SELECT * FROM Location
        WHERE Name = '{park_loc}'
    ''')
    location = cursor.fetchone()
    if location is None:  # if location not found
        abort(404, "Location not found")

    cursor.execute(f'''
        SELECT MAX(History_serial) FROM Rent_history
    ''')
    max_history_serial = cursor.fetchone()['MAX(History_serial)']

    cost = 100  # TODO: calculate cost
    time = 1234  # TODO: obtain rent time
    start_loc = bike['Park_loc']  # location that the cat is rented
    
    # update db data
    cursor.execute(f'''
        UPDATE User
        SET Rent_bike_serial = NULL
        WHERE CardID = {card_id};
    ''')
    db.connection.commit()
    cursor.execute(f'''
        UPDATE Bike
        SET 
            Is_using = 0, 
            Is_broken = {1 if is_broken else 0},
            Park_loc = '{park_loc}'
        WHERE Serial_num = {user['Rent_bike_serial']};
    ''')
    db.connection.commit()

    # insert new rent history
    cursor.execute(f'''
        INSERT INTO Rent_history (
            Start_loc,
            Stop_loc,
            Bike_serial,
            User_cardID,
            History_serial,
            Cost,
            Time
        )
        VALUES (
            '{start_loc}', 
            '{park_loc}', 
            {user['Rent_bike_serial']}, 
            {card_id}, 
            {max_history_serial + 1},
            {cost},
            {time}
        );
    ''')
    db.connection.commit()

    # redirct to user homepage
    return redirect(url_for("user.user_root", card_id=card_id))

@api_blueprint.route("/user/list")
def user_list_api():
    card_id = request.args.get("card_id")
    input_loc = request.args.get("input_loc")
    if card_id is None or input_loc is None:
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

    # query location data
    cursor.execute(f'''
        SELECT * FROM Location
        WHERE Name = '{input_loc}'
    ''')
    location = cursor.fetchone()
    if location is None:  # if location not found
        abort(404, "Location not found")
    
    cursor.execute(f'''
        SELECT * FROM Bike
        WHERE Park_loc = '{input_loc}'
    ''')
    bikes = cursor.fetchall()
    cursor.close()

    return render_template("user_list_result.html", user=user, bikes=bikes)
