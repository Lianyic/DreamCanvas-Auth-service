import random
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates", static_folder="static")


BACKGROUND_IMAGES = [
    "images/background.webp",
    "images/background2.webp"
]

@app.route("/")
def home():
    background_image = random.choice(BACKGROUND_IMAGES)
    return render_template("login.html", background_image=background_image)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "test" and password == "1234":
        return "Login successful!"
    return "Invalid credentials!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
