from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user
from com.models import SysUser, SysLog, SysMenu
bp_auth = Blueprint('auth', __name__)
@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login/sign_in.html')
@bp_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))