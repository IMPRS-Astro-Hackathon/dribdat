# -*- coding: utf-8 -*-
"""Authentication views."""

from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, current_app)
from flask_login import login_user, logout_user, login_required, current_user
from flask_dance.contrib.slack import slack
from flask_dance.contrib.azure import azure  # noqa: I005
from flask_dance.contrib.github import github
# Dribdat modules
from dribdat.user.models import User, Event, Role
from dribdat.extensions import login_manager  # noqa: I005
from dribdat.utils import flash_errors, random_password, sanitize_input
from dribdat.public.forms import LoginForm, UserForm
from dribdat.user.forms import RegisterForm
from dribdat.database import db
from dribdat.mailer import user_activation
# noqa: I005

blueprint = Blueprint('auth', __name__, static_folder="../static")


def current_event():
    """Return the first featured event."""
    return Event.query.filter_by(is_current=True).first()


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


def oauth_type():
    """Check if Slack or another OAuth has been configured."""
    if "OAUTH_TYPE" in current_app.config:
        return current_app.config["OAUTH_TYPE"].lower()
    else:
        return None


@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    """Handle the login route."""
    # Skip login form on forced SSO
    if request.method == "GET" and current_app.config["OAUTH_SKIP_LOGIN"]:
        if not request.args.get('local') and oauth_type():
            return redirect(url_for(oauth_type() + '.login'))
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user, remember=True)
            if not form.user.active:
                flash(
                    'This user account is under review. '
                    + 'Please update your profile and contact the organizing '
                    + 'team to access all functions of this platform.',
                    'warning')
            else:
                flash("You are logged in! Time to make something awesome ≧◡≦",
                      'success')
            redirect_url = request.args.get("next") or url_for("public.home")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/login.html",
                           form=form, oauth_type=oauth_type())


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    """Register new user."""
    if current_app.config['DRIBDAT_NOT_REGISTER']:
        flash("Registration currently not possible.", 'warning')
        return redirect(url_for("auth.login", local=1))
    form = RegisterForm(request.form)
    if request.args.get('name') and not form.username.data:
        form.username.data = request.args.get('name')
    if request.args.get('email') and not form.email.data:
        form.email.data = request.args.get('email')
    if request.args.get('web') and not form.webpage_url.data:
        form.webpage_url.data = request.args.get('web')
    if not form.validate_on_submit():
        flash_errors(form)
        return render_template('public/register.html',
                               form=form, oauth_type=oauth_type())
    # Continue with user creation
    sane_username = sanitize_input(form.username.data)
    new_user = User.create(
                    username=sane_username,
                    email=form.email.data,
                    webpage_url=form.webpage_url.data,
                    password=form.password.data,
                    active=True)
    new_user.socialize()
    if User.query.count() == 1:
        # This is the first user account - promote it
        new_user.is_admin = True
        new_user.save()
        flash("Administrative user created - oh joy!", 'success')
    elif current_app.config['DRIBDAT_USER_APPROVE']:
        # Approval of new user accounts required
        new_user.active = False
        new_user.save()
        if current_app.config['MAIL_SERVER']:
            with current_app.app_context():
                user_activation(new_user)
            flash("New accounts require activation. "
                  + "Please click the dribdat link in your e-mail.", 'success')
        else:
            flash("New accounts require approval from the event organizers. "
                  + "Please update your profile and await activation.",
                  'success')
    else:
        flash(
            "Thank you for registering. You can now log in and submit "
            + "projects.", 'success')
    login_user(new_user, remember=True)
    return redirect(url_for('public.home'))


@blueprint.route("/activate/<userhash>", methods=['GET'])
def activate(userhash):
    """Activate or reset new user account."""
    a_user = User.query.filter_by(sso_id=userhash).first()
    if a_user is not None:
        a_user.sso_id = None
        a_user.active = True
        a_user.save()
        login_user(a_user, remember=True)
        flash("Your user account has been activated.", 'success')
        return redirect(url_for('auth.user_profile'))
    flash("Activation not found. Retry or contact an organizer", 'warning')
    return redirect(url_for('public.home'))


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/forgot/')
def forgot():
    """Forgot password."""
    return render_template('public/forgot.html', oauth_type=oauth_type())


