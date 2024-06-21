import sqlite3
from datetime import date, datetime
from flask import Flask, g, request
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


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    # Example query
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM poops")
    rows = cursor.fetchall()
    return str(rows)


@app.route("/api/users/<user_id>", methods=["GET"])
def users(user_id):

    # Example query
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM user WHERE user_id = ?", (user_id))
    rows = cursor.fetchall()
    print(rows)
    data = ""
    for row in rows:
        print(rows)
        data = {
            "userId": row[0],
            "firstName": row[1],
            "lastName": row[2],
            "email": row[3],
            "active": row[4],
            "createdDate": row[5],
        }
        

    return data


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


@app.route("/api/poops/", methods=["POST"])
def create_poop():
    #REMOVE AFTER TESTING -START
    time.sleep(2)
    data = request.json
    #REMOVE AFTER TESTING -END
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO poops (latitude, longitude, description, state, placed_user_id, picked_user_id, created_date, completed_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (data['latitude'], data['longitude'], data['description'], data['state'], data['placedUserId'], data['pickedUserId'], data['createdDate'], data['completedDate']))
    get_db().commit()
    return {"message": "New poop record created"}

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

if __name__ == "__main__":
    app.run(debug=True)
