from flask import flash, redirect, render_template, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Role, User

from . import main
from .forms import NameForm, RoleForm, EditUserForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Parece que você alterou o nome!')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))


@main.route('/user/<name>')
@login_required
def user(name):
    return render_template('user.html', name=name) 


@main.route('/user/list', methods=['GET', 'POST'])
@login_required
def list_user():
    users = User.query.all()
    return render_template('list_user.html', users=users)


@main.route('/role/add', methods=['GET', 'POST'])
@login_required
def add_role():
    form = RoleForm()
    roles = Role.query.all()
    if form.validate_on_submit():
        new_role = Role()
        new_role.name = form.name.data
        db.session.add(new_role)
        db.session.commit()

        flash('Função cadastrada com sucesso.')
        return redirect(url_for('main.index'))
    return render_template('add_role.html', form=form, roles=roles)


@main.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    
    logged_user = User.query.filter_by(id=current_user.id).first()
    logged_user_role = Role.query.filter_by(id=logged_user.role_id).first()

    edit_user = User.query.filter_by(id=id).first()
    edit_user_role = Role.query.filter_by(id=edit_user.role_id).first()
    form = EditUserForm(edit_user)
    
    if form.validate_on_submit():
        edit_user.username = form.username.data
        edit_user.role_id = form.role.data
        db.session.commit()

        flash('Função cadastrada com sucesso.')
        return redirect(url_for('main.index'))

    if logged_user_role.name != "Administrador":
        del form.role
    if logged_user.id != edit_user.id:
        del form.username

    return render_template('edit_user.html', form=form, show_user=edit_user, show_user_role=edit_user_role)