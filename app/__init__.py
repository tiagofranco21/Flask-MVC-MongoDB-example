from flask import Flask, render_template, redirect,url_for
from flask_assets import Environment, Bundle
from flask_mongoengine import MongoEngine
from flask_breadcrumbs import Breadcrumbs
from flask_mail import Mail
from functools import wraps

from flask_login import  current_user

# create the flask object
app = Flask(__name__)

# Initialize Flask-Breadcrumbs
Breadcrumbs(app=app)

# Configurations
app.config.from_object('config')
app.jinja_env.globals['APP_SETTINGS'] = app.config['APP_SETTINGS']

# mail object
mail = Mail(app)

# Define the database object which is imported
# by modules and controllers
db = MongoEngine(app)

#assets configuration
assets = Environment(app)

# to minify ---> filters='cssmin', filters='jsmin'
css = Bundle('css/bootstrap.min.css', 'css/font-awesome.min.css', 'css/ionicons.min.css', 'css/AdminLTE.min.css', 'css/skin-black.min.css', 'css/custom.css', output='gen/main.css')
js = Bundle('js/jquery.min.js', 'js/bootstrap.min.js', 'js/adminlte.min.js', 'js/custom.js', output='gen/main.js')

# make available in template
assets.register('main_js', js)
assets.register('main_css', css)



# ---------------------- ERRORS HANDLER -----------------

@app.errorhandler(403)
def forbidden(e):
    app.config['APP_SETTINGS']['title'] = 'Forbidden'
    return render_template('error.html', code=403, txt='Forbidden Page'), 403


@app.errorhandler(404)
def not_found(e):
    app.config['APP_SETTINGS']['title'] = 'Not Found'
    return render_template('error.html', code=404, txt='Page not Found'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    app.config['APP_SETTINGS']['title'] = 'Method not Allowed'
    return render_template('error.html', code=405, txt='Method not Allowed'), 405


@app.errorhandler(500)
def server_error(e):
    app.config['APP_SETTINGS']['title'] = 'Server Error'
    return render_template('error.html', code=500, txt='Server Error'), 500



# ------------------------ FUNCTIONS --------------------
def flash_errors(form):
    """ Transform FlaskForm errors into a single object to display in template with Flash Plugin
    *This function must be called after form.validate() failed

    Arguments:
        form {FlaskForm} -- Make sure that all fields have validators 

    Returns:
        dist -- ['text error1', 'text error2', ...]
    """
    messagens = []
    for field, errors in form.errors.items():    
        for error in errors:
           messagens.append("Error in the %s field - %s" % (getattr(form, field).label.text, error))

    return messagens



def login_roles_required(role=app.config['ACCESS'][0]):
    """This decorator function make sure if the user has been logged and if he has access to this call
    We have levels hierarchy, you can see the options and your priorities on config.py

    Keyword Arguments:
        role {str} -- Must be the minimum level for this call (default: minimum level set on config.py)

    ** If the user has been logged, we add USER as global var for every template has access  
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated == False:
                return redirect(url_for('login'))
            else:
                if app.config['ACCESS'].index(role) > current_user.role:
                    return not_found(404)
                else:
                    app.jinja_env.globals['USER'] = current_user
            return f(*args, **kwargs)
        return wrapped
    return wrapper

    
#import all controllers
from app.controllers import *