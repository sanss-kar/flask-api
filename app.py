from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:sanskar@localhost/Resturant"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Registration(db.Model):
    __tablename__ = "registration"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    confirm_password = db.Column(db.String(100))

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/registration", methods=['POST'])
def registration():
    data = request.get_json()  # Receive JSON data

    user_name = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    print(user_name, email, password, confirm_password)

    new_user = Registration(
        username=user_name,
        email=email,
        password=password,
        confirm_password=confirm_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"{user_name} inserted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
