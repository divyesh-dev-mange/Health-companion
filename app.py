from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "your_secret_key"
CORS(app)

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["health_companion"]
users_collection = db["users"]

@app.route("/")
def home():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email already exists"})

        users_collection.insert_one({"name": name, "email": email, "password": password})
        return jsonify({"success": True, "redirect": url_for("login")})

    return render_template("register.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email, "password": password})
    if user:
        session["user"] = user["email"]
        return jsonify({"success": True, "redirect": url_for("dashboard")})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
