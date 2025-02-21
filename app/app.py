import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
import redis
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
import bcrypt

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "79515e01fd5fe2ccf7abaa36bbea4640")

CORS(app, supports_credentials=True)

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://adminuser:password@your-database.mysql.database.azure.com/dream_user_db").strip('"')
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_REDIS"] = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "dreamcanvas-redis.redis.cache.windows.net"),
    port=int(os.getenv("REDIS_PORT", 6380)),
    password=os.getenv("REDIS_PASSWORD", "Si4eQ7Gt1G1jFDmXcR9X7zxqJSwOhBuAzCaOdCV8c="),
    ssl=True,
    decode_responses=True
)


Session(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

@app.route("/")
def home():
    return render_template("login.html")

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

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already exists. Please choose another one."}), 400

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
            session["username"] = username
            return jsonify({"message": "Login successful!"}), 200

        return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out successfully!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)