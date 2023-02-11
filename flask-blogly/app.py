"""Blogly application."""

from flask import Flask, redirect, render_template, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

# app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.route("/")
def root():   
    """homepage that redirects to list of users"""

    return redirect('/users')



@app.route("/users")
def show_users():
    """show all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)



@app.route("/users/new", methods= ["GET"])
def show_add_form():
    """show form to add new users"""

    return render_template("newuser.html")



@app.route("/users/new", methods=["POST"])
def add_new_user():
    """process add from, add new user and  redirect back to /users"""

    new_user = User(
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")



@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show info on specific user using user-id"""


    user = User.query.get_or_404(user_id)
    return render_template('show_users.html', user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_page(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_users(user_id):
    """process edit form and update user"""


    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"] or None

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete the user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
