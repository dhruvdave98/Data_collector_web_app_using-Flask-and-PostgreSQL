# -----------------------------------------------------------
# Demonstrates the application, which requires the email address and height of the user,
# after entering the data, system sends an email to the given email address regarding
# the height of the user and average height of that height group from available
# record in the database.
# This web app has been developed using flask and POSTGRESSql as a database.
#
# email dhruvdave61@gmail.com
# ----------------------------------------------------------
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)

# connecting the postgresql database with the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/height_collector'
db = SQLAlchemy(app)


class Data(db.Model):
    # defining table name and its columns
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height


# home page of the application
@app.route("/")
def index():
    return render_template("index.html")


# success page, which processes the input from the user
@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        # get the input from the user
        email = request.form["email_name"]
        height = request.form["height_name"]

        # filtering the email address, if the redundant email found in the database,
        # it will return index page with the user-friendly message
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            data = Data(email, height)

            # adding data to the database
            db.session.add(data)
            db.session.commit()

            # counting the average height from the available database record
            average_height = db.session.query(func.avg(Data.height)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height).count()

            # sending email to the given email address
            send_email(email, height, average_height, count)
            return render_template("success.html")

        # rendering the index page with user-friendly message
        return render_template("index.html", text="Seems like we've got something from that email address already")


if __name__ == '__main__':
    app.debug = True
    app.run()
