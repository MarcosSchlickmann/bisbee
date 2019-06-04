from flask import flash, redirect, render_template, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.decorators import admin_required, permission_required
from app.main.forms import (
    EditProfileAdminForm, EditProfileForm, NameForm,RoleForm
)
from app.models import Role, User

from . import main


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


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user) 
    


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


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Perfil editado com sucesso!')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    return render_template(
        'edit-profile.html', form=form, username=current_user.username)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Usuário editado com sucesso!')
        return redirect(url_for('.user', username=user.username))
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.about_me.data = user.about_me
    return render_template(
        'edit-profile.html', form=form, username=user.username
    )