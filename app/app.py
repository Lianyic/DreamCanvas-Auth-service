import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import bcrypt

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://adminuser:LeilaLily?!@dreamcanvas-user-db.mysql.database.azure.com/dream_user_db"
).strip('"')

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 用户表模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

@app.route("/")
def home():
    background_image = "images/background.webp"
    return render_template("login.html", background_image=background_image)

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json 
        username = data["username"]
        password = data["password"]

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return jsonify({"message": "Login successful!"}), 200
        return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)