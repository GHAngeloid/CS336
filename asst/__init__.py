from flask import Flask, render_template, flash
from peewee import MySQLDatabase, fn
import sys, traceback
import flask_login


def init_db():
    global DB
    DB = MySQLDatabase(host="ofmc.me",port=3306,user="cs336",passwd="password",database="cs336")


APP = Flask(__name__, template_folder="views/templates", static_url_path='/static')
APP.secret_key = 'A^*4L#Cs8UjQaq!Hjmhz'

LM = flask_login.LoginManager()
LM.init_app(APP)

init_db()

import asst.auth

# Register all views after here
# =======================
from asst.auth import auth_pages
from asst.views import register, feedback, management, reservation, stats
from asst.models import user


APP.register_blueprint(register.page, url_prefix='/register')
APP.register_blueprint(auth_pages, url_prefix='/auth')
APP.register_blueprint(feedback.page, url_prefix='/feedback')
APP.register_blueprint(management.page, url_prefix='/management')
APP.register_blueprint(reservation.page, url_prefix='/reservation')
APP.register_blueprint(stats.page, url_prefix='/stats')


# ==================================== Universal Routes ======================================== #
@APP.route('/',methods=['GET', 'POST'])
def index():
    ''''Renders the default template'''
    if flask_login.current_user.is_authenticated:
        return render_template('default.html',
                               message='Hello {}'.format(flask_login.current_user.Name),
                               current_user = flask_login.current_user,
                               logged_in=True,
                               role=flask_login.current_user.role)
    else:
        form = register.RegistrationForm()
        if form.validate_on_submit():
          try:
            # utils.connect_to_db()
            cust = user.User.create_user(
            name=form.name.data,
            password=form.password.data,
            email=form.email.data,
            phone_no = form.phone.data,
            address = form.address.data,
            role = form.role.data
            )
            flash("Successfully Registered!", 'success')
          except Exception as e:
            traceback.print_exc(file=sys.stdout)
            flash('Registration failed: ' + str(e), 'danger')
        return render_template('default.html',logged_in=False, form=form)

# =============================================================================================== #