import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import sys
import time

load_dotenv()

app = Flask(__name__)
dburl = os.getenv("DATABASE_URL")
dbuser = os.getenv("DATABASE_USER")
dbport = os.getenv("DATABASE_PORT")
dbname = os.getenv("DATABASE_NAME")
dbpw    = os.getenv("DATABASE_PASSWORD")

connection = psycopg2.connect(
    user=dbuser,
    host=dburl,
    port=dbport,
    database=dbname,
    password=dbpw
)

INSERT_USER_RETURN_ID = "INSERT INTO users (name) VALUES (%s) RETURNING id;"
SELECT_ALL_USERS = "SELECT * FROM users"

@app.route("/users", methods=['GET', "POST"])
def users():
    if request.method=='POST':
        mydata = request.get_json()
        name = mydata["name"]
        with connection:
                with connection.cursor() as cursor:
                        cursor.execute(INSERT_USER_RETURN_ID, (name,))
                        user_id = cursor.fetchone()[0]
        return {"id": user_id, "name": name, "message": f"User {name} created."}, 201
    
    if request.method=='GET':
         with connection:
              with connection.cursor() as cursor:
                   cursor.execute(SELECT_ALL_USERS)
                   users = cursor.fetchall()
                   if users:
                        result = []
                        for user in users:
                             result.append({"id":user[0], "name": user[1]})
                        return jsonify(result), 200
                   else:
                        return jsonify({"error": f"Users not found."}), 404
         
@app.route("/users/<int:userid>", methods=['GET'])
def get_user(userid):
     with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", [userid])
            user = cursor.fetchone()
            if user:
                 return jsonify({"id": user[0], "name": user[1]}), 200
            else:
                 return jsonify({"error": f"User with ID {userid} not found"}), 404

@app.route('/liveness')
def healthx():
  time.sleep(2);
  return "<h1><center>Liveness check completed</center><h1>"
  
@app.route('/readiness')
def healthz():
  time.sleep(20);
  return "<h1><center>Readiness check completed</center><h1>"

@app.get("/")
def home():
    return "hello world"

if __name__=='__main__':
    app.run(debug=True)