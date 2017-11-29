from flask import Flask, render_template
import flask_login


APP = Flask(__name__, template_folder="views/templates", static_url_path='/static')
APP.secret_key = 'A^*4L#Cs8UjQaq!Hjmhz'

LM = flask_login.LoginManager()
LM.init_app(APP)

# Register all views after here
# =======================
from asst.views import demo


APP.register_blueprint(demo.page, url_prefix='/demo')


# ==================================== Universal Routes ======================================== #
@APP.route('/')
def index():
    ''''Renders the default template'''
    if flask_login.current_user.is_authenticated:
        return render_template('index.html',
                               message='Hello {}'.format(flask_login.current_user.name),
                               logged_in=True,
                               role=flask_login.current_user.role)
    else:
        return render_template('index.html',logged_in=False)

# =============================================================================================== #