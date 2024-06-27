import sqlite3
from datetime import date, datetime
from flask import Flask, g, request, jsonify
from flask_cors import CORS
import math
import time

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})

app.config["DATABASE"] = "../db/master.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
    return db

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

#GET ALL POOPS
@app.route("/api/poops/", methods=["GET"])
def get_poops():

    #REMOVE AFTER TESTING -START
    time.sleep(2)
    #REMOVE AFTER TESTING -END
    cursor = get_db().cursor()

    cursor.execute("SELECT * FROM poops")

    rows = cursor.fetchall()

    data_list = []

   
    for row in rows:
        age = get_poop_age_days(row[7], row[8]) if row[8] is not None else get_poop_age_days(row[7], date.today().strftime("%Y-%m-%d"))
        data = {
            "poopId": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "description": row[3],
            "status": row[4],
            "placedUserId": row[5],
            "pickedUserId": row[6],
            "startDate": row[7],
            "endDate": row[8],
            "age": age,
            "bounty": math.ceil(exponential_equation(age, .2, 0.1) * 10 + age)  #bounty increases exponentially with age
        }
        data_list.append(data)
    return data_list

#GET POOPS BY USERID
@app.route("/api/poops/placeduser/<user_id>", methods=["GET"])
def get_poops_user(user_id):
    cursor = get_db().cursor()

    cursor.execute(f"SELECT * FROM poops WHERE placed_user_id = ?", (user_id))

    rows = cursor.fetchall()

    data_list = []

    for row in rows:
        age = get_poop_age_days(row[7], row[8]) if row[8] is not None else get_poop_age_days(row[7], date.today().strftime("%Y-%m-%d"))
        data = {
            "poopId": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "description": row[3],
            "status": row[4],
            "placedUserId": row[5],
            "pickedUserId": row[6],
            "startDate": row[7],
            "endDate": row[8],
            "age": age,
            "bounty": math.ceil(exponential_equation(age, .2, 0.1) * 10 + age) #bounty increases exponentially with age
        }
        data_list.append(data)
    return data_list

#UPDATE POOP
@app.route("/api/poops/<poop_id>", methods=["POST"])
def update_poop(poop_id):
    #REMOVE AFTER TESTING -START
    time.sleep(2)
    #REMOVE AFTER TESTING -END
    data = request.json
    cursor = get_db().cursor()
    cursor.execute("UPDATE poops SET state = ?, completed_date = ?, picked_user_id = ?  WHERE poop_id = ?", (data['state'], data['completedDate'], data['pickedUserId'], poop_id))
    get_db().commit()
    print(data['state'])
    return {"message": data}

#CREATE POOP
@app.route("/api/poops/", methods=["POST", "OPTIONS"])
def create_poop():
    #REMOVE AFTER TESTING -START
    time.sleep(2)

    data = request.json
    #REMOVE AFTER TESTING -END
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO poops (latitude, longitude, description, state, placed_user_id, picked_user_id, created_date, completed_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (data['latitude'], data['longitude'], data['description'], data['state'], data['placedUserId'], data['pickedUserId'], data['createdDate'], data['completedDate']))
    get_db().commit()

    max_record = None
    max_value = float('-inf')  # Start with a very low value

    poops_data = get_poops()
    for record in poops_data:
        value = record['poopId']
        if value > max_value:
            max_value = value
            max_record = record

    return jsonify({"message": "New poop record created", "result": max_record})

@app.route("/api/achievements/<user_id>", methods=["GET"])
def get_achievements_user(user_id):
    cursor = get_db().cursor()

    cursor.execute(f"SELECT * FROM poops WHERE picked_user_id = {user_id}")

    rows = cursor.fetchall()

    points_sum = 0
    poops_sum = 0

    for row in rows:
        if row[4] == "completed":
            points_sum += get_poop_age_days(row[7], row[8])
            poops_sum += 1

    data = {"userId": user_id, "totalPoopsPicked": poops_sum, "totalPoints": points_sum}

    return data


def get_poop_age_days(date1, date2):
    start_date = datetime.strptime(date1, "%Y-%m-%d")
    end_date = datetime.strptime(date2, "%Y-%m-%d")

    delta = end_date - start_date
    age = delta.days

    return age

def exponential_equation(x, k, a):
    return k * math.exp(a * x)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


