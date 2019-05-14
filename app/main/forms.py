from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired 

from app.models import Role

class NameForm(FlaskForm):
    name = StringField('Qual o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class EditUserForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired()])
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Enviar')

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name) for role in Role.query.order_by(Role.name).all() 
        ]
        self.user = user
        self.username.data = user.username

        
class RoleForm(FlaskForm):
    name = StringField('Função', validators=[
        DataRequired()
    ])
    submit = SubmitField('Cadastrar')

    def validate_name(self, field):
        role = Role.query.filter_by(name=field.data).first()
        if role:
            raise ValidationError('Função já cadastrada')
