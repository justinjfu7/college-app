from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask import session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.secret_key = "a_super_secret_key"

@app.route("/")
#checks if flask works
def home():
    return "Hello, Flask is working!"


class User(db.Model):
#creates the User object with attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

@app.route("/signup", methods=["POST"])
#signup route
def signup():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])
    role = data.get("role", "student")

    if User.query.filter_by(username=username).first():
        return {"error": "Username taken"}, 400

    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return {"message": "User created!"}, 201



@app.route("/login", methods=["POST"])
#login route
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password required"}, 400

    user = User.query.filter_by(username=username).first()
    session["user_ID"] = user.id
    session["role"] = user.role

    if not user:
        return {"error": "User not found"}, 404

    if check_password_hash(user.password, password):
        return {"message": f"Login successful!", "username": user.username, "role": user.role}, 200
    else:
        return {"error": "Incorrect password"}, 401
    


@app.route("/logout", methods=["POST"])
#logs the user out
def logout():
    session.clear()  # clears session and cookie
    return {"message": "Logged out successfully!"}

#html import belolw******************************************************
app = Flask(__name__, template_folder="templates")

@app.route("/")
def Search():
    return render_template("index.html")

@app.route("/home")
def Home():
    return render_template("home.html")\

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")
#End html import ***********************************************************
@app.route("/ping", methods=["GET"])
#test ping pong message
def ping():
    return jsonify({"message": "pong"})

with app.app_context():
    db.create_all()

import os
#verifies the right database is being reached
print("Database path:", os.path.abspath("database.db"))

if __name__ == "__main__":
    app.run(debug=True)