@blueprint.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Display or edit the current user profile."""
    user = current_user
    user_is_valid = True
    if not user.active:
        flash('This user account is under review. Please update your profile '
              + ' and contact the organizing team to access all functions of '
              + 'this platform.', 'warning')

    form = UserForm(obj=user, next=request.args.get('next'))
    form.roles.choices = [(r.id, r.name) for r in Role.query.order_by('name')]

    # Check conflicting PKs
    if form.email.data != user.email:
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash('This e-mail address is already registered.', 'error')
            user_is_valid = False

    # Validation has passed
    if form.validate_on_submit() and user_is_valid:
        # Assign roles
        user.roles = [Role.query.filter_by(
            id=r).first() for r in form.roles.data]
        del form.roles

        # Sanitize username
        user.username = sanitize_input(form.username.data)
        del form.username

        # Assign password if changed
        originalhash = user.password
        form.populate_obj(user)
        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.password = originalhash

        db.session.add(user)
        db.session.commit()
        user.socialize()
        flash('Profile updated.', 'success')
        return redirect(url_for('public.user', username=user.username))

    if not form.roles.choices:
        del form.roles
    else:
        form.roles.data = [(r.id) for r in user.roles]
    return render_template('public/useredit.html',
                           user=user, form=form, active='profile')


def get_or_create_sso_user(sso_id, sso_name, sso_email, sso_webpage=''):
    """Match a user account based on SSO_ID."""
    sso_id = str(sso_id)
    user = User.query.filter_by(sso_id=sso_id).first()
    if not user:
        if isinstance(current_user, User) and current_user.active:
            user = current_user
            user.sso_id = sso_id
        else:
            user = User.query.filter_by(email=sso_email).first()
            if user:
                # Update SSO identifier
                user.sso_id = sso_id
                db.session.add(user)
                db.session.commit()
            else:
                username = sso_name.lower().replace(" ", "_")
                user = User.query.filter_by(username=username).first()
                if user:
                    flash(
                        'Duplicate username (%s), please try again or '
                        + 'contact an admin.' % username, 'warning')
                    return redirect(url_for("auth.login", local=1))
                user = User.create(
                    username=username,
                    sso_id=sso_id,
                    email=sso_email,
                    webpage_url=sso_webpage,
                    password=random_password(),
                    active=True)
            user.socialize()
            login_user(user, remember=True)
            flash("Welcome! Please complete your user account.", 'info')
            return redirect(url_for("auth.user_profile"))
    login_user(user, remember=True)
    if not user.active:
        flash('This user account is under review. Please update your profile '
              + 'and contact the organizing team to access all functions of '
              + 'this platform.', 'warning')
    else:
        flash(u'Logged in! Time to make something awesome ≧◡≦', 'success')

    if current_event():
        return redirect(url_for("public.event", event_id=current_event().id))
    else:
        return redirect(url_for("public.home"))


@blueprint.route("/slack_login", methods=["GET", "POST"])
def slack_login():
    """Handle login via Slack."""
    if not slack.authorized:
        flash('Access denied to Slack', 'danger')
        return redirect(url_for("auth.login", local=1))

    resp = slack.get("https://slack.com/api/users.identity")
    if not resp.ok:
        flash('Unable to access Slack data', 'danger')
        return redirect(url_for("auth.login", local=1))
    resp_data = resp.json()
    if 'user' not in resp_data:
        flash('Invalid Slack data format', 'danger')
        # print(resp_data)
        return redirect(url_for("auth.login", local=1))
    resp_user = resp_data['user']
    return get_or_create_sso_user(
        resp_user['id'],
        resp_user['name'],
        resp_user['email'],
    )


@blueprint.route("/azure_login", methods=["GET", "POST"])
def azure_login():
    """Handle login via Azure."""
    if not azure.authorized:
        flash('Access denied to Azure', 'danger')
        return redirect(url_for("auth.login", local=1))

    resp = azure.get("https://graph.microsoft.com/v1.0/me/")
    if not resp.ok:
        flash('Unable to access Azure data', 'danger')
        return redirect(url_for("auth.login", local=1))
    resp_user = resp.json()
    if 'mail' not in resp_user:
        flash('Invalid Azure data format', 'danger')
        # print(resp_user)
        return redirect(url_for("auth.login", local=1))
    return get_or_create_sso_user(
        resp_user['id'],
        resp_user['displayName'],
        resp_user['mail'],
    )


@blueprint.route("/github_login", methods=["GET", "POST"])
def github_login():
    """Handle login via GitHub."""
    if not github.authorized:
        flash('Access denied - please try again', 'warning')
        return redirect(url_for("auth.login", local=1))

    resp = github.get("/user")
    if not resp.ok:
        flash('Unable to access GitHub data', 'danger')
        return redirect(url_for("auth.login", local=1))
    resp_user = resp.json()
    if 'email' not in resp_user or 'login' not in resp_user:
        flash('Invalid GitHub data format', 'danger')
        # print(resp_user)
        return redirect(url_for("auth.login", local=1))

    resp_emails = github.get("/user/emails")
    if not resp.ok:
        flash('Unable to access GitHub e-mail data', 'danger')
        return redirect(url_for("auth.login", local=1))
    for u in resp_emails.json():
        if u['primary'] and u['verified']:
            return get_or_create_sso_user(
                resp_user['id'],
                resp_user['login'],
                u['email'],
                'https://github.com/%s' % resp_user['login']
            )
    flash('Please verify an e-mail with GitHub', 'danger')
    return redirect(url_for("auth.login", local=1))
