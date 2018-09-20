from app import app, flash_errors, login_roles_required, mail
from flask import flash, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user
from app.models.user import User
from app.forms.user import LoginForm, UserForm, RemoveUserForm, ForgotUserForm, ChangeUserForm
from flask_breadcrumbs import register_breadcrumb
from flask_mail import Message
import random

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


# -------------- Login Managers methods ---------------

# the route / will be redirect to login, because in this app we just have admin area
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login 
@app.route('/login', methods=['GET', 'POST'])
def login():

    app.config['APP_SETTINGS']['title'] = 'Login'

    if current_user.is_authenticated == True:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('login.html', form=form, login=True)

# Logout
@app.route('/logout', methods = ['GET'])
@login_roles_required()
def logout():
    logout_user()
    return redirect(url_for('login'))


# generate a password with length "passlen" with no duplicate characters in the password
def generate_password(passlen=6):
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    return "".join(random.sample(s, passlen))

# Forgot Password
# We send a email with new password 
# You can config the sender in config.py
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    app.config['APP_SETTINGS']['title'] = 'Forgot Password'

    form = ForgotUserForm()

    if request.method == 'POST':
        user_to_edit = User.objects(email=form.email.data).first()
        if (user_to_edit is None):
            flash("This email is not in our database", 'error')
        else:
            new_password = generate_password()
            
            hashpass = generate_password_hash(new_password, method='sha256')
            user_to_edit.password = hashpass
            user_to_edit.save()

            msg = Message('Password Recovery', recipients = [form.email.data])
            msg.body = "This is your new password: "+new_password
            mail.send(msg)
            flash("We email you with your new password", 'success')
    
    return render_template('login.html', form=form, login=False)


#! This route had been made to generate one first user
#! In privacy web app, we have not register page, so this is better than inject Mongo Document
#! You must remove this route
# @app.route('/first_user')
# def first_user():
#     hashpass = generate_password_hash('123123', method='sha256')
#     User(email='email@email.com', password=hashpass, name='First User', role=2).save()
#     return redirect(url_for('login'))


# ADMIN HOME 
@register_breadcrumb(app, '.', 'Home')
@app.route('/dashboard')
@login_roles_required()
def dashboard(): 
    app.config['APP_SETTINGS']['title'] = 'Dashboard'
    return render_template('users/home.html')


# Change password - Current User 
@register_breadcrumb(app, '.change_password', 'Change Password')
@app.route('/change_password', methods = ['GET', 'POST'])
@login_roles_required()
def change_password():
    
    app.config['APP_SETTINGS']['title'] = 'Change Password'

    form = ChangeUserForm()

    if request.method == 'POST':
        if form.validate():
            user_to_edit = User.objects(id=current_user.id).first()
            hashpass = generate_password_hash(form.password.data, method='sha256')
            user_to_edit.password = hashpass
            user_to_edit.save()
            flash('Your password has been changed successfully', 'success')
            return redirect(url_for('dashboard'))
        else: 
            flash(flash_errors(form), 'error')
   
    return render_template('users/change_password.html', form=form)



# -------------------- Users CRUD Methods -------------------


# List 
@register_breadcrumb(app, '.users', 'Users')
@app.route('/users')
@login_roles_required('MASTER')
def users():
    
    app.config['APP_SETTINGS']['title'] = 'Users'

    if(request.args.get('page') is None):
        page=1
    else:
        page = int(request.args.get('page') )

    form = RemoveUserForm()
    users = User.objects.paginate(page=page, per_page=10)
    
    roles = [v.title() for v in app.config['ACCESS']]
    return render_template('users/index.html', form=form, users=users, roles=roles)

# ADD
@register_breadcrumb(app, '.users.users_add', 'Add')
@app.route('/users/add', methods = ['GET', 'POST'])
@login_roles_required('MASTER')
def users_add():
    
    app.config['APP_SETTINGS']['title'] = 'Users Add'

    form = UserForm()   

    if request.method == 'POST':
        if form.validate():
            hashpass = generate_password_hash(form.password.data, method='sha256')
            User(email=form.email.data, password=hashpass, name=form.name.data, role=form.role.data).save()
            return redirect(url_for('users'))
        else:
            flash(flash_errors(form), 'error')
    
    return render_template('users/add.html', form=form, mod='add')


# Edit breadcrump help
def view_user_edit(*args, **kwargs):
    user_id = request.view_args['user_id']
    return [{'text': "Edit", 'url': user_id}]

# EDIT
@register_breadcrumb(app, '.users.users_edit', 'Edit', '', dynamic_list_constructor=view_user_edit)
@app.route('/users/edit/<user_id>', methods = ['GET', 'POST'])
@login_roles_required('MASTER')
def users_edit(user_id):

    app.config['APP_SETTINGS']['title'] = 'Users Edit'

    user_to_edit = User.objects(id=user_id).first()
    form = UserForm(formdata=request.form, obj=user_to_edit)
    if request.method == 'POST':
        if form.validate():
            hashpass = generate_password_hash(form.password.data, method='sha256')
            user_to_edit.email = form.email.data
            user_to_edit.name = form.name.data
            user_to_edit.password = hashpass
            user_to_edit.role = form.role.data
            user_to_edit.save()

            return redirect(url_for('users'))
        else: 
            flash(flash_errors(form), 'error')
    
    return render_template('users/add.html', form=form, mod='edit')

# DELETE
@app.route('/users/delete', methods = ['POST'])
@login_roles_required('MASTER')
def users_delete():

    form = RemoveUserForm()
    user_to_del = User.objects(id=form.id.data).first()
    if user_to_del is None:
        flash('Could not find this user', 'error')
    else:
        user_to_del.delete()
        flash('User has been removed', 'success')

    return redirect(url_for('users'))