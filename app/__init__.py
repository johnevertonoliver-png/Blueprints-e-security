from flask import Flask, render_template, request
from config import DevelopmentConfig
from app.security import gerar_csrf_token, validar_csrf

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)

    # Disponibiliza csrf_token() dentro dos templates Jinja2
    app.jinja_env.globals['csrf_token'] = gerar_csrf_token

    # Valida o token CSRF em TODA requisição POST (antes de chegar na rota)
    @app.before_request
    def proteger_csrf():
        if request.method == 'POST':
            validar_csrf()

    # Registra os blueprints
    from app.blog import blog_bp
    from app.admin import admin_bp
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Tratadores de erro globais
    @app.errorhandler(403)
    def acesso_negado(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def nao_encontrado(e):
        return render_template('errors/404.html'), 404

    return app
