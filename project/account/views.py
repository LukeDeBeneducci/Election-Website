# IMPORTS #
from flask import render_template, url_for, request, redirect, session, flash, Blueprint, send_from_directory
from flask_login import login_required, current_user
from project import db
import os

# CONFIG #
account_blueprint = Blueprint('account', __name__, template_folder='templates')

## ROUTES ##

# Account Page: Requires login -> @login_required -> renders account.html page.
@account_blueprint.route('/account')
@login_required
def account():
    error = None
    return render_template("account.html", error = error)

# Vote Page: Requires login -> @login_required -> if user has not voted renders vote.html page.
# Let's user vote and updates their voted boolean in the database.
# If user has already voted redirects user back to the account page.
@account_blueprint.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if current_user.userdeets.voted == 0:
        if request.method == 'POST':
                current_user.userdeets.voted = 1
                db.session.commit()
                flash("Thank you for voting")
                return redirect(url_for('account.result'))
        return render_template("vote.html")
    if current_user.userdeets.voted == 1:
        flash("Already Voted")
        return  redirect(url_for("account.account"))

# Results Page: Requires login -> @login_required -> if user has aleady voted renders results.html page.
# If user has not voted redirects user back to the account page.
@account_blueprint.route('/results')
@login_required
def result():
    if current_user.userdeets.voted == 0:
        flash("You Must Vote First")
        return redirect(url_for("account.account"))
    if current_user.userdeets.voted == 1:
        return render_template("results.html")




