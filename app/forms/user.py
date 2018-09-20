from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, Length, InputRequired, EqualTo
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=20)])

class RemoveUserForm(FlaskForm):
    id = StringField('id')

class ForgotUserForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])

class ChangeUserForm(FlaskForm):
    password = PasswordField(
        'Password',validators = [
            Length(min=6, max=20),
            InputRequired(),
            EqualTo('confirm', message='Passwords must match')
        ])

    confirm = PasswordField('Repeat password')

class UserForm(FlaskForm):
    id = StringField('id')
    name = StringField('Name', validators=[Length(min=3, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=6, max=30)])
    
    password = PasswordField(
        'Password',validators = [
            Length(min=6, max=20),
            InputRequired(),
            EqualTo('confirm', message='Passwords must match')
        ])

    confirm = PasswordField('Repeat password')

    # get roles from config.py and transform dist to [(role1, name1), (role2, name2), ...] 
    choices = [(k, v.title()) for k, v in enumerate(app.config['ACCESS']) ]
    role = SelectField('Role', choices=choices, coerce=int)

    def validate(self):
        """ The FlaskForm already has its validator,
            but since we need the unique emails in the database,
            we need to do a search manually to verify
        
        Returns
            Boolean -- valid or not valid
        """

        # Normal FlaskForm validate
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # Validate if is unique email
        if self.id.data == '': 
            check_email = User.objects(email=self.email.data).first()
        else:
            check_email = User.objects(id__ne=self.id.data, email=self.email.data).first()

        if check_email is not None:
            self.email.errors.append('Email must be unique')
            return False

        return True