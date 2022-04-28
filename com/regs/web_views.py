def reg_web_views(app):
    from com.views.auth import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/auth')