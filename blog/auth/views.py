from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import logout_user, login_user, login_required, current_user

from blog.app import login_manager
from blog.forms.userAuth import UserAuthorizationForm
from blog.forms.userRegistration import UserRegisterForm
from blog.models import User
from blog.models.database import db

authBlueprint = Blueprint('authBlueprint', __name__, url_prefix="/auth", static_folder='../static')


@authBlueprint.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('userBlueprint.get_user', pk=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []
    # Обработка регистрации пользователя
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("Почта не уникальна")
            return render_template("auth/register.html", form=form)

        _user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            is_staff=True if request.form.get('is_staff') == 'on' else False,
            password=generate_password_hash(form.password.data),
        )
        db.session.add(_user)
        db.session.commit()
        login_user(_user)
        return redirect(url_for('userBlueprint.get_user', pk=current_user.id))

    return render_template(
        "auth/register.html",
        form=form,
        errors=errors,
    )

@authBlueprint.route('/', methods=["POST", "GET"])
def login():
    form = UserAuthorizationForm(request.form)
    errors = []
    if current_user.is_authenticated:
        return redirect(url_for('userBlueprint.get_user', pk=current_user.id))

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            errors.append("Неправильный логин или пароль")
            return render_template("/auth/login.html", form=form, errors=errors)

        login_user(user)
        return redirect(url_for('userBlueprint.get_user', pk=user.id))

    return render_template("/auth/login.html", form=form, errors=errors)

@authBlueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authBlueprint.login'))


@login_manager.user_loader
def user_loader(user_id: int) -> User:
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("authBlueprint.login"))
