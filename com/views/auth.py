from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from com.forms.auth import LoginForm
from com.models import SysUser, SysLog, SysMenu
from com.plugins import db
import uuid
bp_auth = Blueprint('auth', __name__)
@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user_pwd = form.user_pwd.data
        # print('User id is %s, password is %s' %(user_id, user_pwd))
        user = SysUser.query.filter_by(user_id=user_id.lower()).first()
        if user:
            if user.active:
                validate_ok = user.validate_password(user_pwd)
                if validate_ok:
                    login_user(user, True)
                    log = SysLog(id=uuid.uuid4().hex, url='auth.login', operation='登录系统', user=user)
                    db.session.add(log)
                    db.session.commit()
                    # 类GMES跳转
                    # return redirect(url_for('main.to_function'))
                    # 传统布局使用以下跳转
                    modules = current_user.authed_modules
                    if modules:
                        for module in modules:
                            print('Module name : ', module.name)
                        module_menu = current_user.authed_menus
                        for module, menu in module_menu.items():
                            print('Module id : ', module, ', menus : ', menu)
                        module_id = current_user.authed_modules[0].id
                        return redirect(url_for('main.to_uri', module_id=module_id,
                                                menu_id=current_user.authed_menus[module_id][0].id))
                    else:
                        flash('该用户没有分配任何系统权限，请联系管理员！')
                        return render_template('main/not-authed.html')
                else:
                    flash('密码错误！')
            else:
                flash('用户已停用！')
        else:
            flash('用户不存在！')
    return render_template('login/sign_in.html', form=form)
@bp_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))