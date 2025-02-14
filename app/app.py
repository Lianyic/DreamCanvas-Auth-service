import os
import mysql.connector
import bcrypt
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")


DATABASE_URL = os.getenv("DATABASE_URL", "mysql://adminuser:YourSecurePassword!@127.0.0.1/dreamcanvas-user-db")


db_config = {
    "host": DATABASE_URL.split("@")[1].split("/")[0],
    "user": DATABASE_URL.split("//")[1].split(":")[0],
    "password": DATABASE_URL.split(":")[2].split("@")[0],
    "database": DATABASE_URL.split("/")[-1]
}


@app.route("/")
def home():
    background_image = "images/background.webp"
    return render_template("login.html", background_image=background_image)


@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json 
        username = data["username"]
        email = data["email"]
        password = data["password"]

        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()


        query = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()


        if user and bcrypt.checkpw(password.encode("utf-8"), user[0].encode("utf-8")):
            return jsonify({"message": "Login successful!"}), 200
        return jsonify({"error": "Invalid credentials!"}), 401
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)